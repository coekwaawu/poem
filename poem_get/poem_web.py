import re
import requests
import time
from pyquery import PyQuery as pq


def test_print_array(array):
    i = 1
    for item in array:
        print("({}){}".format(i, item))
        i += 1


def get_target_urls(start_page_number, end_page_number):
    target_urls = ["https://www.gushiwen.org/shiwen/default_0A0A{}.aspx".format(i) for i in
                   range(start_page_number, end_page_number + 1)]
    return target_urls


def post_poem_yi_zhu_shang(poem_id, value):
    post_url = "https://so.gushiwen.org/shiwen2017/ajaxshiwencont.aspx"
    headers = {
        'authority': 'so.gushiwen.org',
        'method': 'POST',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'ASP.NET_SessionId=ugfjj04fd0ujod4o3pdh4t3n; Hm_lvt_04660099568f561a75456483228a9516='
                  '1523587509,1524206749,1524453317; Hm_lpvt_04660099568f561a75456483228a9516=1524703379',
        'referer': 'https://so.gushiwen.org/',
        'pragma': 'no-cache',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/65.0.3325.181 Safari/537.36',
    }
    data = {"id": "{}".format(poem_id), "value": value}
    return requests.post(post_url, data=data, headers=headers).content.decode()


def get_poem_by_id(poem_id):
    poem_url = "https://so.gushiwen.org/shiwenv_{}.aspx".format(poem_id)
    fail_count = 10
    poempage = ""
    success = False
    while not success:
        try:
            poempage = requests.get(poem_url).text
            success = True
        except Exception as e:
            success = False
            print("出现错误,错误信息:{},请等待 5 秒再尝试".format(e))
            time.sleep(5)
    success = False
    poem = {}
    while not success and fail_count > 0:
        try:
            pq_poempage = pq(poempage)(".main3 .left .sons .cont")
            title = pq_poempage("h1").text()
            dynasty = pq(pq_poempage(".source a")[0]).text()
            author = pq(pq_poempage(".source a")[1]).text()
            content = pq(pq_poempage(".contson")[0]).html()
            yi = post_poem_yi_zhu_shang(poem_id, "yi")
            zhu = post_poem_yi_zhu_shang(poem_id, "zhu")
            shang = post_poem_yi_zhu_shang(poem_id, "shang")
            yizhu = post_poem_yi_zhu_shang(poem_id, "yizhu")
            yishang = post_poem_yi_zhu_shang(poem_id, "yishang")
            zhushang = post_poem_yi_zhu_shang(poem_id, "zhushang")
            yizhushang = post_poem_yi_zhu_shang(poem_id, "yizhushang")
            poem = {
                "poem_id": poem_id,
                "title": title,
                "dynasty": dynasty,
                "author": author,
                "content": content,
                "yi": yi,
                "zhu": zhu,
                "shang": shang,
                "yizhu": yizhu,
                "yishang": yishang,
                "zhushang": zhushang,
                "yizhushang": yizhushang
            }
            success = True
        except Exception as e:
            fail_count -= 1
            success = False
            print("get_poem_by_id出现错误,错误信息:{},poem_id:{},请等待 5 秒再尝试".format(e, poem_id))
            time.sleep(5)
    if fail_count == 0:
        return None
    return poem


def remove_copyright_string(string):
    error_pattern = re.compile("<p>(网.+?员)")
    string_temp = string.replace("\n", "")
    if len(re.findall(error_pattern, string_temp)) > 0:
        remove_error_pattern = re.compile("(﻿<.+?.</html>)")
        string = re.sub(remove_error_pattern, "", string_temp)
    remove_copyright_pattern = re.compile("(<p style=.+?.org</p>)")
    return re.sub(remove_copyright_pattern, "", string)


def remove_copyright_poem(poem):
    poem['yi'] = remove_copyright_string(poem['yi'])
    poem['zhu'] = remove_copyright_string(poem['zhu'])
    poem['shang'] = remove_copyright_string(poem['shang'])
    poem['yizhu'] = remove_copyright_string(poem['yizhu'])
    poem['yishang'] = remove_copyright_string(poem['yishang'])
    poem['zhushang'] = remove_copyright_string(poem['zhushang'])
    poem['yizhushang'] = remove_copyright_string(poem['yizhushang'])
    return poem


def get_remove_copyright_poem_by_id(poem_id):
    return remove_copyright_poem(get_poem_by_id(poem_id))


def get_listpage_poem_ids(start, end):
    target_urls = get_target_urls(start, end)
    poem_ids = []
    for target_url in target_urls:
        success = False
        while not success:
            try:
                page = requests.get(target_url)
                success = True
            except Exception as e:
                success = False
                print("出现错误,错误信息:{},请等待 5 秒再尝试".format(e))
                time.sleep(5)
        poem_id_pattern = re.compile(r'id=\"contson(.+?)\"')
        ids = re.findall(poem_id_pattern, page.text)
        for poem_id in ids:
            poem_ids.append(poem_id)
        page.close()

    return poem_ids


# print(get_poem_by_id("ffc3de59f87e")["zhu"])


def get_author_id_and_name_list_urls(start, end):
    return ["https://so.gushiwen.org/authors/default.aspx?p={}".format(i) for i in range(start, end)]


def get_author_id_and_name_list_from_web(url):
    id_and_name_list = []
    page = requests.get(url)
    pq_page = pq(page.text)(".main3 .left")
    pattern = "<a target=\"_blank\" style=\"font-size:18px; line-height:22px; height:22px;\" " \
              "href=\"/authorv_(.+?).aspx\"><b>(.+?)</b></a>"
    temp_list = re.findall(pattern, pq_page.html())
    for item in temp_list:
        id_and_name_list.append(item)
    print("网上获取作者id和姓名成功！{}".format(id_and_name_list))
    page.close()
    return id_and_name_list


def get_author_info_jianjie_by_id(poem_author_id="7ab3b8200774"):
    url = "https://so.gushiwen.org/authorv_{}.aspx".format(poem_author_id)
    page = requests.get(url)
    pq_page = pq(page.text)(".main3 .left")
    pattern_jianjie = "<p style=\" margin:0px;\">(.+?)<a href=\"/authors/authorvsw_"
    jianjie = re.findall(pattern_jianjie, pq_page.html())[0]
    page.close()
    return jianjie


def get_author_info_ziliao_ids_by_poem_author_id(poem_author_id="7ab3b8200774"):
    url = "https://so.gushiwen.org/authorv_{}.aspx".format(poem_author_id)
    page = requests.get(url)
    pq_page = pq(page.text)(".main3 .left")
    pattern_ziliao = "\"fanyiquan(.+?)\""
    ziliao_ids = re.findall(pattern_ziliao, pq_page.html())
    return ziliao_ids


def get_poem_author_ziliao_by_ziliao_id(id):
    url = "https://so.gushiwen.org/authors/ajaxziliao.aspx?id={}".format(id)
    page = requests.get(url)
    pq_page = pq(page.text)
    ziliao = remove_copyright_string(pq_page.html())
    level1_pattern = "<h2><span style=\"float:left;\">(.+?)</span></h2>"
    level1 = re.findall(level1_pattern, ziliao)
    level2_pattern = "<strong>(.+?)<br/></strong>"
    level2 = re.findall(level2_pattern, ziliao)
    level3_pattern = "<p><strong>(.+?)<br/></strong>(.+?)</p>|<p>(.+?)</p>"
    html_pattern = "<a.+?>|</a>"
    level3 = re.findall(level3_pattern, re.sub(html_pattern, "", ziliao))
    ziliao = level3
    page.close()
    return ziliao


def get_author_info_ziliao_list_by_poem_author_id(poem_author_id="7ab3b8200774"):
    return ""


#print(get_author_id_and_name_list_from_web())
print(get_author_info_ziliao_ids_by_poem_author_id())
test_print_array(get_poem_author_ziliao_by_ziliao_id('1379'))
#print(get_author_info_ziliao_list_by_id())

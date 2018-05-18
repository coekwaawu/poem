import re
import requests
import time
from pyquery import PyQuery as pq


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

'''

def get_poem_pq_page_by_url(target_url):
	page = requests.get(target_url).text
	if page != '':
		pq_page = pq(page)
		return pq_page
	else:
		return None

def get_detailpage_poem_yi_by_id(poem_id):
	sentences_yi = []
	reference_yi_list = []
	target_url = "https://so.gushiwen.org/shiwen2017/ajaxshiwencont.aspx?id={}&value=yi".format(poem_id)
	pq_page = get_poem_pq_page_by_url(target_url)
	if pq_page is not None:
		yi_list = pq_page("p")
		for item in yi_list:
			sentence_yi = {"sentence":"","yi":""}
			if pq(item).attr("style") is None:
				sentence_yi["sentence"] = pq(item)("p")[0].text
				sentence_yi["yi"] = pq(item)("span")[0].text
				sentences_yi.append(sentence_yi)
			else:
				reference_yi = item.text

		div = pq_page("div div")
		if pq(div).attr("style") is not None:
			for item in div:
				reference_yi_list.append(pq(item).text())

		poem_yi = {"poem_id":poem_id,"sentences_yi":sentences_yi,"reference_yi":reference_yi,"reference_yi_list":reference_yi_list}
		return poem_yi

def get_detailpage_poem_zhu_by_id(poem_id):
	sentences_zhu = []
	reference_zhu_list = []
	target_url = "https://so.gushiwen.org/shiwen2017/ajaxshiwencont.aspx?id={}&value=zhu".format(poem_id)
	pq_page = get_poem_pq_page_by_url(target_url)
	if pq_page is not None:
		zhu_list = pq_page("div p")
		for item in zhu_list:
			sentence_zhu = {"sentence_include_pinyin":"","zhu":""}
			if pq(item).attr("style") is None:
				sentence_include_pinyin_pattern = re.compile(r'(.+?)<br/>')
				sentence_zhu["sentence_include_pinyin"] = re.findall(sentence_include_pinyin_pattern,pq(item).html())[0]
				sentence_zhu["zhu"] = pq(pq(item)('span')).text()
				sentences_zhu.append(sentence_zhu)
		reference_zhu = pq_page("p").eq(-1).text()
		div = pq_page("div div")
		if pq(div).attr("style") is not None:
			for item in div:
				reference_zhu_list.append(pq(item).text())
		poem_zhu = {"poem_id":poem_id,"sentences_zhu":sentences_zhu,"reference_zhu":reference_zhu,"reference_zhu_list":reference_zhu_list}
		return poem_zhu

def get_detailpage_poem_shang_by_id(poem_id):
	poem_shang = []
	target_url = "https://so.gushiwen.org/shiwen2017/ajaxshiwencont.aspx?id={}&value=shang".format(poem_id)
	pq_page = get_poem_pq_page_by_url(target_url)
	if pq_page is not None:
		shang_list_pattern = re.compile(r'<div class=\"hr\"/>(.+?)')
		shang_list = re.findall(shang_list_pattern,pq_page.html())
		return shang_list
	return poem_shang

'''

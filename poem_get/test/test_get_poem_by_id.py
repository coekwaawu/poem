import requests
import time
from pyquery import PyQuery as pq

def post_poem_yi_zhu_shang(poem_id,value):
	post_url = "https://so.gushiwen.org/shiwen2017/ajaxshiwencont.aspx"
	headers = {
	'authority': 'so.gushiwen.org',
	'method': 'POST',
	'scheme': 'https',
	'accept': '*/*',
	'accept-encoding': 'gzip, deflate, br',
	'accept-language': 'zh-CN,zh;q=0.9',
	'cookie': 'ASP.NET_SessionId=ugfjj04fd0ujod4o3pdh4t3n; Hm_lvt_04660099568f561a75456483228a9516=1523587509,1524206749,1524453317; Hm_lpvt_04660099568f561a75456483228a9516=1524703379',
	'referer': 'https://so.gushiwen.org/',
	'pragma': 'no-cache',
	'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
	}
	data = {"id":"{}".format(poem_id),"value":value}
	return requests.post(post_url,data=data,headers=headers).content.decode()

def get_poem_by_id(poem_id):
	poem_url = "https://so.gushiwen.org/shiwenv_{}.aspx".format(poem_id)

	fail_count = 10
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
	while not success and fail_count>0:
		try:
			pq_poempage = pq(poempage)(".main3 .left .sons .cont")
			title = pq_poempage("h1").text()
			dynasty = pq(pq_poempage(".source a")[0]).text()
			author = pq(pq_poempage(".source a")[1]).text()
			content = pq(pq_poempage(".contson")[0]).html()
			yi = post_poem_yi_zhu_shang(poem_id,"yi")
			zhu = post_poem_yi_zhu_shang(poem_id,"zhu")
			shang = post_poem_yi_zhu_shang(poem_id,"shang")
			yizhu = post_poem_yi_zhu_shang(poem_id,"yizhu")
			yishang = post_poem_yi_zhu_shang(poem_id,"yishang")
			zhushang = post_poem_yi_zhu_shang(poem_id,"zhushang")
			yizhushang = post_poem_yi_zhu_shang(poem_id,"yizhushang")
			success = True
		except Exception as e:
			fail_count -= 1
			success = False
			print("get_poem_by_id 出现错误,错误信息:{},poem_id:{},请等待 5 秒再尝试".format(e,poem_id))
			time.sleep(5)
	if fail_count==0:
		return None
	poem = {
	"poem_id": poem_id, 
	"title": title, 
	"dynasty": dynasty, 
	"author": author, 
	"content": content, 
	"yi": yi,
	"zhu": zhu, 
	"shang": shang, 
	"yizhu":yizhu,
	"yishang":yishang,
	"zhushang":zhushang,
	"yizhushang":yizhushang
	}
	return poem

string = get_poem_by_id("12f82c602c43")["zhu"]
f = open("1.txt","w+",encoding="utf-8")
f.write(string)
f.close()
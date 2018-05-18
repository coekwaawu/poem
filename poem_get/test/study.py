#import os
#print(os.path.abspath(os.path.join(__file__, os.pardir, os.pardir,os.pardir)))
import requests
import urllib3
import re

def get(poem_id):
	url = "https://so.gushiwen.org/shiwenv_{}.aspx".format(poem_id)
	url_post = "https://so.gushiwen.org/shiwen2017/ajaxshiwencont.aspx"
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
	data = {"id":"{}".format(poem_id),"value":"zhu"}
	r = requests.post(url_post,data=data,headers=headers).content.decode()
	f=open('1.txt','w',encoding='utf-8')
	f.write(r)
	f.close()
	#return "status_code:{},\nraw:{},\ncontent:{},\ntext:{},\nheaders:{}".format(r.status_code,r.raw,r.content,r.text,r.headers)

#print(get("12f82c602c43"))

'''
string = "<p>庭户无人秋月明，夜霜欲落气先清。<br /><span style=\"color:#76621c;\">寂静的前庭空无一人，只有秋月仍旧明亮。夜里的清霜将要落下，空气中也充满了清朗的气息。<br /></span></p><p>梧桐真不甘衰谢，数叶迎风尚有声。 <br /><span style=\"color:#76621c;\">梧桐树矗立在庭前，也不甘就此衰落。树上的梧桐叶迎风摇摆，发出了些许声音。<br /></span></p><p style=\" color:#919090;margin:0px; font-size:12px;line-height:160%;\">译赏内容整理自网络（或由匿名网友上传），原作者已无法考证，版权归原作者所有。<a style=\" color:#919090; font-size:12px;\" href=\"https://www.gushiwen.org/\">本站</a>免费发布仅供学习参考，其观点不代表本站立场。站务邮箱：service@gushiwen.org</p>"
remove_copyright_pattern = re.compile("(<p style=.+?.org</p>)")
print(re.sub(pattern,"",string))
print(re.findall(pattern,string))
'''

f = open("1.txt","r",encoding="utf-8")
string = f.read()
#string = string.replace("\n","")
error_pattern = re.compile("<p>(网.+?员)")
print(string)
if len(re.findall(error_pattern,string)) > 0:
	remove_error_pattern = re.compile("(﻿<.+?.</html>)")
	#string = re.sub(remove_error_pattern,"",string)
	print(re.findall(remove_error_pattern,string,re.S))
f.close()
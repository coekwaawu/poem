from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from poem_api.models import Poem
from poem_api.models import PoemTag
import json
import math

# Create your views here.
def test(request):
	template = loader.get_template('poem_api/poem_json.html')
	return HttpResponse(template.render())

#127.0.0.1:8000/title/1
def poem_id(request, poem_title):
	return HttpResponse(Poem.objects.filter(poem_title=poem_title)[0].poem_id)

def title(request, poem_id):
	return HttpResponse(Poem.objects.filter(poem_id=poem_id)[0].title)

def dynasty(request, poem_id):
	return HttpResponse(Poem.objects.filter(poem_id=poem_id)[0].dynasty)

def author(request, poem_id):
	return HttpResponse(Poem.objects.filter(poem_id=poem_id)[0].author)

def content(request, poem_id):
	return HttpResponse(Poem.objects.filter(poem_id=poem_id)[0].content)

def yi(request, poem_id):
	return HttpResponse(Poem.objects.filter(poem_id=poem_id)[0].yi)

def zhu(request, poem_id):
	return HttpResponse(Poem.objects.filter(poem_id=poem_id)[0].zhu)

def shang(request, poem_id):
	return HttpResponse(Poem.objects.filter(poem_id=poem_id)[0].shang)

def poem(request,poem_id):
	return HttpResponse(Poem.objects.filter(poem_id=poem_id)[0])

#Example: 127.0.0.1:8000/api/1
def api(request, curPage):
	all_poem = Poem.objects.all()
	page_size = 10
	start = (curPage-1)*page_size
	end = curPage*page_size
	poems = []
	for id in range(start,end):
		poem = {"poem_id":"","title":"","dynasty":"","author":"","content":"","yi":"","zhu":"","shang":"","tags":""}
		poem["poem_id"] = all_poem[id].poem_id
		poem["title"] = all_poem[id].title
		poem["dynasty"] = all_poem[id].dynasty
		poem["author"] = all_poem[id].author
		poem["content"] = all_poem[id].content
		poem["yi"] = all_poem[id].yi
		poem["zhu"] = all_poem[id].zhu
		poem["shang"] = all_poem[id].shang
		poem["yizhu"] = all_poem[id].yizhu
		poem["yishang"] = all_poem[id].yishang
		poem["zhushang"] = all_poem[id].zhushang
		poem["yizhushang"] = all_poem[id].yizhushang
		poem_tag_rows = PoemTag.objects.filter(poem_id=poem["poem_id"])
		poem_tags=[]
		for row in poem_tag_rows:
			poem_tags.append(row.tag_name)
		poem["tags"] = poem_tags
		poems.append(poem)
	total = all_poem.count()
	pageCount = math.ceil(total/page_size)
	dictionary = {"total":total,"pageCount":pageCount,"curPage":curPage,"rows":poems}
	json_resp = json.dumps(dictionary,ensure_ascii=False)
	response = HttpResponse(json_resp,content_type="application/json")
	response["Access-Control-Allow-Origin"] = "*"
	response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
	response["Access-Control-Max-Age"] = "1000"
	response["Access-Control-Allow-Headers"] = "*"
	return response



import sys
sys.path.append("..")
from get_poem_by_url import get_poem_by_url

if __name__=="__main__":
	target_urls = ["https://www.gushiwen.org/shiwen/default_0A0A{}.aspx".format(i) for i in range(1,11)]
	for target_url in target_urls:
		get_poem_by_url(target_url)
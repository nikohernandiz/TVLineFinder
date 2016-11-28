import requests
import logging

def downloadRedditUrl(url):
	print "downloadRedditUrl(): Downloading url: {}".format(url)
  
	headers = {
    		'TVLineFinder searching...
	}
	r = requests.get(url,headers = headers)
	if r.status_code != 200:
		raise Exception("Error: {}".format(r.status_code))
	return r.text	

#Find the TV Line in post
def parseRedditPost(html):	
	bs = BeautifulSoup(html)
	return bs.select('div.usertext-body')[1].text

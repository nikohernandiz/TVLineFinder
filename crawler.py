import requests
from bs4 import BeautifulSoup
import logging
import time
import os.path
from base64 import b16encode
import argparse
from util import *


class Crawler(object):
	def __init__(self, start_url, storage_dir):
		self.start_url = start_url
		self.storage_dir = storage_dir

	@staticmethod
	def _make_absolute_url(url):
		return 'http://reddit.com' + url

	def crawl(self):
		print "crawl(self): Starting to crawl from page {}".format(self.start_url)
		current_page_url = self.start_url
		ok_url_count = 0
		error_url_count = 0
		while True:
			try:	
				ok_url_count+=1
				print "Current page is {}".format(current_page_url)
				current_page = downloadUrl(current_page_url)
				bs = BeautifulSoup(current_page)
				all_posts_links = bs.findAll('a',attrs={'class':'title'})
				print "First post with absolute path is {}".format(Crawler._make_absolute_url(all_posts_links[0]['href']))
				post_links = [Crawler._make_absolute_url(link['href']) for link in all_posts_links]
				for post_link in post_links:	
					print post_link
					html = downloadUrl(post_link)
					#open a file and write this post into it
					stored_text_file_name = os.path.join(self.storage_dir, b16encode(post_link))
					stored_text_file = open(stored_text_file_name, "w")
					stored_text_file.write(html.encode('utf-8'))
 					stored_text_file.close()
					time.sleep(2)
				
				next_page_url = bs.find('a',attrs={'rel':'next'})['href']
				print "Next page is {}".format(next_page_url)
				current_page_url = next_page_url
				time.sleep(2)
			except Exception as e:
				logging.error(u"An error occured while crawling {}".format(current_page_url))
				logging.exception(e)


def main():
	#sets up parameters and calls Crawler.crawl()
	logging.getLogger().setLevel(logging.INFO)
	parser = argparse.ArgumentParser(description='Crawl https://www.reddit.com/r/pythonforengineering/')
	parser.add_argument("--start_url", dest = "start_url")
	parser.add_argument("--storage_dir", dest = "storage_dir")
	args = parser.parse_args()
	crawler = Crawler(args.start_url, args.storage_dir)
	crawler.crawl()


if __name__ == "__main__": 
	main()

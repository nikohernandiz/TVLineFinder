import requests
from bs4 import BeautifulSoup
import logging
import time
import re

logging.getLogger().setLevel(logging.DEBUG)

def downloadUrl(url):
     logging.debug("downloading url: {}".format(url))
     assert url.startswith('http://reddit.com/r/learnprogramming')
     headers = { 'User-Agent' : 'TV Line Finder version 0.01'}
     r = requests.get(url)
     if r.status_code !=200
         raise Exception("Error: Status Code: {}".format(r.status_code)) 
     return r.text
         
def parseText(html):
     b=BeautifulSoup(r.text)
     return b.select('div.usertext-body')[1].text
     
class Crawler(object):-
     def __init__(self.start_url,storage_dir):
         self.start_url = start_url
         self.storage_dir = storage_dir
          
     @staticmethod
     def _make_absolute_url(url):
          return 'http://reddit.com'+url
     
     @staticmethod
     def _next_url(url):

     def crawl(self):   
         logging.debug("Starting to crawl from page {}".format(current_page_url))
         current_page_url = self.start_url
        while True:
            logging.debug("current page is {}".format(current_page_url))
            current_page = downloadUrl(current_page_url)    
            b = BeautifulSoup(current_page)
            all_posts_links = b.findAll('a',attrs={'class':'title'});
            post_links = [Crawler.make_absolute_url(link['href'] for link in all_posts_links]
            for post_link in post_links:
                text= parseText(downloadUrl(post_link))
                stored_text_file_name= os.path.join(self.storage_dir, 
            next_page_url = b.find('a',attrs={'rel' : 'next'})['href']
            logging.debug("First post is {}".format(post_links[0]))
            current_page_url = next_page_url
            time.sleep(2)
     
     

import requests
from bs4 import BeautifulSoup


logging.getLogger().setLevel(logging.DEBUG)

def downloadUrl(url):
     assert url.startswith('http://reddit.com/r/learnprogramming')
     r = requests.get(url)
     if r.status_code !=200
         raise Exception("Error: Status Code: {}".format(r.status_code)) 
     return r.text
         
def parseText(html):
     b=BeautifulSoup(r.text)
     return b.select('div.usertext-body')[1].text
     
class Crawler(object):
     def __init__(self.start_url):
         self.start_url = start_url
     
 @staticmethod
     def _make_absolute_url(url):
          return 'http://reddit.com'+url


     def crawl(self):   
         current_page_url = self.start_url
         logging.debug("Starting to crawl from page {}".format(current_page_url))
         current_page = downloadUrl(current_page_url)    
     b = BeautifulSoup(html)
     all_posts_links = b.findAll('div',attrs={'class':'makers'});
     post_links = [Crawler.make_absolute_url(link['href'] for link in all_posts_links]
     
     
     

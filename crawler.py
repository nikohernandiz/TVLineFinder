import requests
from bs4 import BeautifulSoup

def downloadUrl(url):
     r = requests.get(url)
     if r.status_code !=200
         raise Exception("Error: Status Code: {}".format(r.status_code)) 
     return r.text
         
def parseText(html):
     b=BeautifulSoup(r.text)
     return b.select('div.usertext-body')[1].text
     

from urllib.request import urlopen

#ALT_URL = "https://en.wikiquote.org/wiki/Archer_(season_1)/"
CURRENT_URL = "http://www.imdb.com/title/tt1486217/quotes/"
CURRENT_HOME = "http://www.imdb.com/"

try:
    import config
    USERAGENT = config.agent
    APP_ID = config.username
    APP_SECRET = config.password
except ImportError:
    pass
	
#kb = [] 
initKB = {}

def main(): 
    print("Getting quotes from IMDb")
#	kb.append(parseSource():)
	
def getHTMLpage(url):
	c=urlopen(url)
	contents=c.read()
	return contents

def parsePage(show):
	contents=getHTMLpage(show)
	split_contents=contents.split('<h2>Cast</h2>')[1].split('\n')
	cast_html_elements=filter(lambda x: x.find('class="character" character="name"') is not -1,split_contents)
	filtered_elements=filter(lambda x: x.find("/company/") is -1,cast_html_elements)
	chars=map(lambda x:x.split('itemprop="name"')[1][1:-7],filtered_elements)
	return chars
	
def buildKB(N):
	print ("KB initiating...")
	showList = parseSource()
	#finding the next tv show needs implementing	
def parseSource():
	page_contents=getHTMLpage(CURRENT_HOME)
	split_contents=page_contents.split('\n')
	html_elements_with_MovieNames=filter(lambda x: x.find("titleColumn") is not -1,split_contents)
	media=map(lambda x : (x.split('"')[6][2:-17],x.split('"')[3]), html_elements_with_MovieNames)
	return parsePage(media)


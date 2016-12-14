
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
	c=urllib2.urlopen(url)
	contents=c.read()
	return contents

def parsePage(show):
	contents=getHTMLpage(show)
	split_contents=contents.split('<h2>Cast</h2>')[1].split('\n')
	cast_html_elements=filter(lambda x: x.find('class="character" character="name"') is not -1,split_contents)
	filtered_elements=filter(lambda x: x.find("/company/") is -1,cast_html_elements)
	cast=map(lambda x:x.split('itemprop="name"')[1][1:-7],filtered_elements)
	return cast
	
def buildKB(N):
	print ("KB initiating...")
	movie_tuples=parse_SeedUrl()
	for movie_id in range(N):
		getCast(movie_tuples[movie_id])
	#finds the the next show 	
def parseSource():
	page_contents=getHTMLpage(CURRENT_HOME)
	split_contents=page_contents.split('\n')
	html_elements_with_MovieNames=filter(lambda x: x.find("titleColumn") is not -1,split_contents)
	media=map(lambda x : (x.split('"')[6][2:-17],x.split('"')[3]), html_elements_with_MovieNames)
	return media


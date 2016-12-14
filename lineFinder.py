import sqlite3
import time
import traceback
import praw
import random
import json
import urllib.request 


#These files must be in the same folder
try:
    import config
    import kbcrawler
except ImportError:
    Print("Import Failed, make sure configuration files and crawler are in same directory")
    pass
	



USERAGENT = "whoslineisthatArcher 0.2 /u/ceffocoyote"
SUBREDDIT = "pythonforengineers"
CURRENT_URL = "http://www.imdb.com/title/tt1486217/quotes"
CURRENT_HOME = "http://www.imdb.com/"
DICTFILE = 'kb.txt'
RESULTFORM = ('TVquote+"  "+TVsource')
MULTIPLE_MATCHES = True
MAXPOSTS = 100 
USERAGENT = config.agent
APP_ID = config.username
APP_SECRET = config.password
APP_URI = "https://127.0.0.1:65010/authorize_callback"
APP_REFRESH = "60"

with open(DICTFILE,'r') as f:
    DICT = json.loads(f.read())
#Moves list from .txt to .db for queries
sql = sqlite3.connect('sql.db')
print('Loaded SQL Database')
cur = sql.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS oldposts(ID TEXT)')
cur.execute('CREATE INDEX IF NOT EXISTS oldpost_index ON oldposts(id)')
print('Loaded Completed table')

sql.commit()

r = praw.Reddit(USERAGENT)
r.set_oauth_app_info(APP_ID, APP_SECRET, APP_URI)
r.refresh_access_information(APP_REFRESH)

if r.has_scope('identity'):
    USERNAME = r.user.name.lower()
else:
    USERNAME = ''

def levenshtein(s1, s2):

    if len(s1) < len(s2):
        return levenshtein(s2, s1)
 
    if len(s2) == 0:
        return len(s1)
    else:
        previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return previous_row[-1]



def typosearch(comment, tolerance= 3):
#Levenshtein Algorithm used here for inaccurate quotes
    list = []
    checked = []
    for lineQuote in DICT:
        itemlength = len(lineQuote.split())
        pos = 0
        commentsplit = comment.split()
        end = False
        while not end:
            try:
                gram = commentsplit[pos:pos+itemlength]
                gramjoin = ' '.join(gram)
                lev = levenshtein(lineQuote, gramjoin)
                if lev <= tolerance:
                    if lineQuote not in checked:
                        checked.append(lineQuote)
                        list = RESULTFORM
                        list = list.replace('TVquote', lineQuote)
                        list = list.replace('TVsource', get_response(lineQuote))
                        list.append(list)
                        if MULTIPLE_MATCHES is False:
                            return list
                pos += 1
                if pos > len(commentsplit):
                    end = True
            except IndexError:
                end = True
    return list

def quicksearch(comment):
#In case the Levenshtein search algorithm becomes problematic 
    list = []
    for lineQuote in DICT:
        if lineQuote.lower() in comment.lower():
            list = RESULTFORM
            list = list.replace('TVquote', lineQuote)
            list = list.replace('TVsource', get_response(lineQuote))
            list.append(list)
            if MULTIPLE_MATCHES is False:
                return list
    return list

def get_response(key):
    value = DICT[key]
    if isinstance(value, list):
        return random.choice(value)
    return value

def TVlineFinder():
    print('Searching '+ SUBREDDIT + '.')
    subreddit = r.get_subreddit(SUBREDDIT)
    posts = subreddit.get_comments(limit=MAXPOSTS)
    for post in posts:
        results = []
        pid = post.id

        if re.search("!whoselineisthat", submission.title, re.IGNORECASE):
            continue
        try:
            pauthor = post.author.name.lower()
        except AttributeError:
            continue
        #Prevents replying to self
        if pauthor == USERNAME:
            continue
        #SQL commands here
        cur.execute('SELECT * FROM oldposts WHERE ID == ?', [pid])
        if cur.fetchone():
            # Already in database
            continue

        cur.execute('INSERT INTO oldposts VALUES(?)', [pid])
        sql.commit()
		#Checks users comment body for TVlines
        pb = post.body.lower()
        results = typosearch(pb)
        #results = quicksearch(pb)

        if len(results) == 0:
            continue

        newcomment = 'I check where tv quotes come from and I found atleast one in that parent comment'
        newcomment += '\n\n' + '\n\n'.join(results) + '\n\n'
        newcomment += 'Call me when you want to identify more lines!'

        note = 'Replying to {id} by {author} with {count} items'
        note = note.format(id=pid, author=pauthor, count=len(results))
        print(note)

        post.reply(newcomment)

#This prevents Reddit from thinking the AI is a spambot
while True:
    try:
        TVlineFinder()
    except Exception as e:
        traceback.print_exc()
    print('Anti-ban waiting...')
    sql.commit()
    time.sleep(60)

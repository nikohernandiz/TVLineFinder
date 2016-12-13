import sqlite3
import time
import traceback
import praw
import random
import json

APP_ID = "sNJ0ODPHsl6sNw"
APP_SECRET = "2d8tpkojQIQ5UwnGWMGfvP4ukk0"
APP_URI = "https://127.0.0.1:65010/authorize_callback"
APP_REFRESH = "60"

USERAGENT = "whoslineisthatArcher 0.2 /u/ceffocoyote"
#This is a short description of what the bot does. For example "/u/GoldenSights' Newsletter bot"
SUBREDDIT = "pythonforengineers"
#This is the sub or list of subs to scan for new posts. For a single sub, use "sub1". For multiple subreddits, use "sub1+sub2+sub3+..."

COMMENTHEADER = "I found a tv line in that comment"
COMMENTFOOTER = "Call me when you want to identify more lines!"
#These can be blank if you don't want them.

DICTFILE = 'kb.txt'

RESULTFORM = (TVquote+"  "+TVsource)
#This is the form that the result will take
#You may use _key_ and _value_ to inject the key/value from the dict.
#This preset will create a link where the text is the snake name and the url is the wiki link
#You may delete one or both of these injectors.

KEYAUTHORS = []
# These are the names of the authors you are looking for
# The bot will only reply to authors on this list
# Keep it empty to allow anybody.

MULTIPLE_MATCHES = True
# If True, the comment will respond to multiple keywords within the comment.
# Using snakes.txt as an example, True means that we will link multiple snake URLs if
# the comment contained multiple snake names.
# If False, only keep the first generated response. Because dictionaries are unordered,
# there is no guarantee which one will be picked.

LEVENMODE = True
#If this is True it will use a function that is slow but can find misspelled keys
#If this is False it will use a simple function that is very fast but can only find keys which are spelled exactly

MAXPOSTS = 100
#This is how many posts you want to retrieve all at once. PRAW can download 100 at a time.
WAIT = 30
#This is how many seconds you will wait between cycles. The bot is completely inactive during this time.



try:
    import bot
    USERAGENT = bot.ag
    APP_ID = bot.username
    APP_SECRET = bot.password
except ImportError:
    pass


with open(DICTFILE,'r') as f:
    DICT = json.loads(f.read())

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
    #This method compares similiar strings so if the user is not 100% accurate the result can still be found
    #http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
 
    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)
 
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



def findsuper(comment, tolerance= 3):
#checks the knowledge base for any tv lines in the users comments with levenshtein for spelling
    list = []
    checked = []
    for itemname in DICT:
        itemlength = len(itemname.split())
        pos = 0
        commentsplit = comment.split()
        end = False
        while not end:
            try:
                gram = commentsplit[pos:pos+itemlength]
                gramjoin = ' '.join(gram)
                lev = levenshtein(itemname, gramjoin)
                if lev <= tolerance:
                    if itemname not in checked:
                        checked.append(itemname)
                        list = RESULTFORM
                        list = list.replace('TVquote', itemname)
                        list = list.replace('TVsource', get_response(itemname))
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
#checks the kb simply, quotes must not have spelling errors
    list = []
    for itemname in DICT:
        if itemname.lower() in comment.lower():
            list = RESULTFORM
            list = list.replace('TVquote', itemname)
            list = list.replace('TVsource', get_response(itemname))
            list.append(list)
            if MULTIPLE_MATCHES is False:
                return list
    return list

def get_response(key):
    value = DICT[key]
    if isinstance(value, list):
        return random.choice(value)
    return value

def ie():
    print('Searching '+ SUBREDDIT + '.')
    subreddit = r.get_subreddit(SUBREDDIT)
    posts = subreddit.get_comments(limit=MAXPOSTS)
    for post in posts:
        results = []
        pid = post.id

        try:
            pauthor = post.author.name.lower()
        except AttributeError:
            continue

        if KEYAUTHORS != [] and all(keyauthor != pauthor for keyauthor in KEYAUTHORS):
            continue

        if pauthor == USERNAME:
            # Will not reply to self
            continue

        cur.execute('SELECT * FROM oldposts WHERE ID == ?', [pid])
        if cur.fetchone():
            # Already in database
            continue

        cur.execute('INSERT INTO oldposts VALUES(?)', [pid])
        sql.commit()
        pbody = post.body.lower()
        
        if LEVENMODE is True:
            results = findsuper(pbody)
        else:
            results = quicksearch(pbody)

        if len(results) == 0:
            continue

        newcomment = COMMENTHEADER
        newcomment += '\n\n' + '\n\n'.join(results) + '\n\n'
        newcomment += COMMENTFOOTER

        note = 'Replying to {id} by {author} with {count} items'
        note = note.format(id=pid, author=pauthor, count=len(results))
        print(note)

        post.reply(newcomment)

#This prevents Reddit from thinking the AI is a spambot
while True:
    try:
        ie()
    except Exception as e:
        traceback.print_exc()
    print('Running again in %d seconds \n' % WAIT)
    sql.commit()
    time.sleep(WAIT)

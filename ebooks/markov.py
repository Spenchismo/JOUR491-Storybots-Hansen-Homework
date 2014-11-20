from db import Db
from gen import Generator
from parse import Parser
from sql import Sql
from rnd import Rnd
from twython import Twython
import time, string
import random
import sys
import sqlite3
import codecs

API_KEY = #api key in single quotes
API_SECRET = #api secret in single quotes
ACCESS_TOKEN = #access token in single quotes
ACCESS_TOKEN_SECRET = #access token secret in single quotes

twitter = Twython(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

SENTENCE_SEPARATOR = '.'
WORD_SEPARATOR = ' '

if __name__ == '__main__':
    args = sys.argv
    usage = 'Usage: %s (parse <name> <depth> <path to txt file>|gen <name> <count>)' % (args[0], )

    if (len(args) < 3):
        raise ValueError(usage)

    mode  = args[1]
    name  = args[2]
    
    if mode == 'parse':
        if (len(args) != 5):
            raise ValueError(usage)
        
        depth = int(args[3]) #controls insanity level of tweets
        file_name = args[4]
        
        db = Db(sqlite3.connect(name + '.db'), Sql())
        db.setup(depth)
        
        txt = codecs.open(file_name, 'r', 'utf-8').read()
        Parser(name, db, SENTENCE_SEPARATOR, WORD_SEPARATOR).parse(txt)
    
    elif mode == 'gen':
        count = int(args[3])
        db = Db(sqlite3.connect(name + '.db'), Sql())
        generator = Generator(name, db, Rnd())
        for i in range(0, count):
            markovs = generator.generate(WORD_SEPARATOR)
            markovs = markovs.split("\n")
            potentialtweets = []
            for mark in markovs:                
                potentialtweets.append(mark)
            tweets = []
            for tw in potentialtweets:
                if len(tw)<140:
                    if len(tw) != 0:
                        tweets.append(tw)
                    else:
                        pass
                    #this will limit generated tweets to 140 characters or less. If over 140, it'll skip it.
                    if len(tw)<3:
                        pass
                    #if it's less than 3 characters, it won't shoot off a tweet
                    else:
                        continue
                else:
                    pass
            try:    
                tweet=random.choice(tweets)
                print tweet
                twitter.update_status(status=tweet)
                time.sleep(5) #sleeps 5 seconds to avoid hitting API spam cap on Twitter
            except:
                continue
    else:
        raise ValueError(usage)
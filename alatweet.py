#!/usr/bin/python

from time import sleep
from serial import Serial
from twitter import Twitter
import string
import textwrap
import re
import sys

class HashTagDisplay():
    def __init__(self, delay=5, debug=False):
        # duration in seconds to allow human to read display
        self.delay = delay
        # print messages to shell for debugging 
        self.debug = debug
        self.ser = Serial('/dev/ttyS0', baudrate=9600, timeout=1)

    def search(self, hashtag):
           # search for tweets with specified hashtag
           twitter_search = Twitter(domain="search.twitter.com")
           return twitter_search.search(q=hashtag)
    
    def display(self, results):
           # Display each tweet in the twitter search results
           for tweet in results.get('results'):
               msg = "@" + tweet.get('from_user') + ": " + tweet.get('text')
               #http://stackoverflow.com/questions/8689795/python-remove-non-ascii-characters-but-leave-periods-and-spaces
               msg = filter(lambda x: x in string.printable, msg)
               msg = re.sub('\s+',' ', msg)
               if self.debug == True:
                   print "msg: [" + msg + "]"
               for c in msg:
                   self.ser.write(c)
                   sleep(0.01)
               self.ser.write('\n');
               sleep(self.delay)

# following is executed when this script is run from the shell
if __name__ == '__main__':
    # use argument to specify twitter hashtag to search and display
    if len(sys.argv) < 2:  
        sys.exit("usage: " + sys.argv[0] + " <hash-tag>")
    hashtag = sys.argv[1]
    hashTagDisplay = HashTagDisplay(debug=True)
   # repeat twitter search and display forever
    while True:
        results = hashTagDisplay.search(hashtag)
        hashTagDisplay.display(results)


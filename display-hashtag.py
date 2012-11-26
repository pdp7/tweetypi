#!/usr/bin/python
# Author: Drew Fustini
# Target: Raspberry Pi
# Desc: display tweets for a given hashtag on char LCD

from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
from twitter import Twitter
import textwrap
import re
import sys

class HashTagDisplay():
    def __init__(self, hashtag, cols=16, rows=2, delay=3, debug=False):
        self.lcd = Adafruit_CharLCD()
        self.cols = cols
        self.rows = rows
        self.delay = delay
        self.debug = debug
        #note: tweet display loop is hardcoded for 2 rows
        self.lcd.begin(cols, rows)

    def search(self, hashtag):
           # search for tweets with specified hashtag
           print hashtag
           twitter_search = Twitter(domain="search.twitter.com")
           return twitter_search.search(q=hashtag)
    
    def display(self, results):
           # Display each tweet in the twitter search results
           for tweet in results.get('results'):
               msg = "@" + tweet.get('from_user') + ": " + tweet.get('text') 
               if self.debug == True:
                   print "msg: " + msg
               # break tweet into lines the width of LCD
               lines = textwrap.wrap(msg, self.cols)
               self.printLines(lines)

    def printLines(self, lines):
               # display each line of the tweet
               i = 0
               while i < lines.__len__():
                   self.lcd.clear()
                   # I added short delay after every LCD command
                   # as I found intermittement issue where
                   # eventually the LCD would start displaying
                   # random "garbage" characters.  This stopped
                   # occuring after adding the delay
                   sleep(0.2)

                   # display line on first row
                   self.lcd.message(lines[i])
                   sleep(0.2)
                   i=i+1

                   # no more lines remaining for this tweet
                   if i >= lines.__len__():
                      sleep(3)
                      break

                   # move cursor to the next LCD row
                   self.lcd.message("\n")
                   sleep(0.2)

                   # display line on second row
                   self.lcd.message(lines[i])
                   sleep(0.2)
                   i=i+1

                   # pause to allow human to read displayed rows
                   sleep(self.delay)


# following is executed when this script is run from the shell
if __name__ == '__main__':
    # use argument to specify twitter hashtag to search and display
    if len(sys.argv) < 2:  
        sys.exit("usage: " + sys.argv[0] + " <hash-tag>")
    hashtag = sys.argv[1]
    hashTagDisplay = HashTagDisplay(hashtag, debug=True)
    # repeat twitter search and display forever
    while True:
        results = hashTagDisplay.search(hashtag)
        hashTagDisplay.display(results)

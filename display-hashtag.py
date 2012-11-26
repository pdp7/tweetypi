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
    def __init__(self, hashtag, cols=16, rows=2):
        self.lcd = Adafruit_CharLCD()
        self.cols = cols
        self.rows = rows
        #note: tweet display loop is hardcoded for 2 rows
        self.lcd.begin(cols, rows)

    def search(self):
           # search for tweets with specified hashtag
           twitter_search = Twitter(domain="search.twitter.com")
           self.results = twitter_search.search(q=hashtag)
    
    def display(self):
           # Display each tweet in the twitter search results
           for tweet in self.results.get('results'):

               msg = "@" + tweet.get('from_user') + ": " + tweet.get('text') 
               print "msg: " + msg
   
               # break tweet into lines the width of LCD
               lines = textwrap.wrap(msg, self.cols)

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
                   sleep(3)

    def run(self):
       # repeat twitter search and results display loop forever
       print "run"
       self.search()
       self.display()



# following is executed when this script is run from the shell
if __name__ == '__main__':
    # use argument to specify twitter hashtag to search and display
    if len(sys.argv) < 2:  
        sys.exit("usage: " + sys.argv[0] + " <hash-tag>")
    hashtag = sys.argv[1]
    hashTagDisplay = HashTagDisplay(hashtag)
    hashTagDisplay.run()

#!/usr/bin/python
# Author: Drew Fustini
# Target: Raspberry Pi
# Desc: display tweets for a given hashtag on char LCD; released a public domain
# Blog post: http://www.element14.com/community/groups/raspberry-pi/blog/2012/11/26/display-tweets-on-a-character-lcd

from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
from twitter import Twitter
import textwrap
import re
import sys

class HashTagDisplay():
    def __init__(self, hashtag, cols=16, rows=2, delay=3, debug=False):
        # number of columns on the character LCD (min: 16, max: 20)
        self.cols = cols
        # number of rows on the character LCD (min: 1, max: 4)
        self.rows = rows
        # duration in seconds to allow human to read LCD lines
        self.delay = delay
        # print messages to shell for debugging 
        self.debug = debug
        self.lcd = Adafruit_CharLCD()
        self.lcd.begin(cols, rows)

    def search(self, hashtag):
        """ search for tweets with specified hashtag """
        twitter_search = Twitter(domain="search.twitter.com")
        return twitter_search.search(q=hashtag)
    
    def display(self, results):
        """ Display each tweet in the twitter search results """
        for tweet in results.get('results'):
            msg = "@" + tweet.get('from_user') + ": " + tweet.get('text') 
            if self.debug == True:
                print "===================="
                print "msg: " + msg
            # break tweet into lines the width of LCD
            lines = textwrap.wrap(msg, self.cols)
            self.printLines(lines)

    def printLines(self, lines):
        """ display each line of the tweet """
        i = 0
        while i < lines.__len__():
            self.lcd.clear()
            # I added short delay after every LCD command
            # as I found intermittement issue where
            # eventually the LCD would start displaying
            # random "garbage" characters.  This stopped
            # occuring after adding the delay
            sleep(0.2)
                
            if self.debug == True:
                print "--------------------"

            # print line to each LCD row 
            for row in range(self.rows):
                # move cursor to the next LCD row
                #self.lcd.message("\n")
                self.lcd.setCursor(0,row)
                sleep(0.2)
                       
                # display line on current LCD row
                print lines[i]
                self.lcd.message(lines[i])
                sleep(0.2)
                i=i+1

                # no more lines remaining for this tweet
                if i >= lines.__len__():
                    sleep(3)
                    break

                # pause to allow human to read displayed rows
                sleep(self.delay)


# following is executed when this script is run from the shell
if __name__ == '__main__':
    # use argument to specify twitter hashtag to search and display
    if len(sys.argv) < 2:  
        sys.exit("usage: " + sys.argv[0] + " <hash-tag>")
    hashtag = sys.argv[1]
    hashTagDisplay = HashTagDisplay(hashtag, cols=16, rows=2, debug=True)
    # repeat twitter search and display forever
    while True:
        results = hashTagDisplay.search(hashtag)
        hashTagDisplay.display(results)

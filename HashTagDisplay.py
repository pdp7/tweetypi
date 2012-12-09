#!/usr/bin/python
# Author: Drew Fustini
# Target: Raspberry Pi
# Desc: display tweets for a given hashtag on char LCD; released as public domain
# Blog post: http://www.element14.com/community/groups/raspberry-pi/blog/2012/11/26/display-tweets-on-a-character-lcd

from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
from twitter import Twitter
import textwrap
import re
import sys
import argparse

class HashTagDisplay():
    def __init__(self, cols, rows, delay, debug=False):
        # number of columns on the character LCD (min: 16, max: 20)
        self.cols = cols
        # number of rows on the character LCD (min: 1, max: 4)
        self.rows = rows
        # duration in seconds to allow human to read LCD lines
        self.delay = delay
        # print messages to shell for debugging 
        self.debug = debug
        print self
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
                print "msg: " + msg
            # break tweet into lines the width of LCD
            lines = textwrap.wrap(msg, self.cols)
            self.printLines(lines)

    def printLines(self, lines):
        """ display each line of the tweet """
        i = 0
        while i < lines.__len__():
            self.lcd.clear()
                
            # print line to each LCD row 
            for row in range(self.rows):

                # display line on current LCD row
                self.lcd.setCursor(0,row)
                self.lcd.message(lines[i])
                i=i+1
                # 200ms delay is now only for visual effect
                # initially added the delay to avoid issue 
                # where garbage characters were displayed:
                # https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/pull/13
                sleep(0.2)

                # no more lines remaining for this tweet
                if i >= lines.__len__():
                    # sleep according to the number of rows displayed
                    row_delay = self.delay / float(self.rows)
                    delay = row_delay * (row+1)
                    if(delay < 1):
                        delay = 1
                    sleep(delay)
                    break

                # pause to allow human to read displayed rows
                if(row+1 >= self.rows):
                     sleep(self.delay)



def usage():
    sys.exit("usage: " + sys.argv[0] + " <hash-tag>")

# following is executed when this script is run from the shell
if __name__ == '__main__':
    # use argument to specify twitter hashtag to search and display
    parser = argparse.ArgumentParser(description='Search Twitter for hashtag and display results on LCD')
    parser.add_argument('hashtag', help='twitter hashtag to search and display (exclude "#" prefix)')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help="print debug messages to shell")
    parser.add_argument('-r', '--rows', type=int, default='2', help="number of rows on the character LCD")
    parser.add_argument('-c', '--cols', type=int, default='16', help="number of columns on the character LCD")
    parser.add_argument('-d', '--delay', type=int, default='3', help="delay in seconds to allow human to read all displayed rows")
    args = parser.parse_args()
    print args
    hashTagDisplay = HashTagDisplay(cols=args.cols, rows=args.rows, delay=args.delay, debug=args.verbose)
    # repeat twitter search and display forever
    while True:
        results = hashTagDisplay.search(args.hashtag)
        hashTagDisplay.display(results)

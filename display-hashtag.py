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

# takes command line argument for twitter hashtag to display
if len(sys.argv) < 2:  
  sys.exit("usage: tweet.py <hash-tag>")
hashtag = sys.argv[1]

# using a 16x2 character LCD
lcd_cols = 16
#note: results display loop is hardcoded for 2 rows
lcd_rows = 2
lcd = Adafruit_CharLCD()
lcd.begin(lcd_cols, lcd_rows)

# repeat twitter search and results display loop forever
while True:

    # search for tweets with specified hashtag
    twitter_search = Twitter(domain="search.twitter.com")
    results = twitter_search.search(q=hashtag)

    # Display each tweet in the twitter search results
    for tweet in results.get('results'):

        msg = "@" + tweet.get('from_user') + ": " + tweet.get('text') 
        print "msg: " + msg

        # break tweet into lines the width of LCD
        lines = textwrap.wrap(msg, lcd_cols)

        # display each line of the tweet
        i = 0
        while i < lines.__len__():
            lcd.clear()

            # I added short delay after every LCD command
            # as I found intermittement issue where
            # eventually the LCD would start displaying
            # random "garbage" characters.  This stopped
            # occuring after adding the delay
            sleep(0.2)

            # display line on first row
            lcd.message(lines[i])
            sleep(0.2)
            i=i+1

            # no more lines remaining for this tweet
            if i >= lines.__len__():
               sleep(3)
               break

            # move cursor to the next LCD row
            lcd.message("\n")
            sleep(0.2)
            # display line on second row
            lcd.message(lines[i])
            sleep(0.2)
            print lines[i]
            i=i+1
            # pause to allow human to read displayed rows
            sleep(3)

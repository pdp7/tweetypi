#!/usr/bin/python

from time import sleep
from serial import Serial
from twitter import Twitter
import string
import textwrap
import re
import sys

def checkSerial():
    ser = Serial('/dev/ttyS0', baudrate=9600, timeout=1)
    out = True
    msg = "GO BEARS!"
    n = len(msg)

    ser.write(msg);
    sleep(1);
    data = ser.read(n)
    print 'checkSerial() data:', data
    if len(data) != n:
        out = False
    else:
        out = data == msg
    return out;

class HashTagDisplay():
    def __init__(self, hashtag, cols=16, rows=2, delay=3, debug=False):
        # number of columns on the character LCD
        self.cols = cols
        # number of rows on the character LCD 
        # note: tweet display loop is hardcoded for 2 rows
        self.rows = rows
        # duration in seconds to allow human to read LCD lines
        self.delay = delay
        # print messages to shell for debugging 
        self.debug = debug
        self.ser = Serial('/dev/ttyS0', baudrate=9600, timeout=1)

    def search(self, hashtag):
           # search for tweets with specified hashtag
           print hashtag
           twitter_search = Twitter(domain="search.twitter.com")
           return twitter_search.search(q=hashtag)
    
    def display(self, results):
           # Display each tweet in the twitter search results
           for tweet in results.get('results'):
               msg = "@" + tweet.get('from_user') + ": " + tweet.get('text') + "   "
               #http://stackoverflow.com/questions/8689795/python-remove-non-ascii-characters-but-leave-periods-and-spaces
               msg = filter(lambda x: x in string.printable, msg)
               if self.debug == True:
                   print "===================="
                   print "msg: " + msg
               # break tweet into lines the width of LCD
               #lines = textwrap.wrap(msg, self.cols)
               #self.printLines(lines)
               self.ser.write(msg)
               sleep(60)

    def printLines(self, lines):
               # display each line of the tweet
               i = 0
               while i < lines.__len__():
                   #self.lcd.clear()
                   # I added short delay after every LCD command
                   # as I found intermittement issue where
                   # eventually the LCD would start displaying
                   # random "garbage" characters.  This stopped
                   # occuring after adding the delay
                   sleep(0.1)
                       
                   #if self.debug == True:
                   #       print "--------------------"

                   # print line to each LCD row 
		   for row in range(self.rows):
                       # display line on current LCD row
                       self.ser.write(lines[i]);
                       sleep(0.1)
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


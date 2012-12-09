#!/usr/bin/python
from hashtagdisplay import HashTagDisplay
import argparse

# following is executed when this script is run from the shell
if __name__ == '__main__':
    # parse arguments from the command line for the hashtag and LCD properties
    parser = argparse.ArgumentParser(description='Search Twitter for hashtag and display results on LCD')
    parser.add_argument('hashtag', help='twitter hashtag to search and display (exclude "#" prefix)')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help="print debug messages to shell")
    parser.add_argument('-r', '--rows', type=int, default='2', help="number of rows on the character LCD")
    parser.add_argument('-c', '--cols', type=int, default='16', help="number of columns on the character LCD")
    parser.add_argument('-d', '--delay', type=int, default='2', help="delay in seconds to allow human to read all displayed rows")
    args = parser.parse_args()

    hashTagDisplay = HashTagDisplay(cols=args.cols, rows=args.rows, delay=args.delay, debug=args.verbose)
    # repeat twitter search and display forever
    while True:
        # add the "#" prefix for the hashtag since "#" is comment character in shell
        results = hashTagDisplay.search("#" + args.hashtag)
        hashTagDisplay.display(results)

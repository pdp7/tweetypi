#!/usr/bin/python
import argparse

parser = argparse.ArgumentParser(description='Search Twitter for hashtag and display results on LCD')
parser.add_argument('hashtag', help='twitter hashtag to search and display (exclude "#" prefix)')
parser.add_argument('-v', '--verbose', action='store_true', help="print debug messages to shell")
parser.add_argument('-r', '--rows', type=int, default='2', help="number of rows on the character LCD")
parser.add_argument('-c', '--cols', type=int, default='16', help="number of columns on the character LCD")
parser.add_argument('-d', '--delay', type=int, default='3', help="delay in seconds to allow human to read all displayed rows")
#parser.add_argument('--sum', dest='accumulate', action='store_const',
                   #const=sum, default=max,
                   #whelp='sum the integers (default: find the max)')

args = parser.parse_args()
print args.hashtag
print args.cols
print args.delay
print args.rows
print args.verbose

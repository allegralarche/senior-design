from __future__ import print_function
import json
from pprint import pprint
import csv
from datetime import date, datetime, timedelta
import mysql.connector
import traceback
import nltk
import sys
from twokenize import tokenize
from nltk.tag.perceptron import PerceptronTagger


'''
**** USAGE ****

In README

Note: Startup takes a little while

'''

def format_tagged(tagged_list):
    out = ''
    for t in tagged_list:
        out = out + t[0] + '/' + t[1] + '/'
    out = out + '\n'
    return out

def main(argv):

    if len(sys.argv) != 3:
        print("Usage:> python getTaggedFile.py infile.txt outfile.txt")
        exit()

    infile_name = str(sys.argv[1])
    outfile_name = str(sys.argv[2])

    infile = open(infile_name, 'r')
    outfile = open(outfile_name, 'w')

    tagger = PerceptronTagger()

    print("Reading file...")
    line = infile.readline()

    while line != '':
        # Use Twokenizer for twitter parser
        tagset = None
        tokens = tokenize(line)
        tags = nltk.tag._pos_tag(tokens, tagset, tagger)
        outfile.write(format_tagged(tags))
        line = infile.readline()

    # close file and connection
    infile.close()
    outfile.close()
    print("Finished tagging... Closing files.")



if __name__ == "__main__":
    main(sys.argv[1:])
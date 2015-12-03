from __future__ import print_function
import json
from pprint import pprint
import csv
from datetime import date, datetime, timedelta
import mysql.connector
import traceback
import nltk
import sys
import re
# from twokenize import tokenize
# from nltk.tag.perceptron import PerceptronTagger


'''
**** USAGE ****

python getCFFromTagged.py inputfile.txt output.txt


'''

def identify(tagged_line):

    # CASE 1 WISH VERB FORM
    p1 = re.compile('\wish\/VB.*/', re.IGNORECASE)
    if p1.search(tagged_line) != None:
        return True

    # CASE 2 CONJUNTION NORMAL
    p2 = re.compile('\.*/CC/.*(/VBD/)|(/VBN/).*/MD/', re.IGNORECASE)
    if p2.search(tagged_line) != None:
        return True



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
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

python getTaggedFile.py inputfile.txt output.txt

Note: Startup takes a little while

'''


def is_twitter_cf_modal(word):
    w = unicode(word, errors='ignore').encode('utf-8').lower()
    if (w == 'should' or 
        w == 'should\'ve' or
        w == 'shouldve' or
        w == 'shoulda' or 
        w == 'shulda' or 
        w == 'shuda' or 
        w == 'shudda' or 
        w == 'shudve' or 
        w == 'would' or 
        w == 'would\'ve' or
        w == 'wouldve' or
        w == 'woulda' or 
        w == 'wuda' or 
        w == 'wulda' or 
        w == 'wudda' or 
        w == 'wudve' or 
        w == 'wlda' or 
        w == 'could' or 
        w == 'could\'ve' or
        w == 'couldve' or
        w == 'coulda' or 
        w == 'cudda' or 
        w == 'culda' or 
        w == 'cudve' or 
        w == 'must' or 
        w == 'mustve' or 
        w == 'might' or 
        w == 'might\'ve' or
        w == 'mightve' or 
        w == 'ought' or 
        w == 'may' or 
        w == 'i\'d' or 
        w == 'id' or 
        w == 'we\'d' or 
        w == 'youd' or 
        w == 'you\'d' or
        w == 'he\'d' or
        w == 'she\'d'):
            return True
    return False

def tag_CCJ(word):
    w = word.lower()
    '''
    as long as, even if, if, one condition that, provided (that), 
    providing (that), so long as, unless, whether... or, supposing, 
    suppose, imagine, but for
    '''
    if(w == 'as' or
        w == 'if' or
        w == 'even' or
        w == 'provided' or
        w == 'providing' or
        w == 'suppose' or
        w == 'supposing' or
        w == 'unless' or
        w == 'whether' or
        # w == 'rather' or
        w == 'envision' or
        w == 'envisioning' or
        w == 'conceptualize'or
        w == 'conceptualizing' or
        w == 'conjure' or
        w == 'conjuring' or
        w == 'visualize' or
        w == 'visualizing'):
        return True
    return False


def postprocess_tag(token, tag):
    outtag = tag
    if (is_twitter_cf_modal(token)):
        outtag = 'MD'
    elif (tag_CCJ(token)):
        outtag = 'CCJ'
    return token, outtag



def format_tagged(tagged_list):
    out = ''
    for t in tagged_list:
        token, tag = postprocess_tag(t[0], t[1])
        out = out + token + '/' + tag + '/'
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
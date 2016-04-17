import sys
import nltk
import re

from nltk import pos_tag, word_tokenize, PerceptronTagger

import json
from pprint import pprint
import csv
from datetime import date, datetime, timedelta
#import mysql.connector
import traceback
import array



def pullFeatures(tagged_line, rawTweet, CF):

    sentences = tagged_line.split("','")

    features = [rawTweet, CF, 0, 0, 0, 0, 0, 0, 0]

    for sentence in sentences:
        # Check if the tweet just has if and a past tense verb
        ifMod = re.compile("('if').*('VBD'|'VBN')", re.IGNORECASE)
        if ifMod.search(tagged_line) != None and CF == "1":
            features[2] = 2

        # Check if the tweet has a model followed by if
        modIf = re.compile("('MD').*('VBD'|'VBN').*('CCJ')", re.IGNORECASE)
        if modIf.search(tagged_line) != None and CF == "1":
            features[3] = 1


        # Check if the tweet contains wish
        wish = re.compile("('wish'|'wished'|'wishing').*('VBD'|'VBN'|'VB'|MD')", re.IGNORECASE)
        if wish.search(tagged_line) != None and CF == "1":
            features[4] = 4

        # Check if the tweet has a past tense verb followed by a modal
        conjNorm = re.compile("('VBD'|'VBN').*('MD')", re.IGNORECASE)
        if conjNorm.search(tagged_line) != None and CF == "1":
            features[5] = 2

        # CASE 4 MODAL NORMAL
        modNorm = re.compile("('MD').*('VBN'|'VBD')", re.IGNORECASE)
        if modNorm.search(tagged_line) != None and CF == "1":
            features[6] = 4

        # verb inversion
        vbInv = re.compile("('were'|'had').*('VBN'|'VBD')", re.IGNORECASE)
        if vbInv.search(tagged_line) != None and CF == "1":
            features[7] = 2


        # MD have
        mdHave = re.compile("('MD').*('have')", re.IGNORECASE)
        if mdHave.search(tagged_line) != None and CF == "1":
            features[8] = 0.6

        
    return features

def main():

    tweetsFile = open('taggedTrainTweets.csv', 'r')
    POSTaggedFile = open('POSTagged.csv', 'w')
    featureFile = open('features.csv', 'w')
    tagger = PerceptronTagger()


    features = []
    for line in tweetsFile:
        split = line.split(',')
        rawTweet = split[0]
        CF = split[1].strip()
        tags = nltk.tag._pos_tag(word_tokenize(str(rawTweet)), None, tagger)
        tagStr = ""
        for tag in tags:
            tagStr = tagStr + tag[1] + " "
        POSTaggedFile.write("%s\n" % tagStr)
        features.append(pullFeatures(', '.join([str(x) for x in tags]), rawTweet, CF))
        
    featureFile.write("tweet, CF, ifMod, modIf, wish, conjNorm, modNorm, vbIn, mdHave\n")
    for tweet in features:
        featureFile.write("%s, %s, %d, %d, %d, %d, %d, %d, %d\n" % (tweet[0], tweet[1], tweet[2], tweet[3], tweet[4], tweet[5], tweet[6], tweet[7], tweet[8]))

if __name__ == "__main__":
    main()
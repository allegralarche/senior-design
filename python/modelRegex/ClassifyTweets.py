from __future__ import print_function
import json
from pprint import pprint
import csv
from datetime import date, datetime, timedelta
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import accuracy_score
import numpy
import scipy
import mysql.connector
import traceback
import nltk
import sys
import re
import array
import nltk
from nltk.tag.perceptron import PerceptronTagger
import CounterfactualMethods
# import imp
# CounterfactualMethods = imp.load_source('CounterfactualMethods', '../helpers/CounterfactualMethods.py')


'''
**** USAGE ****
python ClassifyTweets.py tweets.txt labels.txt predicted.txt tagged.txt report.txt"
'''

def main(argv):

    if len(sys.argv) != 6:
        print("Usage:> python ClassifyTweets.py tweets.txt labels.txt predicted.txt tagged.txt report.txt")
        exit()

    # Input Files
    tweetsFile = open(sys.argv[1], 'r')
    labelsFile = open(sys.argv[2], 'r')

    #Output Files
    predictedFile = open(sys.argv[3], 'w')
    taggedFile = open(sys.argv[4], 'w')
    reportFile = open(sys.argv[5], 'w')

    tagger = PerceptronTagger()
    form_num = 7

    cf_count = [[0 for x in range(form_num)] for x in range(form_num)]

    y_true = labelsFile.read().splitlines()
    y_true = [int(i) for i in y_true]

    y_pred = []

    # Output to report file to keep track of number of CFs of each form
    form_vec = []

    print("Reading file...")
    tweet = tweetsFile.readline()

    i = 0
    while tweet != '': 
        
        # Get Counterfactual form
        taggedTweet = CounterfactualMethods.get_tagged_message(tweet, tagger)
        taggedFile.write(taggedTweet)
        form = int(CounterfactualMethods.get_cf_form(taggedTweet))
        form_vec.append(form)

        # Increase counter
        cf_count[form][0] = cf_count[form][0] + 1

        if(y_true[i] == 1):
            cf_count[form][1] = cf_count[form][1] + 1

        if(form == 0):
            # write 0
            predictedFile.write('0\n')
            y_pred.append(0)

        else:
            # write 1
            predictedFile.write('1\n')
            y_pred.append(1)


        i = i + 1
        tweet = tweetsFile.readline()

    ## Report
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, thresholds = precision_recall_curve(y_true, y_pred)

    pearson_corr = scipy.stats.pearsonr(y_true, y_pred)

    count = 0
    for i in xrange(1,form_num):
        count = count + cf_count[i][0]

    reportFile.write("Identified " + str(count) + " Counterfactuals \n")
    reportFile.write("Accuracy: %0.4f \n" % accuracy)
    reportFile.write("pearson corr: %0.4f \n" % pearson_corr[0])
    reportFile.write("p-val: %0.4f \n" % pearson_corr[1])
    reportFile.write("Precision: %0.4f \n" % precision[1])
    reportFile.write("Recall: %0.4f \n" % recall[1])

    for i in xrange(1,form_num):
        c = 1
        if cf_count[i][0] != 0:
            c = float(cf_count[i][1]) / float(cf_count[i][0])
        reportFile.write("Form %d   Count: %d,  Accuracy: %0.4f \n" % (i, cf_count[i][0], c))

    reportFile.write("Incorrect predictions\n")
    reportFile.write("idx, pred, label, form\n")

    for i in xrange(len(y_true)):
        if(int(y_true[i]) != int(y_pred[i])):
            reportFile.write(str(i + 1) + "  " + str(y_pred[i]) +  "  " + str(y_true[i]) + "  " + str(form_vec[i]) + "\n")


    print("Finished tagging... Closing files.")
    print("Identified " + str(count) + " Counterfactuals")

    #Input Files
    tweetsFile.close()
    labelsFile.close()

    #Output Files
    predictedFile.close()
    taggedFile.close()
    reportFile.close()


if __name__ == "__main__":
    main(sys.argv[1:])
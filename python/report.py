from __future__ import print_function
import json
from pprint import pprint
import csv
from datetime import date, datetime, timedelta
import mysql.connector
import traceback
import nltk
import sys
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import accuracy_score


'''
**** USAGE ****

python report.py labels.txt predicted.txt

'''
def main(argv):
    if len(sys.argv) != 3:
        print("Usage:> python getTaggedFile.py labels.txt predicted.txt")
        exit()

    infile1_name = str(sys.argv[1])
    infile2_name = str(sys.argv[2])

    infile1 = open(infile1_name, 'r')
    infile2 = open(infile2_name, 'r')
    r1 = infile1.read().splitlines()
    r1 = [int(i) for i in r1]
    r2 = infile2.read().splitlines()
    r2 = [int(i) for i in r2]

    y_true = r1
    y_pred = r2
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, thresholds = precision_recall_curve(y_true, y_pred)

    print("Accuracy: %0.4f" % accuracy)
    print("Precision: %0.4f" % precision[1])
    print("Recall: %0.4f" % recall[1])

if __name__ == "__main__":
    main(sys.argv[1:])
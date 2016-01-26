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


'''
**** USAGE ****

python getTaggedFile.py inputfile.txt output.txt

Note: Startup takes a little while

'''
def main(argv):
    if len(sys.argv) != 3:
        print("Usage:> python getTaggedFile.py infile.txt outfile.txt")
        exit()

    infile1_name = str(sys.argv[1])
    infile2_name = str(sys.argv[2])

    infile1 = open(infile1_name, 'r')
    infile2 = open(infile2_name, 'r')
    r1 = read(infile1)
    print(r1)

    '''y_true = 
    y_predicted = 
    precision, recall, thresholds = precision_recall_curve(y_true, y_predicion)
    '''

if __name__ == "__main__":
    main(sys.argv[1:])
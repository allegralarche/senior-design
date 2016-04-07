from __future__ import print_function
import json
from pprint import pprint
import csv
from datetime import date, datetime, timedelta
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import accuracy_score
#import mysql.connector
import traceback
import nltk
import sys
import re
import array
# from twokenize import tokenize
# from nltk.tag.perceptron import PerceptronTagger


'''
**** USAGE ****

python getCFFromTagged.py tagged.txt labels.txt predicted.txt


'''
'''
def identify(tagged_line):

    # CASE 1 WISH VERB FORM
    p1 = re.compile('\wish\/VB.*/', re.IGNORECASE)
    if p1.search(tagged_line) != None:
        # print("p1")
        return True

    # CASE 2 CONJUNTION NORMAL
    p2 = re.compile('\.*((/CC/)|(/IN/)).*((/VBD/)|(/VBN/)|(/VB/)).*/MD/', re.IGNORECASE)
    if p2.search(tagged_line) != None:
        # print("p2")
        return True

    # CASE 3 CONJUNCTIVE CONVERSE
    p3 = re.compile('\.*/MD/.*((/CC/)|(/IN/)).*((/VBN/)|(/VBD/)|(/VB/))', re.IGNORECASE)
    if p3.search(tagged_line) != None:
        # print("p3")
        return True

    # CASE 4 MODAL NORMAL
    p4 = re.compile('\.*/MD/.*((/VBN/)|(/VBD/)|(/VB/)).*/MD/.*((/VBN/)|(/VBD/)|(/VB/))', re.IGNORECASE)
    if p4.search(tagged_line) != None:
        # print("p4")
        return True

    # CASE 6 HYPOTHETICAL NORMAL
    # Key words: rather, imagine, envision, conceptualize, conjure up, visualize
    p5 = re.compile('\.*((rather/)|(imagine/)|(envision/)|(conceptualize/)|(conjure/)|(visualize/)).*/VB.*/.*/MD/', re.IGNORECASE)
    if p5.search(tagged_line) != None:
        # print("p6")
        return True

    # CASE 6 VERB INVERSION
    p6 = re.compile('\.*((were/)|(had/)).*((/NN/)|(/NNP/)|(/NNPS/)|(/NNS/)|(/PRP.*/)).*((/VBN/)|(/VBD/)|(/VB/)).*/MD/', re.IGNORECASE)
    if p6.search(tagged_line) != None:
        # print("p7")
        return True

    # CASE 7 MODAL PREPOSITIONAL
    # p7 = "";

    # If no matches
    return False

'''

def getForm(tagged_line):


    # CASE 0 WISH VERB FORM
    # p0 = re.compile('\.*/will/MD/', re.IGNORECASE)
    # pq = re.compile('\.*\?.*')
    # if p0.search(tagged_line) != None or pq.search(tagged_line) != None:
    #     return 0


    # CASE 1 WISH VERB FORM
    p1 = re.compile('\.*(wish|wishing)/(VB.*/|JJ/)', re.IGNORECASE)
    if p1.search(tagged_line) != None:
        return 1


    # CASE 2 CONJUNTION NORMAL
    p2 = re.compile('\.*/CCJ/.*((/VBD/)|(/VBN/)).*/MD/', re.IGNORECASE)
    if p2.search(tagged_line) != None:
        return 2


    # CASE 3 CONJUNCTIVE CONVERSE
    p3 = re.compile('\.*/MD/.*/CCJ/.*((/VBN/)|(/VBD/))', re.IGNORECASE)
    if p3.search(tagged_line) != None:
        return 3

    # CASE 4 MODAL NORMAL
    p4 = re.compile('\.*/MD/.*((/VBN/)|(/VBD/)).*/MD/.*((/VBN/)|(/VBD/)|(/VB/)|(VBZ))', re.IGNORECASE)
    if p4.search(tagged_line) != None:
        return 4

    # CASE 4 MODAL NORMAL
    # p4 = re.compile('\.*/MD/.*((/VBN/)|(/VBD/)).*/MD/.*((/VBN/)|(/VBD/))', re.IGNORECASE)
    # if p4.search(tagged_line) != None:
    #    return 4


    # CASE  HYPOTHETICAL NORMAL -> now included in CCJ
    # Key words: rather, imagine, envision, conceptualize, conjure up, visualize


    # CASE 5 Should have
    p5 = re.compile('\.*/((should)|(shoulda)(shulda)|(shuda)|(shudda)|(shudve))/MD/((have)|(hve)|(ve))/(\w)*((/VBN/)|(/VBD/))', re.IGNORECASE)
    if p5.search(tagged_line) != None:
        return 5

    # CASE 6 VERB INVERSION
    p6 = re.compile('\.*((were/)|(had/)).*((/NN/)|(/NNP/)|(/NNPS/)|(/NNS/)|(/PRP.*/)).*((/VBN/)|(/VBD/)).*/MD/', re.IGNORECASE)
    if p6.search(tagged_line) != None:
        return 6

    # CASE 7 MODAL Adverb Comparative
    p7 = re.compile('\.*/MD/.*((/VBN/)|(/VBD/)|(/VB/)).*/RBR/.*/MD/.*((/VBN/)|(/VBD/)|(/VB/))', re.IGNORECASE)
    if p7.search(tagged_line) != None:
        return 7

    # If no matches
    return 0


def main(argv):

    if len(sys.argv) != 4:
        print("Usage:> python getCFFromTagged.py tagged.txt labels.txt predicted.txt")
        exit()

    infile_name = str(sys.argv[1])
    outfile_name = str(sys.argv[3])

    infile = open(infile_name, 'r')
    outfile = open(outfile_name, 'w')
    report_file = open('report.txt', 'w')
    label_file = open(str(sys.argv[2]), 'r')

    form_num = 8

    cf_count = [[0 for x in range(form_num)] for x in range(form_num)]

    y_true = label_file.read().splitlines()
    y_true = [int(i) for i in y_true]

    y_pred = []

    form_vec = []

    print("Reading file...")
    tagged_line = infile.readline()

    i = 0
    while tagged_line != '': 
        
        # Get Counterfactual form
        form = int(getForm(tagged_line))

        form_vec.append(form)

        # Increase counter
        cf_count[form][0] = cf_count[form][0] + 1

        if(y_true[i] == 1):
            cf_count[form][1] = cf_count[form][1] + 1

        if(form == 0):
            # write 0
            outfile.write('0\n')
            y_pred.append(0)

        else:
            # write 1
            outfile.write('1\n')
            y_pred.append(1)


        i = i + 1
        tagged_line = infile.readline()

    # close file and connection
    infile.close()
    outfile.close()

    ## Report
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, thresholds = precision_recall_curve(y_true, y_pred)

    count = 0
    for i in xrange(1,form_num):
        count = count + cf_count[i][0]

    report_file.write("Identified " + str(count) + " Counterfactuals \n")
    report_file.write("Accuracy: %0.4f \n" % accuracy)
    report_file.write("Precision: %0.4f \n" % precision[1])
    report_file.write("Recall: %0.4f \n" % recall[1])

    for i in xrange(1,form_num):
        c = 1
        if cf_count[i][0] != 0:
            c = float(cf_count[i][1]) / float(cf_count[i][0])
        report_file.write("Form %d   Count: %d,  Accuracy: %0.4f \n" % (i, cf_count[i][0], c))

    report_file.write("Incorrect predictions\n")
    report_file.write("idx, pred, label, form\n")

    for i in xrange(len(y_true)):
        if(int(y_true[i]) != int(y_pred[i])):
            report_file.write(str(i + 1) + "  " + str(y_pred[i]) +  "  " + str(y_true[i]) + "  " + str(form_vec[i]) + "\n")

    report_file.close()


    print("Finished tagging... Closing files.")
    print("Identified " + str(count) + " Counterfactuals")


if __name__ == "__main__":
    main(sys.argv[1:])
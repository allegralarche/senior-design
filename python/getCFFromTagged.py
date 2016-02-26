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

    # CASE 5 MODAL PREPOSITIONAL
    # Problem: can't find prepositional phrases 
    # p5 = "";

    # CASE 6 HYPOTHETICAL NORMAL
    # Key words: rather, imagine, envision, conceptualize, conjure up, visualize
    p6 = re.compile('\.*((rather/)|(imagine/)|(envision/)|(conceptualize/)|(conjure/)|(visualize/)).*/VB.*/.*/MD/', re.IGNORECASE)
    if p6.search(tagged_line) != None:
        # print("p6")
        return True

    # CASE 7 VERB INVERSION
    p7 = re.compile('\.*((were/)|(had/)).*((/NN/)|(/NNP/)|(/NNPS/)|(/NNS/)|(/PRP.*/)).*((/VBN/)|(/VBD/)|(/VB/)).*/MD/', re.IGNORECASE)
    if p7.search(tagged_line) != None:
        # print("p7")
        return True

    # If no matches
    return False


def main(argv):

    if len(sys.argv) != 3:
        print("Usage:> python getTaggedFile.py infile.txt outfile.txt")
        exit()

    infile_name = str(sys.argv[1])
    outfile_name = str(sys.argv[2])

    infile = open(infile_name, 'r')
    outfile = open(outfile_name, 'w')

    cf_count = 0

    print("Reading file...")
    tagged_line = infile.readline()

    # i = 0

    while tagged_line != '': # and i < 11:
        
        if(identify(tagged_line)):
            # write 1
            outfile.write('1\n')
            cf_count = cf_count + 1
        else:
            # write 0
            outfile.write('0\n')

        tagged_line = infile.readline()
        # i = i + 1

    # close file and connection
    infile.close()
    outfile.close()
    print("Finished tagging... Closing files.")
    print("Identified " + str(cf_count) + " Counterfactuals")



if __name__ == "__main__":
    main(sys.argv[1:])
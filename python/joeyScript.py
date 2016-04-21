from __future__ import print_function
from datetime import date, datetime, timedelta
from twokenize import tokenize
from nltk.tag.perceptron import PerceptronTagger
import mysql.connector
import json
import nltk
import traceback
import sys
import ast
import re
import array
import counterfactualMethods


def getPercents(cursor, tagger, file):
    for row in cursor:
        message = row[0]
        tagged_message = counterfactualMethods.get_tagged_message(message, tagger)
        cf_form = counterfactualMethods.get_cf_form(tagged_message)

        if cf_form != 0 and row[1] != '':
            print(row[1])
            file.write(row[1] + "\n")
        


# args: county start_time end_time
def main(argv):
    counterfactualsFile = open('counterfactuals.txt', 'w')
    queries = []
    firstYear = argv[1].split('-')[0]
    lastYear = argv[2].split('-')[0]

    for i in range(int(firstYear), int(lastYear) + 1):
        queries.append("select message, coordinates from msgs_" + str(i) + " where state='" + argv[0] + "' and created_time > '" + argv[1] + "' and created_time < '" + argv[2] + "'")


    tagger = PerceptronTagger()
    db = 'randomTwitterByCounty'
    username = 'kzembroski'


    for query in queries:
        print(query)
        cnx = mysql.connector.connect(host='127.0.0.1', port=3306, user=username, db=db)
        cursor = cnx.cursor()
        cursor.execute(query)
        getPercents(cursor, tagger, counterfactualsFile)


if __name__ == "__main__":
    main(sys.argv[1:])
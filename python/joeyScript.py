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


def getPercents(cursor, tagger):
    cf_total = 0.0
    tweet_total = 0.0
    for row in cursor:
        message = row[0]
        tagged_message = counterfactualMethods.get_tagged_message(message, tagger)
        cf_form = counterfactualMethods.get_cf_form(tagged_message)

        if cf_form != 0:
            cf_total = cf_total + 1
    
        tweet_total = tweet_total + 1
    return cf_total/tweet_total


# args: county start_time middle end_time
def main(argv):
    sql_before = "select message from msgs_2013_04 where cnty=" + argv[0] + " and created_time > '" + argv[1] + "' and created_time < '" + argv[2]"'" 
    sql_after = "select message from msgs_2013_04 where cnty=" + argv[0] + " and created_time > '" + argv[2] + "' and created_time < '" + argv[3]"'" 



    tagger = PerceptronTagger()
    db = 'randomTwitterByCounty'
    username = 'kzembroski'


    cnx = mysql.connector.connect(host='127.0.0.1', port=3306, user=username, db=db)
    cursor = cnx.cursor()
    cursor.execute(sql_before)


    print(getPercents(cursor, tagger))




    cursor = cnx.cursor()
    cursor.execute(sql_after)


    print(getPercents(cursor, tagger))

if __name__ == "__main__":
    main(sys.argv[1:])
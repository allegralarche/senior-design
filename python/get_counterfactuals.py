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



def main(argv):
    sql_after = "select message from msgs_2013_04 where created_time > '2013-04-16 00:00:00' and created_time < '2013-04-30 23:59:59' and state='MA'" 

    if len(sys.argv) != 2:
        print("Usage:> python get_counterfactuals.py outfile.txt")
        exit()

    print('Starting process...')

    tagger = PerceptronTagger()
    db = 'randomTwitterByCounty'
    username = 'kzembroski'

    print('Executing sql...')

    cnx = mysql.connector.connect(host='127.0.0.1', port=3306, user=username, db=db)
    cursor = cnx.cursor()
    cursor.execute(sql_after)

    print('Rtrieving counterfactuals...')

    cf_total = 0.0
    tweet_total = 0.0
    reg = re.compile("(boston|marathon)", re.IGNORECASE);
    for row in cursor:
        message = row[0]
        tagged_message = counterfactualMethods.get_tagged_message(message, tagger)
        cf_form = counterfactualMethods.get_cf_form(tagged_message)

        if reg.search(message) != None:
            if cf_form != 0:
                cf_total = cf_total + 1
        
            tweet_total = tweet_total + 1

        
        if tweet_total != 0:
            print(tweet_total)    
        
        if cf_total != 0:
            print("Percent Counterfactual: {}".format(cf_total/tweet_total)) 
        


    '''
    cursor.execute(sql_after)

    count_after = 0
    for row in cursor:
        message = row[0]
        tagged_message = counterfactualMethods.get_tagged_message(message, tagger)
        cf_form = counterfactualMethods.get_cf_form(tagged_message)
        cf = 0 if cf_form == 0 else 1

        if (cf == 1):
            count_after = count_after + 1

    outfile_name = str(sys.argv[1])
    outfile = open(outfile_name, 'w')
    outfile.write('Testing number of counterfactuals used in Los Angeles and Santa Barbara counties within five days leading up to and the five days following the 2014 Isla Vista Killing\n')
    outfile.write('Dates, Number of Tweets, Number of Counterfactuals, Counterfactual Percentage\n')
    outfile.write('2014/04/18 00:00:00 to 2014/04/22 23:59:59, {}, {}, {}\n'.format(limit_count, count_before, (100.0 * count_before / limit_count)))
    outfile.write('2014/04/24 00:00:00 to 2014/04/28 23:59:59, {}, {}, {}\n'.format(limit_count, count_after, (100.0 * count_after / limit_count)))
    outfile.close()
    cnx.close()
    '''

if __name__ == "__main__":
    main(sys.argv[1:])
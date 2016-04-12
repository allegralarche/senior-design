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

    limit_count = 31400
    sql_before = "select message from msgs_2014_05 where (cnty = 6037 or cnty = 6083) and created_time > '2014-05-18 00:00:00' and created_time < '2014-05-22 23:59:59' LIMIT {}".format(limit_count)
    sql_after = "select message from msgs_2014_05 where (cnty = 6037 or cnty = 6083) and created_time > '2014-05-23 00:00:00' and created_time < '2014-05-28 23:59:59' LIMIT {}".format(limit_count)

    sql_year = "select message from msgs_2014 where (cnty = 6037 or cnty = 6083) limit {}".format(limit_count * 10)

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
    cursor.execute(sql_year)

    print('Retrieving counterfactuals...')

    count_before = 0
    for row in cursor:
        message = row[0]
        tagged_message = counterfactualMethods.get_tagged_message(message, tagger)
        cf_form = counterfactualMethods.get_cf_form(tagged_message)
        cf = 0 if cf_form == 0 else 1

        if (cf == 1):
            count_before = count_before + 1

    avg_five_day_cnt = 5.0 * count_before / 365
    avg_five_day_msg_cnt = 5.0 * (limit_count * 10) / 365
    print("Average cf count for five days: {} or {} percent".format(avg_five_day_cnt, avg_five_day_cnt / avg_five_day_msg_cnt))

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
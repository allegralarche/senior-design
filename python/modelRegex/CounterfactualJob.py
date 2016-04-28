from __future__ import print_function
from datetime import date, datetime, timedelta
from twokenize import tokenize
from nltk.tag.perceptron import PerceptronTagger
import mysql.connector
import CounterfactualMethods
import json
import nltk
import traceback
import sys
import ast
import re
import array

'''
inputs: sql file
outputs: 
'''
def main(argv):

    if len(sys.argv) != 3:
    	print("Usage:> python Counterfactual_Job.py sql_query.sql outfile.csv")
    	exit()

    print('Starting process...')

    sql_file_name = str(sys.argv[1])
    outfile_name = str(sys.argv[2])

    outfile = open(outfile_name, 'w')
    sql_file = open(sql_file_name, 'r')

    tagger = PerceptronTagger()

    print("Executing query...")

    db = 'randomTwitterByCounty'
    query = sql_file.read()

    username = 'kzembroski'
    # Execute query
    # ss = mysqlMethods.executeGetSSCursor(mysqlMethods, db, query)
    cnx = mysql.connector.connect(host='127.0.0.1', port=3306, user=username, db=db)
    cursor = cnx.cursor()
    cursor.execute(query)

    print('Retrieving counterfactuals...')

    i = 0
    for result in cursor:
        message_id = result[0]
        message = format_tweet(result[1])
        cnty = result[2]
        '''
        coordinates = ast.literal_eval(result[2])
        latitude = coordinates[0]
        longitude = coordinates[1]
        '''
        tagged_message = CounterfactualMethods.get_tagged_message(message, tagger)
        cf_form = CounterfactualMethods.get_cf_form(tagged_message)
        cf = 0 if cf_form == 0 else 1

        if(i % 10000 == 0):
            sys.stdout.write("\r%d results finished..." % i)
            sys.stdout.flush()
        
        s_out = str(message_id) + ", "  + str(cnty) + ", " + str(cf) + ", " + str(cf_form) + "\n"
        outfile.write(s_out)

        i = i + 1

    outfile.close()



if __name__ == "__main__":
    main(sys.argv[1:])

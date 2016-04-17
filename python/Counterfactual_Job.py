from __future__ import print_function
from datetime import date, datetime, timedelta
from twokenize import tokenize
from nltk.tag.perceptron import PerceptronTagger
import mysql.connector
# import mysqlMethods
import json
import nltk
import traceback
import sys
# import urllib
import ast
# import urllib2
import re
import array





def get_tagged_message(message, tagger):
    tagset = None
    formatted_message = format_tweet(message)
    tokens = tokenize(formatted_message)
    tags = nltk.tag._pos_tag(tokens, tagset, tagger)
    return format_tagged(tags)


def get_cf_form(tagged_message):

    # Filter out questions
    pq = re.compile('\.*/\?/.', re.IGNORECASE)
    if pq.search(tagged_message) != None:
        return 0

    # CASE 1 WISH VERB FORM
    p1 = re.compile('\.*(wish|wishing)/((VB.*/)|(JJ/))', re.IGNORECASE)
    if p1.search(tagged_message) != None:
        return 1


    # CASE 2 CONJUNTION NORMAL
    p2 = re.compile('\.*/CCJ/.*((/VBD/)|(/VBN/)).*/MD/', re.IGNORECASE)
    if p2.search(tagged_message) != None:
        return 2


    # CASE 3 CONJUNCTIVE CONVERSE
    p3 = re.compile('\.*/MD/.*/CCJ/.*((/VBN/)|(/VBD/))', re.IGNORECASE)
    if p3.search(tagged_message) != None:
        return 3


    # CASE 5 Should have
    p4 = re.compile('\.*/((should\'ve)/MD/)|(((should)|(shoulda)(shulda)|(shuda)|(shudda)|(shudve))/MD/((have)|(hve)|(ve))/)(\w)*((/VBN/)|(/VBD/))', re.IGNORECASE)
    if p4.search(tagged_message) != None:
        return 4

    # CASE 6 VERB INVERSION
    p5 = re.compile(("\.*(had/(\w)*/(\w)*((/NN/)|(/NNP/)|(/NNPS/)|(/NNS/)|(/PRP/)).*((/VBN/)|(/VBD/)).*/MD/)"
                    "|(were/(\w)*/(\w)*((/NN/)|(/NNP/)|(/NNPS/)|(/NNS/)|(/PRP/)).*/MD/)"
                    "|(/MD/.*/VB.*/had/(\w)*/(\w)*((/NN/)|(/NNP/)|(/NNPS/)|(/NNS/)|(/PRP/)).*((/VBN/)|(/VBD/)))"), re.IGNORECASE)
    if p5.search(tagged_message) != None:
        return 5


    # CASE 6 MODAL NORMAL
    p6 = re.compile('\.*/MD/.*((/VBN/)|(/VBD/)).*/MD/.*((/VBN/)|(/VBD/)|(/VB/)|(VBZ))', re.IGNORECASE)
    if p6.search(tagged_message) != None:
        return 6

    # If no matches
    return 0

def is_twitter_cf_modal(word):
    w = unicode(word, errors='ignore').encode('utf-8').lower()
    if (w == 'should' or 
        w == 'should\'ve' or
        w == 'shouldve' or
        w == 'shoulda' or 
        w == 'shulda' or 
        w == 'shuda' or 
        w == 'shudda' or 
        w == 'shudve' or 
        w == 'would' or 
        w == 'would\'ve' or
        w == 'wouldve' or
        w == 'woulda' or 
        w == 'wuda' or 
        w == 'wulda' or 
        w == 'wudda' or 
        w == 'wudve' or 
        w == 'wlda' or 
        w == 'could' or 
        w == 'could\'ve' or
        w == 'couldve' or
        w == 'coulda' or 
        w == 'cudda' or 
        w == 'culda' or 
        w == 'cudve' or 
        w == 'must' or 
        w == 'mustve' or 
        w == 'might' or 
        w == 'might\'ve' or
        w == 'mightve' or 
        w == 'ought' or 
        w == 'may' or 
        w == 'i\'d' or 
        w == 'id' or 
        w == 'we\'d' or 
        w == 'youd' or 
        w == 'you\'d' or
        w == 'he\'d' or
        w == 'she\'d'):
            return True
    return False

def tag_CCJ(word):
    w = word.lower()
    '''
    as long as, even if, if, one condition that, provided (that), 
    providing (that), so long as, unless, whether... or, supposing, 
    suppose, imagine, but for
    '''
    if(w == 'as' or
        w == 'if' or
        w == 'even' or
        w == 'provided' or
        w == 'providing' or
        w == 'suppose' or
        w == 'supposing' or
        w == 'unless' or
        w == 'whether' or
        # w == 'rather' or
        w == 'envision' or
        w == 'envisioning' or
        w == 'conceptualize'or
        w == 'conceptualizing' or
        w == 'conjure' or
        w == 'conjuring' or
        w == 'visualize' or
        w == 'visualizing'):
        return True
    return False


def postprocess_tag(token, tag):
    outtag = tag
    if (is_twitter_cf_modal(token)):
        outtag = 'MD'
    elif (tag_CCJ(token)):
        outtag = 'CCJ'
    return token, outtag


def write_to_output(outfile, message_id, fips_code, cf_form):
    output = str.format()

    outfile.write(output)



def format_tweet(message):
    m = message
    m = m.replace('\n', ' ')
    m = m.encode('ascii', 'ignore')
    return m

def format_tagged(tagged_list):
    out = ''
    for t in tagged_list:
        token, tag = postprocess_tag(t[0], t[1])
        out = out + token + '/' + tag + '/'
    out = out + '\n'
    return out


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

    '''
    Get all tweets from a specific year with coordinates within United States.
    Convert coordinates to county.
    Aggregate tweets within same county.
    Find number of tweets / county.
    Find number of counterfactuals / county.
    Store county, # CFs, # Tweets

    '''

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
        tagged_message = get_tagged_message(message, tagger)
        cf_form = get_cf_form(tagged_message)
        cf = 0 if cf_form == 0 else 1

        if(i % 10000 == 0):
            sys.stdout.write("\r%d results finished..." % i)
            sys.stdout.flush()
        
        # format output
        s_out = str(message_id) + ", "  + str(cnty) + ", " + str(cf) + ", " + str(cf_form) + "\n"
        
        # sql_insert = "INSERT INTO counterfactuals_coord VALUES (" + s_out + ")"
        # mysqlMethods.executeGetSSCursor(mysqlMethods, db, sql_insert)
        outfile.write(s_out)

        i = i + 1

    outfile.close()



if __name__ == "__main__":
    main(sys.argv[1:])
from __future__ import print_function
import json
from pprint import pprint
import csv
from datetime import date, datetime, timedelta
#from sshtunnel import SSHTunnelForwarder
import mysql.connector
#import MySQLdb
import traceback
import nltk
import sys
# from sshtunnel import SSHTunnelForwarder
# import paramiko


'''
**** USAGE ****

In README

'''


def main(argv):
    username = ''
    # private_key_file = ''

    if len(sys.argv) != 3:
        exit()

    username = str(sys.argv[1])
    filename = str(sys.argv[2])


    # my code here
    cnx = mysql.connector.connect(host='127.0.0.1', port=3306, user=username, db="randomTwitter_by_month")
    print("connected")

    cursor = cnx.cursor()

    #open the file to write to
    f = open(filename, 'w')
    
    # test
    cursor.execute("SELECT message FROM messages_es_2014_07_country LIMIT 2")
    for message in cursor:
        #print("Message is : {}".format(message))
        f.write(str(message))
        f.write("\n")

    #close file and connection
    f.close()

    print("closing connection...")
    cnx.close()

if __name__ == "__main__":
    main(sys.argv[1:])
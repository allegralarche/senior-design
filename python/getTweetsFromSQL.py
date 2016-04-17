from __future__ import print_function
import json
from pprint import pprint
import csv
from datetime import date, datetime, timedelta
import mysql.connector
import traceback
import nltk
import sys
import unicodedata


'''

Usage

python getTweetsFromSQL.py <username> <sql query file> <path to output file>

'''

def main(argv):
    username = ''
    # private_key_file = ''

    if len(sys.argv) != 4:
        print("Usage:> python getTweetsFromSQL.py username queryfile.sql outfile.txt")
        exit()

    username = str(sys.argv[1])
    queryfile = str(sys.argv[2])
    filename = str(sys.argv[3])

    qfile = open(queryfile, 'r')
    query = qfile.read()

    cnx = mysql.connector.connect(host='127.0.0.1', port=3306, user=username, db="randomTwitter_by_month")
    print("Connected to database")

    cursor = cnx.cursor()

    # open the file to write to
    f = open(filename, 'w')
    
    # test
    cursor.execute(query)
    for message in cursor:
        # format and write string
        # print(message[0])
        m = message[0]
        # m.replace
        m = m.replace('\n', ' ')
        m = m.encode('ascii', 'ignore')
        f.write(m)
        # f.write(str(message)[3:-3])
        f.write("\n")

    # close file and connection
    f.close()

    print("Closing connection...")
    cnx.close()

if __name__ == "__main__":
    main(sys.argv[1:])
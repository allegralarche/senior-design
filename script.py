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
from sshtunnel import SSHTunnelForwarder

'''
**** USAGE ****

script.py username private_key_file

'''


def main(argv):
    username = ''
    private_key_file = ''

    if len(sys.argv) != 3:
        exit()

    username = str(sys.argv[1])
    private_key_path = str(sys.argv[2])

    with SSHTunnelForwarder(
        ('ssh.wwbp.org', 22),
        ssh_private_key=private_key_path,
        ssh_username=username,
        remote_bind_address=('127.0.0.1', 3308)) as server:

        # my code here
        print('here')
        cnx = mysql.connector.connect(host='127.0.0.1', port=server.local_bind_port, user=username, db="randomTwitter_by_month")

        cursor = cnx.cursor()

        # test
        cursor.execute("SELECT message FROM messages_es_2014_07_country LIMIT 1")

        print(cursor)

        cnx.close()

if __name__ == "__main__":
    main(sys.argv[1:])
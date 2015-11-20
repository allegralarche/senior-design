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

Make sure you do this:
mysql -u root
GRANT SELECT ON randomTwitter_by_month.* TO 'username'@'localhost';
GRANT SELECT ON randomTwitter_by_month.* TO 'username'@'%';

First run in command prompt: 
ssh username@ssh.wwbp.org -i "path_to_private_key" -L 3306:127.0.0.1:3306:3306 -N

Second run in different command prompt:
script.py username

'''


def main(argv):
    username = ''
    # private_key_file = ''

    if len(sys.argv) != 2:
        exit()

    username = str(sys.argv[1])


    # my code here
    cnx = mysql.connector.connect(host='127.0.0.1', port=3306, user=username, db="randomTwitter_by_month")
    print("connected")

    cursor = cnx.cursor()
    
    # test
    cursor.execute("SELECT message FROM messages_es_2014_07_country LIMIT 1")
    for (message) in cursor:
        print("Message is : {}".format(message))


    print("closing connection...")
    cnx.close()

if __name__ == "__main__":
    main(sys.argv[1:])
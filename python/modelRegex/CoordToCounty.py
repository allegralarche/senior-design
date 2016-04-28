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
import urllib2
import re
import array
import csv



def get_counties(coordinates):
    url = "http://www.datasciencetoolkit.org/coordinates2politics/"
    req = urllib2.Request(url)
    req.add_data(str(coordinates))
    response = urllib2.urlopen(req)
    res = response.read()
    json_res = json.loads(res)

    counties = [0 for i in range(len(coordinates))]


    for i in xrange(len(coordinates)):
        politics = json_res[i]['politics']
        county = None
        if politics != None:
            for j in xrange(len(politics)):
                if politics[j]['friendly_type'] == 'county':
                    county = int(politics[j]['code'].replace('_', ''))
                    break;
        counties[i] = county

    return counties


def main(argv):

    if len(sys.argv) != 3:
            print("Usage:> python counterfactual_coord_to_county.py cf_coord.csv cf_county.csv")
            exit()

    filename = str(sys.argv[1])
    outfile_name = str(sys.argv[2])

    outfile = open(outfile_name, 'w')
    count = 0

    batch_size = 500
    batch_coords = []
    rows = []
    with open(filename, 'r') as file:
        csvreader = csv.reader(file)

        i = 0
        for row in csvreader:
            if (i >= batch_size):
                # send request
                
                counties = get_counties(batch_coords)

                # write to file
                for x in xrange(len(counties)):
                    outfile.write(str(rows[x][0]) + ", " + str(counties[x]) + ", " + str(rows[x][3]) + ", " + str(rows[x][4]) + "\n")


                i = 0
                batch_coords = []
                rows = []

            rows.append(row)
            batch_coords.append([float(row[1]), float(row[2])])
            i = i + 1

            if (count % batch_size == 0):
                print("\r {} results finished...".format(count))
            count = count + 1
    
    counties = get_counties(batch_coords)

    # write to file
    for x in xrange(len(counties)):
        outfile.write(str(rows[x][0]) + ", " + str(counties[x]) + ", " + str(rows[x][3]) + ", " + str(rows[x][4]) + "\n")


    outfile.close()


if __name__ == "__main__":
        main(sys.argv[1:])
from __future__ import print_function
import sys
import mysql.connector
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import accuracy_score
import numpy
import scipy



def main(argv):
    if len(sys.argv) != 4:
        print("Usage:> python get_correlation.py TABLENAME COLUMN_NAME JOIN_COLUMN_NAME")
        exit()


    db = 'counterfactuals'
    username = 'kzembroski'
    table_name = str(sys.argv[1])
    column_name = str(sys.argv[2])
    join_column = str(sys.argv[3])

    query = "SELECT X1.score, X2." + column_name + " FROM county_counterfactuals_2012 as X1 INNER JOIN " + table_name + " AS X2 ON X1.cnty_id = X2." + join_column + " WHERE X1.message_count > 652"

    X1 = []
    X2 = []

    cnx = mysql.connector.connect(host='127.0.0.1', port=3306, user=username, db=db)
    cursor = cnx.cursor()
    cursor.execute(query)

    for result in cursor:
        X1.append(result[0]) if result[0] != None else X1.append(0)
        X2.append(result[1]) if result[1] != None else X2.append(0)


    pearson_corr = scipy.stats.pearsonr(X1, X2)
    print(pearson_corr)


if __name__ == "__main__":
    main(sys.argv[1:])
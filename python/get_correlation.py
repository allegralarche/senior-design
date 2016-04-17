from __future__ import print_function
import sys
# import mysql.connector
import mysqlMethods
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import accuracy_score
import numpy
import scipy



def main(argv):
    if len(sys.argv) != 4:
        print("Usage:> python get_correlation.py  TABLENAME  CORR_COLUMN  JOIN_COLUMN")
        exit()


    db = 'counterfactuals'
    # username = 'kzembroski'
    table_name = str(sys.argv[1])
    column_name = str(sys.argv[2])
    join_column = str(sys.argv[3])

    query = "SELECT X1.score, X2." + column_name + " FROM county_1400_counterfactuals_2012 as X1 INNER JOIN " + table_name + " AS X2 ON X1.cnty_id = X2." + join_column
    
    '''
    ADD this to end of query if want more messages per county:
    + " WHERE X1.message_count > 652"
    '''

    X1 = []
    X2 = []

    sys.stdout.write("\rEstablishing connection...")
    sys.stdout.flush()

    sys.stdout.write("\rExecuting query...")
    sys.stdout.flush()

    cursor = mysqlMethods.executeGetSSCursor(mysqlMethods, db, query)
    # cnx = mysql.connector.connect(host='127.0.0.1', port=3306, user=username, db=db)
    # cursor = cnx.cursor()

    # cursor.execute(query)

    sys.stdout.write("\rGetting correlation...\n")

    for result in cursor:
        X1.append(result[0]) if result[0] != None else X1.append(0)
        X2.append(result[1]) if result[1] != None else X2.append(0)


    pearson_corr = scipy.stats.pearsonr(X1, X2)
    print("R: {}".format(pearson_corr[0]))
    print("p-val: {}".format(pearson_corr[1]))


if __name__ == "__main__":
    main(sys.argv[1:])
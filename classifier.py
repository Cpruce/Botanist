#!/usr/bin/python
#
#   File created by Cory Pruce on 10/25/2015
#
#   Part of the RevEngdroid project
#
#
#   The classifier program takes a signature and compares against previously
#   seen instances through clusters. If the distance is within a certain
#   threshold, the signature is added to the cluster. If it does not fall within
#   the limit distance for a cluster, a new one is created with itself as the
#   cluster id.
#

import sys
from optparse import OptionParser
import fileinput
import MySQLdb


option_0 = {
    'name': ('-f', '--file'),
    'help': 'filename input (APK or android resources(arsc))',
    'nargs': 1
}
option_1 = {
    'name': ('-v', '--verbose'),
    'help': 'verbose mode',
    'action': 'count'
}

options = [option_0, option_1]

def table_add(cur, params, db):
    query = """INSERT INTO signatures VALUES(%s, %s, %s);"""
    try:
       cur.execute(query, params)
       db.commit()
    except:
        db.rollback()


def tapered_levenshtein(sig1, sig2):
    sig1_mnemonics = sig1.split()
    sig2_mnemonics = sig2.split()
    position = 0
    num_mnemonics = len(sig1_mnemonics) #assumption len(sig1) == len(sig2)
    weight = 1.0 - position/num_mnemonics
    distance = 0.0

    for mn1, mn2 in sig1_mnemonics, sig2_mnemonics:
        if mn1 != mn2:
            distance+=weight

        position+=1
        weight = 1.0 - position/num_mnemonics

    return distance


def cluster_add(sig):
    flag = 0
    epsilon = 10 # threshold hold that decides clustering

    try:
        db = MySQLdb.connect(host="localhost", # your host, usually localhost
                      user="root", # your username
                      passwd="password", # your password
                      db="signatureDB") # name of the data base

        cur = db.cursor()

        cur.execute("SHOW tables;", [])

        if cur.rowcount > 0:


            for row in cur.fetchall():
                #print row
                if "signatures" in row[0]:
                    flag = 1
                    break

        if flag == 0:

            query = "CREATE TABLE signatures (signature VARCHAR(300) DEFAULT NULL, cluster_id VARCHAR(300) DEFAULT NULL, distance FLOAT, PRIMARY KEY (signature), UNIQUE(signature)) ENGINE=InnoDB;"

            cur.execute(query, ())
            print 'Table created'
            params = (sig, sig, 0.0)
            table_add(cur, params, db)
            return

        query = "SELECT * FROM signatures WHERE signature = '" + sig + "';"
        cur.execute(query, ())

        if cur.rowcount > 0:
            # signature already exists, print contents
            row = cur.fetchall()
        else:
            print "no item found, finding cluster"

            distance = 0.0
            min_cid = ('', 100000000.000)
            query = "SELECT cluster_id FROM signatures;"
            cluster_ids = [] # store tuples of cluster_ids + distances
            cur.execute(query, ());

            if cur.rowcount > 0:
                for row in cur.fetchall():
                    cluster_id = row['cluster_id']
                    print 'cluster_id is ' + cluster_id
                    flag = 0

                    # don't compare with a cluster id already passed by
                    for (cid, dist) in cluster_ids:
                        if cid == cluster_id:
                            flag = 1
                            break
                    if flag == 0:
                        distance = tapered_levenshtein(sig, cluster_id)
                        cluster_ids.append((cluster_id, distance))

                        if distance < min_cid[1]:
                            min_cid = (cluster_id, distance)

                if min_cid[1] <= -epsilon or min_cid >= epsilon:
                    params = (sig, sig, 0.0)
                    table_add(cur, params, db)
                else:
                    params = (sig, min_cid[0], min_cid[1])
                    table_add(cur, params, db)
            else:

                params = (sig, sig, 0.0)
                table_add(cur, params, db)


    except MySQLdb.Error, (i, e):
            print (i, e)
            if "Unknown database" in e:
                con = MySQLdb.connect(user="root", passwd="password")
                cur = con.cursor()
                cur.execute('CREATE DATABASE signatureDB;')
                print "signatureDB created"
                cur.execute("USE signatureDB;")
                query = "CREATE TABLE signatures (signature VARCHAR(300) DEFAULT NULL, cluster_id VARCHAR(300) DEFAULT NULL, distance FLOAT, PRIMARY KEY (signature), UNIQUE(signature)) ENGINE=InnoDB;"

                cur.execute(query, ())

                params = (sig, sig, 0.0)
                table_add(cur, params, con)



    # print all the first cell of all the rows
    for row in cur.fetchall() :
        print row[0]


def main(options, arguments):

    sig = fileinput.input()[0].strip('\n')[:-1]
    if "error" in sig:
        print sig
    else:
        cluster_add(sig)


if __name__ == "__main__":
    parser = OptionParser()
    for option in options:
        param = option['name']
        del option['name']
        parser.add_option(*param, **option)


    options, arguments = parser.parse_args()
    sys.argv[:] = arguments
    main(options, arguments)

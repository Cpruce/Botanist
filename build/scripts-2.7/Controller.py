#
#   File created by Cory Pruce on 10/25/2015
#
#   Part of the RevEngdroid project
#
#
#   The controller program provides the API for operations on the MySQL table.
#

import MySQLdb

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

def table_add(cur, params, db):
    query = """INSERT INTO signatures VALUES(%s, %s, %s);"""
    try:
       cur.execute(query, params)
       db.commit()
    except:
        db.rollback()

def has_table(cur):

    cur.execute("SHOW tables;", [])

    if cur.rowcount > 0:
        for row in cur.fetchall():
            # assuming the table name is signatures
            if "signatures" in row[0]:
                return True

    return False

def create_table(cur):
    query = "CREATE TABLE signatures (signature VARCHAR(300) DEFAULT NULL, cluster_id VARCHAR(300) DEFAULT NULL, distance FLOAT, PRIMARY KEY (signature), UNIQUE(signature)) ENGINE=InnoDB;"

    cur.execute(query, ())
    print 'Table created'

def find_cluster(cur, sig, db):
    print "no item found, finding cluster"

    epsilon = 10 # threshold hold that decides clustering
    distance = 0.0
    min_cid = ('', 100000000.0)
    query = "SELECT cluster_id FROM signatures;"
    cluster_ids = [] # store tuples of cluster_ids + distances
    cur.execute(query, ());

    if cur.rowcount > 0:
        for row in cur.fetchall():
            cluster_id = row['cluster_id']
            print 'cluster_id is ' + cluster_id

            distance = tapered_levenshtein(sig, cluster_id)
            cluster_ids.append((cluster_id, distance))

            if distance < min_cid[1]:
                min_cid = (cluster_id, distance)

        if epsilon <= min_cid[1]:
            params = (sig, sig, 0.0)
            table_add(cur, params, db)
        else:
            params = (sig, min_cid[0], min_cid[1])
            table_add(cur, params, db)
    else:
        params = (sig, sig, 0.0)
        table_add(cur, params, db)

def find_placement(cur, sig, db):
    query = "SELECT * FROM signatures WHERE signature = '" + sig + "';"
    cur.execute(query, ())

    if cur.rowcount > 0:
        # signature already exists, print contents
        row = cur.fetchall()
        print "Signature exists"
        print row
    else:
        find_cluster(cur, sig, db)

def test_and_connect(uname, pwd, sig):
    table_exists = False

    try:
        db = MySQLdb.connect(host="localhost", # your host, usually localhost
                      user=uname, # your username
                      passwd=pwd, # your password
                      db="signatureDB") # name of the data base

        cur = db.cursor()

        table_exists = has_table(cur)

        if table_exists == False:
            create_table(cur)
            params = (sig, sig, 0.0)
            table_add(cur, params, db)
            return

        find_placement(cur, sig, db)

    except MySQLdb.Error, (i, e):

        if "Unknown database" in e:
            con = MySQLdb.connect(user="root", passwd="password")
            cur = con.cursor()
            cur.execute('CREATE DATABASE signatureDB;')
            print "signatureDB created"
            cur.execute("USE signatureDB;")

            create_table(cur)
            params = (sig, sig, 0.0)
            table_add(cur, params, con)
        else:
            print (i, e)


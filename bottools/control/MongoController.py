#
#   File created by Cory Pruce on 11/24/2015
#
#   Part of the RevEngdroid project
#
#
#   The controller program provides the API for operations on the MongoDB table.
#

import pymongo

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
                db.close()
                return True

    return False

def create_index(cur):
    result = db.instances.create_index([('instance_id', pymongo.ASCENDING)], unique=True)

def create_table(cur):

    query = "CREATE TABLE signatures (signature VARCHAR(300) DEFAULT NULL, cluster_id VARCHAR(300) DEFAULT NULL, distance FLOAT, PRIMARY KEY (signature), UNIQUE(signature)) ENGINE=InnoDB;"

    cur.execute(query, ())
    print 'Table created'


def find_cluster(sig, db):

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

def find_placement(cur, sig):

    db = get_sig_table_handler()

    query = "SELECT * FROM signatures WHERE signature = '" + sig + "';"
    cur.execute(query, ())

    if cur.rowcount > 0:
        # signature already exists, print contents
        row = cur.fetchall()
        print "Signature exists"
        print row
    else:
        find_cluster(cur, sig, db)
    
    db.close()

def test_and_connect(sig):#uname, pwd, sig):
    table_exists = False

    try:
        db = pymongo.MongoClient('mongodb://localhost:27017/SignaturesDB')
        instances = db['instances']

        table_exists = has_table(cur)

        if table_exists == False:
            create_table(cur)
            params = (sig, sig, 0.0)
            table_add(cur, params, db)
            return

        find_placement(cur, sig, db)
        db.close()

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

def insert_sig(sig):
    test_and_connect(sig)


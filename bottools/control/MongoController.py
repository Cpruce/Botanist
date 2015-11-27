#
#   File created by Cory Pruce on 11/24/2015
#
#   Part of the RevEngdroid project
#
#   The controller program provides the API for operations on the MongoDB table.
#   Mongo creates the collection upon first insertion if collection does not
#   already exist.

import sys
import json
import pymongo
from bottools.api.Classifier import tapered_levenshtein
from bottools.api.LibSO import LibSO

################# Intended Interface #######################

def insert_instance(so_inst):

    res = test_and_connect()

    if res == None:
        print 'Could not connect to mongodb. Is mongod running on port 27017?'
        return

    (clusters, botdb, mclient) = res

    # find place in clusters, or create another
    find_placement(clusters, so_inst)

    mclient.close()

def get_clusters():

    res = test_and_connect()

    if res == None:
        print 'Could not connect to mongodb. Is mongod running on port 27017?'
        return

    (clusters, botdb, mclient) = res

    # gather cluster id's to determine if part of an existing cluster
    clusters_centers = clusters.find(
        {'jni_onload_info.is_cluster_center': True})

    for center in clusters_centers:
        print center

    mclient.close()

################### Direct MongoDB Functions ####################

def test_and_connect():
    try:
        # hardcoded test config
        mclient = pymongo.MongoClient('mongodb://localhost:27017')

        db = connect_db(mclient)
        clusters = connect_collection(db)
        return (clusters, db, mclient)

    except pymongo.errors.PyMongoError:
        return None

def connect_db(mclient):

    try:
        # TODO: add db.authenticate(username, password...) around here
        # for convenience during dev, this will be left out

        # ASSUMPTION: this db name is BotanistDB. This can be changed here
        # and in db_populate.js if another db name is desirable.
        botDB = mclient['BotanistDB']
        return botDB

    except pymongo.errors.InvalidName:

        # BotanistDB does not exist. Create a new instance.
        botDB = pymongo.database.Database(mclient, 'BotanistDB')
        return botDB

def connect_collection(db):

    try:
        # ASSUMPTION: collection name is called clusters. Like with the db
        # name, this can be changed.
        clusters = db['clusters']
        return clusters

    except pymongo.errors.InvalidName:

        # since InvalidName was raised, CollectionInvalid signifying existence
        # shouldn't be raised.
        db.create_collection('clusters')
        clusters = db['clusters']
        return clusters

#def create_index(db):
#    result = db.instances.create_index([('cluster_id', pymongo.ASCENDING)], 
# unique=True)

############### Clustering Logic ###################

def find_placement(clusters, so_inst):

    # if exact copy exists, 
    incumbant = clusters.find_one({'hash':so_inst.sha1})

    # found exact copy
    if incumbant != None:
        # did not find association with current apk
        if so_inst.apk_filename not in incumbant['apks_found_in']:
            instance = clusters.find_one_and_update({'hash':so_inst.sha1}, 
                                                    {$push:{'apks_found_in': 
                                                    so_inst.apk_filename}})
        return 

    # gather cluster id's to determine if part of an existing cluster
    clusters_centers = clusters.find(
        {'jni_onload_info.is_cluster_center': True})

    for center in clusters_centers:
        center_obj = json.load(center)

        # calculate weight distance based on the shorter lengthed signature
        # TODO: Remove similar code at the start of JNI_OnLoad's
        (distance, num_mnemonics) = tapered_levenshtein(
            center_obj["jni_onload_info"]["signature"], so_inst.mnemonics)

        # calc similarity with center
        similarity = 1.0 - distance/num_mnemonics

        if similarity >= 0.9:
            # found cluster, end search
            # TODO: switch to insert_many with large amounts of apks
            instance = 
                clusters.insert_one({'so_file_name': so_inst.so_file_name,
                                     'apks_found_in':[so_inst.apk_filename],
                                     'hash': so_inst.sha1,
                                     'jni_onload_info': {
                                        'signature': so_inst.mnemonics,
                                        'is_cluster_center': False,
                                         'similarity_with_center': similarity,
                                         'variations': []
                                      })
            return

    # else form own cluster
    instance = clusters.insert_one({'so_file_name': so_inst.so_file_name,
                                     'apks_found_in':[so_inst.apk_filename],
                                     'hash': so_inst.sha1,
                                     'jni_onload_info': {
                                        'signature': so_inst.mnemonics,
                                        'is_cluster_center': True,
                                         'similarity_with_center': 1.0,
                                         'variations': []
                                      })
 
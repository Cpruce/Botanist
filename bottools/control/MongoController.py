#
#   File created by Cory Pruce on 11/24/2015
#
#   Part of the RevEngdroid project
#
#   The controller program provides the API for operations on the MongoDB table.
#   Mongo creates the collection upon first insertion if collection does not
#   already exist.

import sys
import pymongo
import json
from bottools.api.Classifier import tapered_levenshtein
from bottools.api.LibSO import LibSO

################# Intended Interface #######################

def insert_lib_instance(so_inst):

    res = test_and_connect('libraries')

    if res == None:
        print 'Could not connect to mongodb. Is mongod running on port 27017?'
        return

    (libraries, botdb, mclient) = res

    # find place in libraries, or create another
    find_lib_placement(libraries, so_inst)

    mclient.close()

def insert_apk_instance(apk_inst):

    res = test_and_connect('apks')

    if res == None:
        print 'Could not connect to mongodb. Is mongod running on port 27017?'
        return

    (apks, botdb, mclient) = res

    # find place in libraries, or create another
    find_apk_placement(apks, apk_inst)

    mclient.close()

# inserting apk name when no apk found
def insert_dummy_apk_instance(apk_name):

    res = test_and_connect('apks')

    if res == None:
        print 'Could not connect to mongodb. Is mongod running on port 27017?'
        return

    (apks, botdb, mclient) = res

    write_result = apks.insert_one({"apk_name":apk_name, "present":False, "libs":[]})

    mclient.close()

def get_apks():

    res = test_and_connect('apks')

    if res == None:
        print 'Could not connect to mongodb. Is mongod running on port 27017?'
        return

    (apks, botdb, mclient) = res

    # gather cluster id's to determine if part of an existing cluster
    apk_insts = apks.find()

    ret = []
    for apk_inst in apk_insts:
        ret.append(apk_inst)

    mclient.close()
    return ret

def get_libs():

    res = test_and_connect('libraries')

    if res == None:
        print 'Could not connect to mongodb. Is mongod running on port 27017?'
        return

    (libraries, botdb, mclient) = res

    # gather cluster id's to determine if part of an existing cluster
    so_libs = libraries.find()

    ret = []
    for so_lib in so_libs:
        ret.append(so_lib)

    mclient.close()
    return ret

def get_clusters():

    res = test_and_connect('libraries')

    if res == None:
        print 'Could not connect to mongodb. Is mongod running on port 27017?'
        return

    (libraries, botdb, mclient) = res

    # gather cluster id's to determine if part of an existing cluster
    cluster_centers = libraries.find(
        {'jni_onload_info.is_cluster_center': True})

    ret = []
    for cluster in cluster_centers:
        ret.append(cluster)

    mclient.close()
    return ret

################### Direct MongoDB Functions ####################

def test_and_connect(collection_name):
    try:
        # hardcoded test config
        mclient = pymongo.MongoClient('mongodb://localhost:27017/')

        db = connect_db(mclient)
        collection = connect_collection(db, collection_name)
        return (collection, db, mclient)

    except pymongo.errors.PyMongoError as e:
        print e
        return None

def connect_db(mclient):

    try:
        # TODO: add db.authenticate(username, password...) around here
        # for convenience during dev, this will be left out

        # ASSUMPTION: this db name is BotanistDB. This can be changed here
        # and in db_populate.js if another db name is desirable.
        botDB = mclient['BotanistDB']
        return botDB

    except pymongo.errors.InvalidName as e:
        print e
        # BotanistDB does not exist. Create a new instance.
        botDB = pymongo.database.Database(mclient, 'BotanistDB')
        return botDB

def connect_collection(db, collection_name):

    try:

        collection = db[collection_name]
        return collection

    except pymongo.errors.InvalidName as e:
        print e
        # since InvalidName was raised, CollectionInvalid signifying existence
        # shouldn't be raised.
        db.create_collection(collection_name)
        collection = db[collection_name]
        return collection

############### Clustering Logic ###################

def add_potential_lib_variation(libraries, so_inst):

    # if name exists,
    try:
        incumbant = libraries.find_one({'so_file_name':so_inst.so_file_name})
        # found copy by name
        if incumbant != None:
            # did not find association with current apk
            if so_inst.apk_filename not in incumbant['apks_found_in']:

                write_result = libraries.update_one({'so_file_name':so_inst.so_file_name}, { '$push': { 'apks_found_in' : so_inst.apk_filename } } )
                print 'added to existing record'
                return True

    except Exception as e:
        print e

    return False

def find_lib_cluster_link(so_inst, libs):

    (closest_relative, max_similarity) = ("nothing", 0.0)

    for lib in libs:

        # lib's with absent sigs cannot be cluster centers
        if lib["jni_onload_info"]["signature"] != []:
            print 'Comparing signatures of ' + lib['so_file_name'] + ' and ' + so_inst.so_file_name
            print lib['jni_onload_info']['signature'], so_inst.mnemonics
            # calculate weight distance based on the shorter lengthed signature
            # TODO: Remove similar code at the start of JNI_OnLoad's
            (distance, num_mnemonics) = tapered_levenshtein(lib["jni_onload_info"]["signature"], so_inst.mnemonics)

            # calc similarity with center
            similarity = 1.0 - float(distance)/num_mnemonics
            print '\tSimilarity is ' + str(similarity) + ' and distance ' + str(distance) + '\n'
            if similarity > max_similarity:
                # found cluster, end search
                # TODO: switch to insert_many with large amounts of apks
                max_similarity = similarity
                closest_relative = lib["so_file_name"]

    print 'Chose ' + closest_relative
    return (closest_relative, max_similarity)

def find_lib_placement(libraries, so_inst):

    is_variation = add_potential_lib_variation(libraries, so_inst)

    if is_variation:
        return

    # gather cluster id's to determine if part of an existing cluster
    try:

        libs = libraries.find()

        (closest_relative, max_similarity) = find_lib_cluster_link(so_inst, libs)

        json_obj = json.loads("{}")
        json_obj['so_file_name'] = so_inst.so_file_name
        json_obj['arch'] = so_inst.arch
        json_obj['apks_found_in'] = [so_inst.apk_filename]
        json_obj['sha1'] = so_inst.sha1
        json_obj['jni_onload_info'] = { 'signature': []}
        json_obj['jni_onload_info']['signature'] = so_inst.mnemonics
        json_obj['variations'] = []

        if max_similarity == 0.0:
            # form own cluster
            json_obj["jni_onload_info"]["is_cluster_center"] = True
            json_obj["jni_onload_info"]["similarity_with_center"] = 1.0
            print 'created new cluster'
        else:
            json_obj["jni_onload_info"]["is_cluster_center"] = False
            json_obj["jni_onload_info"]["similarity_with_center"] = max_similarity
            so_file_name = json_obj["so_file_name"]
            write_result = libraries.update_one({'so_file_name':closest_relative}, { "$push" : { 'variations' : so_file_name } })
            print 'added to existing cluster'

        write_result = libraries.insert_one(json_obj)

    except Exception as e:
        print e

def add_potential_apk_variation(apk, incumbant, apks):

    variation = json.loads('{}')

    # see what discrepancies there are and add variation
    if incumbant["package"] != apk.package:
        variation["package"] = apk.package
    if incumbant["permissions"] != apk.permissions:
        variation["permissions"] = apk.permissions
    if incumbant["libs"] != apk.libs:
        variation["libs"] = apk.libs

    # if not empty
    if variation != {}:
        # assumption: variation to already in list since
        # sha1 not found
        write_result = apks.update_one({'apk_name':incumbant["apk_name"], 'sha1': incumbant["sha1"]}, { "$addToSet" : { 'variations' : variation } })

    # o.w. do nothing. this is an exact match

def find_apk_cluster_link(apks, apk):

    json_obj = json.loads('{}')

    json_obj['apk_name'] = apk.apk_name
    json_obj['sha1'] = apk.sha1
    json_obj['package'] = apk.package
    json_obj['permissions'] = apk.permissions
    json_obj['libs'] = [lib.so_file_name + ":" + lib.arch for lib in apk.libs]
    print 'libs is ' + str(json_obj['libs'])
    json_obj['present'] = True

    # nothing to compare. attach to root
    if apk.libs == []:

        write_result = apks.insert_one(json_obj)
        return

    # cluster by similarity in .so files

    apk_insts = apks.find({})

    (closest_relative, max_common_libs) = ("nothing", 0)

    for apk_inst in apk_insts:

        if apk_inst['present']:
            if apk_inst["libs"] != []:
                num_common_libs = 0

                for lib in apk_inst["libs"]:
                    if lib in apk.libs:
                        num_common_libs+=1

                if num_common_libs > max_common_libs:
                    closest_relative = apk_inst["apk_name"]
                    max_common_libs = num_common_libs

    write_result = apks.update_one({'apk_name':closest_relative}, { "$addToSet" : { 'variations' : json_obj["apk_name"] } })
    write_result = apks.insert_one(json_obj)


def find_apk_placement(apks, apk_inst):
    try:
        print str(apk_inst.libs)
        incumbant = apks.find_one({'apk_name':apk_inst.apk_name})
        # found copy by name
        if incumbant != None:
            add_potential_apk_variation(apk_inst, incumbant, apks)
        else:
            # match not found, insert separate
            find_apk_cluster_link(apks, apk_inst)

    except Exception as e:
        print e





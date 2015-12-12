#!/usr/bin/python
#
#   File created by Cory Pruce, Rajiv Kulkarni,
#   and Kumar Vikramjeet on 12/1/2015
#
#   Botanist Build Graph script
#
#   This program is used to build the json
#   representation of the graph that will be
#   loaded into the javascript client.

import sys
import pymongo
import json
from bottools.api.APKInfo import APKInfo
from bottools.control.MongoController import get_lib, get_libs
from optparse import OptionParser
from androguard.core.androconf import *
import bson.json_util
options = []

traversed = []

def make_json_obj(apk):
    cur_json_obj = json.loads('{}')

    cur_json_obj['name'] = apk["apk_name"]
    cur_json_obj['size'] = 1
    # stopped here, focusing on libs
    cur_json_obj['apks_in'] = so_lib["apks_found_in"]
    cur_json_obj['sha1'] = so_lib['sha1']

    return cur_json_obj
           
def createChildBranches(cur_json_obj, so_lib):
   
    if so_lib['variations'] == []:
        return cur_json_obj

    cur_json_obj['children'] = []
    
    # branch off again if variation has variations
    for v in so_lib['variations']:
       
        var = v.split(':')
        name = var[0]
        sha1 = var[1]
        
        if sha1 not in traversed:
                        
            traversed.append(sha1)
            var_so = get_lib(sha1)
            var_obj = make_json_obj(var_so)
            var_obj = createChildBranches(var_obj, var_so)
            cur_json_obj['size'] += var_obj['size']
            cur_json_obj["children"].append(var_obj) 

    return cur_json_obj

def createMainBranch(json_obj, so_libs):

    json_obj['size'] = 0
    for so_lib in so_libs:

        if so_lib['sha1'] not in traversed:

            traversed.append(so_lib['sha1'])
            
            cur_json_obj = make_json_obj(so_lib)

            # only records with sig's can have variations
            if so_lib['jni_onload_info']['signature'] != []:

                cur_json_obj['sig'] = so_lib["jni_onload_info"]["signature"]
                if so_lib['variations'] == []:
                    continue
               
                cur_json_obj['children'] = []
                # not used atm
                #is_cluster_center = so_lib["jni_onload_info"]["is_cluster_center"]
        
                # use the variations to build branches
                #for variation in so_lib['variations']:
                cur_json_obj = createChildBranches(cur_json_obj, so_lib)
                json_obj['size'] += cur_json_obj['size']

            json_obj["children"].append(cur_json_obj)
    

    return json_obj

def main(options, arguments):
    # get clusters from mongodb collection
    # assumption: mongod is running and is populated :p
    so_libs = get_libs()

    # initial json structure for the d3.js CodeFlower
    # module
    init_json = '''{
        "name":"root",
        "children":[]
        }'''

    # parse json and create obj
    json_obj = json.loads(init_json)
    # use obj to store clustering schematic
    json_obj = createMainBranch(json_obj, so_libs)
    # save json data
    with open('apks.json', 'w') as outfile:
        print >> outfile, bson.json_util.dumps(json_obj)


if __name__ == "__main__":
    parser = OptionParser()
    for option in options:
        param = option['name']
        del option['name']
        parser.add_option(*param, **option)


    options, arguments = parser.parse_args()
    sys.argv[:] = arguments
    main(options, arguments)

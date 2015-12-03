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
from bottools.control.MongoController import get_libs
from optparse import OptionParser
from androguard.core.androconf import *

options = []

def createChildBranch():


def createMainBranch(json_obj, so_libs):
     
    for so_lib in so_libs:
        
        cur_json_obj = json.loads('{}')
        
        cur_json_obj['name'] = so_lib["so_file_name"] 
        cur_json_obj['apks_in'] = so_lib["apks_found_in"]
        cur_json_obj['size'] = len(cur_json_obj['apks_in']

        # only records with sig's can have variations
        if sig != []:
        
            cur_json_obj['sig'] = so_lib["jni_onload_info"]["signature"]
                 
            # not used atm
            #is_cluster_center = so_lib["jni_onload_info"]["is_cluster_center"]
                            
            # use the variations to build branches
            for variation in so_lib['variations']:
                cur_json_obj = createChildBranch(cur_json_obj, variation, )
                
        json_obj["children"].append(cur_json_obj)
    

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
    with open('libs.json', 'w') as outfile:
        json.dump(json_obj, outfile)

if __name__ == "__main__":
    parser = OptionParser()
    for option in options:
        param = option['name']
        del option['name']
        parser.add_option(*param, **option)


    options, arguments = parser.parse_args()
    sys.argv[:] = arguments
    main(options, arguments)

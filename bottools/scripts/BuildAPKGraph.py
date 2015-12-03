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
from bottools.api.Classifier import tapered_levenshtein
from bottools.control.MongoController import get_clusters
from optparse import OptionParser
from androguard.core.androconf import *

options = []

#def createChildBranch(cur_root, variations):
#
#    for variation in variations:
#        cur_root["children"].push(variation)

def main(options, arguments):
    # get clusters from mongodb collection
    # assumption: mongod is running and is populated :p
    clusters_centers = get_clusters()

    # initial json structure for the d3.js CodeFlower
    # module
    init_json = '''{
        "name":"root",
        "children":[]
        }'''

    json_obj = json.loads(init_json)

    for cluster_center in clusters_centers:
        #print cluster_center['jni_onload_info']['signature']
        json_obj["children"].append({"name":cluster_center["so_file_name"],"size":len(cluster_center["apks_found_in"])})

        #for variation in variations:
            # TODO: createChildBranch


    with open('data.json', 'w') as outfile:
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

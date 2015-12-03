#!/usr/bin/python
#
#   File created by Cory Pruce, Rajiv Kulkarni,
#   and Kumar Vikramjeet on 12/1/2015
#
#   Botanist Signature Comparison script
#
#   This program is used to test the simarilty to
#   other cluster's in the database.

#   TODO: make legitimate tests and branch off
#   into another folder

import sys
import pymongo
import json
from bottools.api.APKInfo import APKInfo
from bottools.api.Classifier import tapered_levenshtein
from bottools.control.MongoController import get_clusters
from optparse import OptionParser
from androguard.core.androconf import *

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

def main(options, arguments):

    libs = libraries.find()


    for json_obj in libs:

        for comp_obj in libs:

            (distance, num_mnemonics) = tapered_levenshtein(center_obj["jni_onload_info"]["signature"], so_inst.mnemonics)

            if distance != -1.0:
                print 'no mnemonics'
                break

            # calc similarity with center
            similarity = 1.0 - float(distance)/num_mnemonics

            if similarity >= 0.9:
                # found cluster, end search
                # TODO: switch to insert_many with large amounts of apks
                instance = libraries.insert_one({'so_file_name': so_inst.so_file_name, 'arch': so_inst.arch, 'apks_found_in':[so_inst.apk_filename], 'hash': so_inst.sha1, 'jni_onload_info': {'signature': so_inst.mnemonics,'is_cluster_center': False, 'similarity_with_center': similarity, 'variations': [] } })
                print 'added to existing cluster'
                return

if __name__ == "__main__":
    parser = OptionParser()
    for option in options:
        param = option['name']
        del option['name']
        parser.add_option(*param, **option)


    options, arguments = parser.parse_args()
    sys.argv[:] = arguments
    main(options, arguments)

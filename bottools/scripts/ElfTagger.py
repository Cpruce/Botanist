#!/usr/bin/python
#
#   File created by Cory Pruce, Rajiv Kulkarni,
#   and Kumar Vikramjeet on 10/26/2015
#
#   Botanist ELFTagger script
#
#   This script uses the Botanist API to collect
#   tools in the form of shared object libraries
#   and generates the set of tool signatures for
#   the supplied APK.

import sys
from bottools.api.APKInfo import APKInfo
from bottools.control.MongoController import insert_apk_instance, insert_dummy_apk_instance, insert_lib_instance
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
    if options.file != None:

        ret_type = is_android(options.file)

        apk_name = options.file

        name_without_path = apk_name.split("/")[-1]

        # only work on APK's
        if ret_type == "APK":

            apk_info = APKInfo(options.file)

            print "\nSignatures for " + name_without_path + "\n" +(15+len(name_without_path))*'-'
            for so_lib in apk_info.libs:
                
                print so_lib.so_file_name + ' (' + so_lib.arch + '): ' + str(so_lib.mnemonics)
                
                insert_lib_instance(so_lib)
                

            insert_apk_instance(apk_info)

        else:
            print "APK " + options.file + " likely missing"
            insert_dummy_apk_instance(name_without_path)

if __name__ == "__main__":
    parser = OptionParser()
    for option in options:
        param = option['name']
        del option['name']
        parser.add_option(*param, **option)


    options, arguments = parser.parse_args()
    sys.argv[:] = arguments
    main(options, arguments)

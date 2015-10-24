#!/usr/bin/python
#
#   File created by Cory Pruce on 10/21/2015
#
#   Part of the RevEngdroid project
#
#   This program is used to unzip and parse
#   apk files for particular signatures for
#   toolchains that have been used. This
#   chain begins in the MainActivity's
#   onCreate method. Notably, the
#   System.loadLibrary function is of
#   interest due to the statement information
#   gain ratio being the most revealing. This
#   HexParse program then creates the signature
#   with the tapered levenshtein distance. The
#   file handling and parsing in this program
#   leverages the androguard framework.

import sys
from optparse import OptionParser
from androguard.core import *
from androguard.core.androconf import *
from androguard.core.bytecode import *
from androguard.core.bytecodes.dvm import *
from androguard.core.bytecodes.apk import *

from androguard.core.analysis.analysis import *
from androguard.decompiler.decompiler import *
from androguard.session import Session

from androguard.util import *
from androguard.misc import *

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

def make_sig(options):
    # Obtain apk, classes.dex, and the classes.dex analysis
    a, d, dx = AnalyzeAPK(options.file)

    # tie analysis to classes.dex
    d.set_vmanalysis(dx)

    # Create cross and data references
    d.create_xref()
    d.create_dref()

    # get MainActivity
    main_act = a.get_main_activity().replace(".", "/")
    # "Runtime" is also important for the Mono DLL
    print main_act

    # find the Xref From of System.loadLibrary
    for method in d.get_methods():

        #if "MonoPackageManager" in method.get_class_name():
        #print main_act, method.get_class_name()
        if main_act in method.get_class_name():# or "onCreate" in method.get_name():
            print method.get_class_name(), method.get_name(), method.get_descriptor()
            idx = 0
            for i in method.get_instructions():
                if options.verbose:
                    print "\t", "%x" % idx, i.get_name(), i.get_output(), i.get_op_value()
                    
                idx += i.get_length()

                # follow the trail
                # TODO: make this more robust. What if there are more
                # invoke-static's or none?
                if "invoke-static" in i.get_name():

                    # parse for the next function
                    func_sig = i.get_output().split(",")

                    params = []
                    for elem in func_sig:
                        if elem[0] == "L":
                            break
                        params.append(elem)





def main(options, arguments):
    if options.file != None:
        # add in checks for malformed input here
        ret_type = is_android(options.file)
        #print ret_type
        if ret_type == "APK":
            #a = apk.APK(options.input)
            make_sig(options)
            #arscobj = a.get_android_resources()

        else:
            print "Unknown file type"
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

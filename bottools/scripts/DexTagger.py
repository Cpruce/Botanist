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
import pydot
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

from capstone import *

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

def get_so(func):

    # the androguard documentation is wrong or
    # outdated. it says source() returns a string
    # but it is void and just prints. some intuition
    # led me to try get_source which got me my str
    src = func.get_source()
    lines = src.split('\n')
    r = ""
    for l in lines:

        if "loadLibrary" in l:
            # extract the shared object file
            r = l.strip()[20:-3] # System.loadLibrary("");
    return r


#def parse_elf(so):
#    so += ".save"
#    print so
    #ex = AnalyzeElf(so)



def make_sig(options):
    # Obtain apk, classes.dex, and the classes.dex analysis
    a, d, dx = AnalyzeAPK(options.file)

    # tie analysis to classes.dex
    d.set_vmanalysis(dx)

    # Create cross and data references
    d.create_xref()
    d.create_dref()

    # cfg unfortunately ends abruptly... should look into why
    #m = d.get_method_descriptor("Lmd5dfde85a0e109f0767a543d97f5960030/MainActivity;", "onCreate", "(Landroid/os/Bundle;)V")

    # get the analysis method and transform it in dot
    #buff_dot = method2dot(dx.get_method( m ))
    #method2format( "toto.jpg", "jpg", raw=buff_dot )




    #for m in d.get_methods():
    #    if "onCreate" in m.name:
    #        print m.name, m.get_descriptor()
            #m.pretty_show()
    """if "MonoPackageManager" in m.class_name:
        if "Runtime" in m.class_name and "init" in m.name:
            print m.class_name + "->" + m.name + " ----------------- " + m.get_descriptor()
            m.show_info()
            m.show_xref()
            m.show_notes()
            m.pretty_show()
            XREFfrom: [" + join_names(m.XREFfrom.items) + "] XREFto: [" + join_names(m.XREFto.items) + "]")"""


    # get MainActivity
    main_act = a.get_main_activity().replace(".", "/")

    # find the tools
    for method in d.get_methods():
        #if "LoadApplication" in method.name:
        #    print method.show_xref()
        #if "MonoPackageManager" in method.get_class_name():
        #print main_act, method.get_class_name()
        #if main_act in method.get_class_name():# or "onCreate" in method.get_name():

        #print method.get_class_name(), method.get_name(), method.get_descriptor()

        # if signature is of the LoadApplication method
        if "loadLibrary" in method.get_source():
            sig = ""

            for i in method.get_instructions():
                sig+=str(i.get_op_value()) + " "
                #print i.get_op_value(),


            print sig

            # there might be more though...
            # this also might not be the right way to find tools
            break

        """idx = 0
        for i in method.get_instructions():
            if options.verbose:
                print "\t", "%x" % idx, i.get_name(), i.get_output(), i.get_op_value()

            if "loadLibrary" in i.get_output():

                so = "lib" + get_so(method) + ".so"
                print so
                for fname in a.get_files():

                    # will the so always be lib+fname+.so?
                    if so in fname:
                        so_file = a.get_file(fname)
                        fd = open(so + ".save","w")
                        print >> fd, so_file
                        fd.close()
                        return parse_elf(so)



            idx += i.get_length()
        """



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

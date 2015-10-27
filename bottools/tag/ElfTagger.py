#!/usr/bin/python
#
#   File created by Cory Pruce on 10/26/2015
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

from capstone import *

import subprocess

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


def get_init(rname, method, d, dx):
    instructions = method.get_code().get_bc().get_instructions()
    rname_passed = False
    loadLib_passed = False

    xrefs_to = method.XREFto.items


    for i in instructions:
        lit = i.get_output()#.split()[1]
        if rname in lit:
            rname_passed = True
            print 'real name passed'
        if rname_passed:
            if "loadLibrary" in lit:
                loadLib_passed = True
                print 'loadLibrary passed'
                
        if loadLib_passed:

            if 'invoke' in i.get_name():

                #print i.get_name(), lit, rname, rname in lit

                for n_method in get_NativeMethods(dx):
                    #print lit, n_method
                    if n_method[0] in lit:
                        print lit, n_method
                        #print path[0], xrefto[0].name, n_method
                        cname = lit[0][1:-1].replace('/', '_')  # remove OS type and semicolon
                        func = "Java_" + cname + "_" + i.get_name()#xrefto[0].name
                        

                """
                for xrefto in xrefs_to:


                    print xrefto[0].name, "||||||||", xrefto[1][0].get_dst(d.get_class_manager()), "|||||||", lit

                    path = xrefto[1][0].get_dst(d.get_class_manager())
                    #xrefto[1][0].show()
                    for n_method in get_NativeMethods(dx):
                        if path[0] in n_method:
                            #print path[0], xrefto[0].name, n_method
                            cname = path[0][1:-1].replace('/', '_')  # remove OS type and semicolon
                            func = "Java_" + cname + "_" + xrefto[0].name
                    """

    return ''


def get_real_names(func):

    # the androguard documentation is wrong or
    # outdated. it says source() returns a string
    # but it is void and just prints. some intuition
    # led me to try get_source which got me my str
    src = func.get_source()
    lines = src.split('\n')
    rnames = []
    for l in lines:
        if "loadLibrary" in l:
            # extract the .so real name
            last_lib = l.strip()[20:-3] # System.loadLibrary("");
            rnames.append(last_lib)

    return rnames


def parse_elf(so, func):

    cmd_get_func = "nm -D test/" + so + " | grep '" + func + "'"

    process = subprocess.Popen(cmd_get_func.split(), stdout=subprocess.PIPE)

    output = process.communicate()[0]
    print output

def dump_files(so, a):
    for fname in a.get_files():

        if so in fname:
            so_file = a.get_file(fname)
            fd = open(so,"w")
            print >> fd, so_file
            fd.close()
            return True

    return False

def find_so_files(method, a):
    rnames = get_real_names(method)
    so_files = []

    for rname in rnames:
        so = "lib" + rname + ".so"
        so_file = ""

        if dump_files(so, a):
            so_files.append(so)

    return so_files

def find_tools(options):
    # Obtain apk, classes.dex, and the classes.dex analysis
    a, d, dx = AnalyzeAPK(options.file)

    # tie analysis to classes.dex
    d.set_vmanalysis(dx)

    # Create cross and data references
    d.create_xref()
    d.create_dref()

    # find the tools
    for method in d.get_methods():

        # find .so's
        if "loadLibrary" in method.get_source():
            so_files = find_so_files(method, a)

            # tag tools
            for so in so_files:
                # .so found, find the init function

                #method.pretty_show()
                rname = so[3:-3] # remove 'lib' prefix and '.so' extension
                init = get_init(rname, method, d, dx)
                #method.show_xref()

                if init != '':
                    # init found, now find code in .so
                    print 'init', init, 'found.'

                else:
                    print 'func', init, 'not found.'



def main(options, arguments):
    if options.file != None:
        # add in checks for malformed input here
        ret_type = is_android(options.file)
        #print ret_type
        if ret_type == "APK":
            #a = apk.APK(options.input)
            find_tools(options)
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

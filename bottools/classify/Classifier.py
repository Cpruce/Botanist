#!/usr/bin/python
#
#   File created by Cory Pruce on 10/25/2015
#
#   Part of the RevEngdroid project
#
#
#   The classifier program takes a signature and compares against previously
#   seen instances through clusters. If the distance is within a certain
#   threshold, the signature is added to the cluster. If it does not fall within
#   the limit distance for a cluster, a new one is created with itself as the
#   cluster id.
#

import sys
import fileinput
from optparse import OptionParser

import bottools.control.Controller as mdb

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
option_2 = {
    'name': ('-u', '--username'),
    'help': 'MySQL user name',
    'nargs': 1
}
option_3 = {
    'name': ('-p', '--password'),
    'help': 'MySQL password',
    'nargs': 1
}
options = [option_0, option_1, option_2, option_3]

# Create Classification class

def main(options, arguments):

    sig = fileinput.input()[0].strip('\n')[:-1]
    if "error" in sig:
        print sig
        sys.exit(1)
    else:
        if options.username:
            uname = options.username
        else:
            uname = "root"

        if options.password:
            pwd = options.password
        else:
            pwd = ""

        print uname, pwd
        mdb.test_and_connect(uname, pwd, sig)


if __name__ == "__main__":
    parser = OptionParser()
    for option in options:
        param = option['name']
        del option['name']
        parser.add_option(*param, **option)


    options, arguments = parser.parse_args()
    sys.argv[:] = arguments
    main(options, arguments)

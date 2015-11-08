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

from r2.r_core import RCore

core = RCore()

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

def get_method_from_instr(instr_args):
    method = ''
    i = 0
    while instr_args[i] != 'L':
        i+=1
    return instr_args[i:]

def get_stub_method(i, rname, type_sig, d, dx):

    if 'invoke' in i.get_name():

        meth_call = get_method_from_instr(type_sig)

        for n_method in get_NativeMethods(dx):

            meth = n_method[0] + '->' + n_method[1] + n_method[2]

            if meth_call == meth:
                # this is the first dynamic library call. From here, the
                # analysis is transfered to finding this method's code
                # in the .so.
                # TODO: make sure that this native call is definitely
                # the first call from THAT library


                #print path[0], xrefto[0].name, n_method
                cname = n_method[0][1:-1].replace('/', '_')  # remove OS type and semicolon
                func = "Java_" + cname + "_" + n_method[1] #TODO: is Java always prepended?
                # for mono: build's 'Java_mono_android_Runtime_init
                print func
                parse_elf(rname, func)
                return 0

    return -1

def get_init(rname, method, d, dx):
    instructions = method.get_code().get_bc().get_instructions()
    rname_passed = False
    loadLib_passed = False

    for i in instructions:
        type_sig = i.get_output()

        # first find the so
        if rname in type_sig:
            rname_passed = True
            print 'real name passed'
            continue
        # next, find the the dynamic load
        if rname_passed:
            if "loadLibrary" in type_sig:
                loadLib_passed = True
                print 'loadLibrary passed'
                continue
        # after the lib load, the first native call to the loaded library will
        # be the "unpacking" routine that will be used as the signature
        if loadLib_passed:

            val = get_stub_method(i, rname, type_sig, d, dx)
            if val == 0:
                print 'native stub found'
                break
            elif val == 1:
                print 'no stub found for dyna lib'
                sys.exit(1)
            # else continue, first native call not found


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

def get_func_start_addr(so, func):

    # use the nm tool to dump the func addrs
    # TODO: find out running the command is ok as opposed to a library call
    cmd_dump_func_addrs = "nm -D " + so
    process = subprocess.Popen(cmd_dump_func_addrs.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]

    # basically grep
    lines = output.split('\n')
    for line in lines:
        if func in line:
            return line.split()[0]

    return ''


def get_sig(so, func, func_start_addr):

    # Capstone class for ARM architectures
    #md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)

    func_start_addr_int = int(func_start_addr, 16)
    func_start_addr_hex = hex(func_start_addr_int)
    so_file = open(so, 'rb')
    so_file_str = so_file.read()
    so_file.close()

    so_file = "./libmonodroid.so"
    core.bin.load (so_file, 0)
    print ("Supported archs: %d"%core.bin.narch)

    if core.bin.narch>1:
        for i in range (0,core.bin.narch):
            core.bin.select_idx (i)
            info = core.bin.get_info ()
            if info:
                print ("%d: %s %s"%(i,info.arch,info.bits))

    # TODO: detect the architecture and set to that. Most will be 32-bit ARM
    # Load file in core
    core.config.set ("asm.arch", "arm");
    core.config.set ("asm.bits", "32");
    #core.config.set ("asm.bits", "64");

    f = core.file_open(so_file, False, 0)
    #core.bin_load (None)
    core.bin_load ("", 0)
    """entry_point = core.num.get("entry0")
    print entry_point
    sys.exit(1)
    
    print ("Entrypoint : 0x%x"%(entry_point))

    for i in xrange(0, 20):
        print ("%s"%(core.disassemble(entry_point+4*i).get_asm()))
    """

    entry_point = func_start_addr_int

    print ("Entrypoint : 0x%x"%(entry_point))

    for i in xrange(0, 20):
        print ("%s"%(core.disassemble(entry_point+4*i).get_asm()))

    #for string in core.bin.get_strings():
    #    print ("0x%x 0x%x "%(string.vaddr, string.paddr))

    #md = Cs(CS_ARCH_X86, CS_MODE_64) this prints instructions but it seems to be ARM

    #CODE = b"\x55\x48\x8b\x05\xb8\x13\x00\x00"
    #print func_start_addr_hex
    #for i in md.disasm(CODE, 0x1000):
    #    print("0x%x:\t%s\t%s" %(i.address, i.mnemonic, i.op_str))

    #sys.exit(0)
    #for (address, size, mnemonic, op_str) in md.disasm_lite(so_file_str, 0xea7c):#func_start_addr_hex):
    #    print("0x%x:\t%s\t%s" %(address, mnemonic, op_str))


def parse_elf(so, func):

    so = 'lib' + so + '.so'

    func_start_addr = get_func_start_addr(so, func)

    if func_start_addr == '':
        print 'stub function not found in .so file'
        sys.exit(1)
    else:
        print 'stub func begins at ' + func_start_addr
        sig = get_sig(so, func, func_start_addr)



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

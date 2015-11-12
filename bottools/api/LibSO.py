#
#   File created by Cory Pruce, Rajiv Kulkarni, and
#   Kumar Vikramjeet on 11/11/2015
#
#   Botanist SO API
#
#   This library gives an interface to the LibSO
#   class, whose sole function is to make a signature
#   out of the stub function of the imported library.

import os
import sys
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

class LibSO(object):
    """
        shared object dyn lib representing a tool
    """

    def __init__(self, so_file_name, apk):

        # use radare2's RCore for lib analysis
        core = RCore()

        # load the file with RBin from r2
        self.jni_on_load_vaddr = self.load_file(core, so_file_name, apk)

        if self.jni_on_load_vaddr == "":
            print "ERROR: library file has no JNI_OnLoad method"
            sys.exit(1)

        self.so_file_name = so_file_name
        self.sig = self.get_sig(core)

        print ("Sig: %s "%(self.sig))

    def print_bin_info(self, rbin):
        print ""
        print ("Get info of %s " % (rbin.get_info().file))
        print ("%s"%((12+len(rbin.file))*'-'))
        print ("Type: %s " % (rbin.get_info().type))
        print ("Bclass: %s " % (rbin.get_info().bclass))
        print ("Rclass: %s " % (rbin.get_info().rclass))
        print ("Machine: %s " % (rbin.get_info().machine))
        print ("Arch: %s " % (rbin.get_info().arch))
        print ("OS: %s " % (rbin.get_info().os))
        print ""


    def tapered_levenshtein(sig1, sig2):
        sig1_mnemonics = sig1.split()
        sig2_mnemonics = sig2.split()
        position = 0
        num_mnemonics = len(sig1_mnemonics) #assumption len(sig1) == len(sig2)
        weight = 1.0 - position/num_mnemonics
        distance = 0.0

        for mn1, mn2 in sig1_mnemonics, sig2_mnemonics:
            if mn1 != mn2:
                distance+=weight

            position+=1
            weight = 1.0 - position/num_mnemonics

        return distance

    def get_sig(self, core):

        # TODO: check magic field for x86 and see if code needs to be tweeked
        
        print ("Creating signature of stub entrypoint: JNI_OnLoad @ address %s"%(hex(self.jni_on_load_vaddr)[:-1]))
        print (51+len("JNI_OnLoad")+len(hex(self.jni_on_load_vaddr)))*'-'

        sig = ""

        # TODO: what if the function ends or transfers control before the first 40
        # instructions? (Maybe check for BL something?)
        for i in xrange(0, 40):
            instr = core.disassemble(self.jni_on_load_vaddr+4*i)
            #print ("%s. %s"%(instr.get_asm(), instr.get_hex()))
            mnemonic = instr.get_asm().split()[0]
            sig += mnemonic + " " # attach to signature
            scale = 16 ## equals to hexadecimal
            num_of_bits = 32 ## size of instruction unless x64
            #print bin(int(instr.get_hex(), scale))[2:].zfill(num_of_bits)

        return sig

    def get_jni_on_load_vaddr(self, rbin):

        for sym in rbin.get_symbols():
            #print sym.name
            if "JNI_OnLoad" in sym.name:
                print sym.name
                return sym.rva

        return ""

    def load_file(self, core, fname, apk):

        # dump so file binary to self.so_file
        self.dump_file(fname, apk)

        path_components = fname.split('/')
        fname = path_components[len(path_components)-1] 

        #print os.path.dirname(os.path.realpath(fname))
        #f = core.file_open(os.path.dirname(str(os.path.realpath(fname)) + '/' + fname), False, 0)
        fname = './test/' + str(fname)
        f = core.file_open(fname, False, 0)


        core.bin_load ("", 0)

        self.print_bin_info(core.bin)

        return self.get_jni_on_load_vaddr(core.bin)


    def dump_file(self, fname, apk):

        # TODO: add option to choose location to dump to and look into not
        # dumping or removing after loaded into RCore

        og_path = fname
       
        path_components = fname.split('/')
        fname = 'test/' + path_components[len(path_components)-1]

        print ("Dumping %s to " % fname)
        print (17+len(fname))*'-'

        try:
            os.remove(fname)
        except OSError:
            pass

        so_file = apk.get_file(og_path)
        fd = open(fname,"w")
        print >> fd, so_file
        fd.close()

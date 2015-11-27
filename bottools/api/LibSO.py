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
import r2pipe
import hashlib
from androguard.core.bytecodes.apk import *

class LibSO(object):
    """
        shared object dyn lib representing a tool
    """

    def __init__(self, so_file_name, apk):

        # set apk parent name
        self.apk_filename = apk.get_filename()

        # dump so_file for further analysis
        self.dump_file(so_file_name, apk)

        # extract name from apk path
        self.so_file_name = so_file_name.split('/')[2]

        r2 = r2pipe.open('test/' + self.so_file_name)

        # build signature from JNI_OnLoad mnemonics
        self.build_signature(r2)

        self.build_hash()

        # build symbol table
        #self.get_symbols(r2)

    def build_hash(self):
        mstr = ''
        for m in self.mnemonics:
            mstr += m

        # set hash
        self.sha1 = hashlib.sha1(mstr).hexdigest()

    def get_symbols(self, r2):
        # get symbols
        funcs = r2.cmd('f').split('\n')
        self.syms = []
        for f in funcs:
            ls = f.split()
            if ls != []:
                [addr, size, name] = ls

                if name[:4] == 'sym.':
                    self.syms.append(name)

    def build_signature(self, r2):

        # create signature from JNI_OnLoad fcn
        try:
            asm_lines = r2.cmd('aa; s sym.JNI_OnLoad; pdf').split('\n')


            self.mnemonics = []

            if asm_lines == '':
                print 'JNI_OnLoad not found'
                return

            for line in asm_lines:
                print line

                if line[0] == '/':
                    # start mnemonic parse next line
                    #print line
                    pass
                elif line[0] == '\\':
                    # end JNI_OnLoad parse
                    instr = line.split()

                    self.mnemonics.append(instr[3])

                    break
                else:
                    # else |, keep parsing
                    instr = line.split()

                    if 'XREF' not in instr:
                        if len(instr[1]) < 3:
                            # conditional, mnemonic is one over
                            self.mnemonics.append(instr[4])
                        elif len(instr[1]) > 3:
                            self.mnemonics.append(instr[3])

        except Exception:
            return


    def dump_file(self, fname, apk):

        og_path = fname

        # dump file to test/
        path_components = fname.split('/')
        fname = 'test/' + path_components[-1]

        print ("\nDumping %s to test/" % fname)
        print (22+len(fname))*'-'

        try:
            os.remove(fname)
        except OSError:
            pass

        so_file = apk.get_file(og_path)
        fd = open(fname,"w")
        print >> fd, so_file
        fd.close()

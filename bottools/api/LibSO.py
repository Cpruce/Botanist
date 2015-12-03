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
from elftools.elf.elffile import ELFFile
from androguard.core.bytecodes.apk import *

def parse_arch(arch):
    if arch == 'EM_X86_64':
        return 'x64'
    elif arch in ('EM_386', 'EM_486'):
        return 'x86'
    elif arch == 'EM_ARM':
        return 'ARM'
    elif arch == 'EM_AARCH64':
        return 'AArch64'
    elif arch == 'EM_MIPS':
        return 'MIPS'
    else:
        return ''

class LibSO(object):
    """
        shared object dyn lib representing a tool
    """

    def __init__(self, so_file_name, apk):

        # set apk parent name
        self.apk_filename = apk.get_filename().split('/')[-1]

        # dump so_file for further analysis
        self.dump_file(so_file_name, apk)

        # extract name from apk path
        self.so_file_name = so_file_name.split('/')[-1]

        with open('test/'+self.so_file_name, 'rb') as f:
            elffile = ELFFile(f)
            self.arch = parse_arch(elffile.header.e_machine)

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

            # use the r2 commands thru r2pipe to analysis, search for
            # JNI_OnLoad, and print the function into asm_lines
            asm_lines = r2.cmd('aa; s sym.JNI_OnLoad; pdf').split('\n')

            # TODO: r2 doesn't translate all x86 correctly. handle errs

            self.mnemonics = []

            # signature will be the length of the function or the first 100 op's
            count = 0
            threshold = 99

            for line in asm_lines:
                
                if line[0] == '/':
                    if 'JNI_OnLoad' not in line:
                        break
                    # start mnemonic parse next line
                    #print line
                    pass
                # end on function limit or threshold
                elif line[0] == '\\' or count == threshold:
                    # end JNI_OnLoad parse
                    instr = line.split()
                    mnemonic = instr[3].strip()
                    self.mnemonics.append(mnemonic)
                    break
                else:
                    # else |, keep parsing
                    instr = line.split()

                    if 'XREF' not in instr:

                        if len(instr[1]) < 3:

                            # conditional, mnemonic is one over
                            mnemonic = instr[4].strip()
                        else:
                            mnemonic = instr[3].strip()

                        if 'invalid' in mnemonic:
                            break

                        self.mnemonics.append(mnemonic)

                count += 1

        except Exception:
            return


    def dump_file(self, fname, apk):

        og_path = fname

        # dump file to test/
        path_components = fname.split('/')
        fname = 'test/' + path_components[-1]

        print ("\n    Dumping %s to test/" % fname)
        print (" "*4) + (18+len(fname))*'-'

        try:
            os.remove(fname)
        except OSError:
            pass

        so_file = apk.get_file(og_path)
        fd = open(fname,"w")
        print >> fd, so_file
        fd.close()

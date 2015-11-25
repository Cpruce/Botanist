import hashlib
from bottools.api.LibSO import LibSO
from androguard.core.bytecodes.apk import *

class APKInfo(object):
    """
        base lass for apk info, focusing on its tools
    """

    def __init__(self, apk_name):

        # use androguard to get apk
        self.apk = APK(apk_name)

        ##### bottools fields #####

        # hash of the apk file
        self.sha1 = hashlib.sha1(self.apk.get_raw()).hexdigest()

        # shared object dynamic library objects that contain signatures
        self.libs = []
        
        for fname in self.apk.get_files():
            
            if fname[:3] == 'lib' and fname[-3:] == '.so':
                lib = LibSO(fname, self.apk) 
                
                # keep only tools directly loaded using JNI_OnLoad
                if lib.mnemonics != []:
                    self.libs.append(lib)


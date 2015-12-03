import hashlib
from bottools.api.LibSO import LibSO
from androguard.core.bytecodes.apk import *

class APKInfo(object):
    """
        base lass for apk info, focusing on its tools
    """

    def __init__(self, apk_name):

        # use androguard to get apk
        apk = APK(apk_name)
        self.apk_name = apk.filename.split("/")[-1]
        self.package = apk.package
        self.permissions = apk.permissions
        ##### bottools fields #####

        # hash of the apk file
        self.sha1 = hashlib.sha1(apk.get_raw()).hexdigest()

        # shared object dynamic library objects that contain signatures
        self.libs = []

        for fname in apk.get_files():

            if fname[:3] == 'lib' and fname[-3:] == '.so':
                lib = LibSO(fname, apk)
                self.libs.append(lib)


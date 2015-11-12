#!/usr/bin/env python

from setuptools import setup, find_packages



def try_build():
    print 'Build started'
    build_ok = True


    try:
        setup(
            name = 'botanist',
            version = '1.0',
            packages = find_packages(),
            scripts = ['bottools/api/APKInfo.py', 'bottools/api/LibSO.py',
                       'bottools/tag/DexTagger.py', 'bottools/tag/ElfTagger.py', 
                       'bottools/classify/Classifier.py', 
                       'bottools/control/Controller.py', ],
            platforms='Cross Platform',
            classifiers = [
                        'Programming Language :: Python :: 2',
                        'Programming Language :: Python :: 3',
                        ],

        )
    except SystemExit, e:
        print repr(e)
        build_ok = False

    if build_ok == True:
        print 'Build success'
    else:
        print 'Build failed'
        #install_requires=['python-mysql', 'androguard',],


try_build()

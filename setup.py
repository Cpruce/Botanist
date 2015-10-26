#!/usr/bin/env python
import sys
from setuptools import setup, find_packages



def try_build():
    print 'Build started'
    build_ok = True


    try:
        setup(
            name = 'botanist',
            version = '1.0',
            packages = find_packages(),
            scripts = ['tagger.py', 'classifier.py', ],
            #install_requires=['python-mysql', 'androguard',],
        )
    except SystemExit, e:
        print repr(e)
        build_ok = False

    if build_ok == True:
        print 'Build success'
    else:
        print 'Build failed'


try_build()

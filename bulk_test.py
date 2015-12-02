#!/usr/bin/python

import os
d = './apks/slides.night-labs.de/apks'
i = 0
for f in os.listdir(d):
    if i >310:
        break
    #print f
    output = os.system("python ./Botanist/bottools/scripts/ElfTagger.py -f " + d + "/" + f)
    for line in str(output).split('\n'):
        print line

    i+=1


# Botanist 
## APK toolchain fingerprinting and clustering program

### About

Botanist is a program to determine the tools that were used to produce an Android Application Package binary. These include IDE's, packers, compilers, and libraries. The program is split into two parts: creating a set of signatures for a given apk and then integrating that data into the stored collection. 

The name Botanist was chosen for several attributes.

1. Brevity
2. Relevance to categorization
3. Homage to growing software 

### Dependencies

Botanist uses:

* Androguard, currently using stable release v2.0 aka version 3.0, for apk/dex analysis
* MySQL for non-volatile storage of clusters
* python-mysql for interaction with past instances and storing purposes


### Components

1. <i> Tagger.py </i> - creates the set of signatures
2. <i> Classifier.py </i> - provides the interface between the Tagger and Controller
3. <i> Controller.py </i> - adds signatures to the db if doesn't already exist and assigns a cluster

### Setup

1. ```sudo python setup.py install```
2. ```python bottools/tag/Tagger.py -f test/Xamarin/com.revengdroid.XamarinHelloWorld.apk | python bottools/classify/Classifier.py -u {USERNAME} -p {PASSWORD}```


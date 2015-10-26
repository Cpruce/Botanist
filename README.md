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

1. <i> tagger.py </i> - this program creates the set of signatures
2. <i> classifier.py </i> - this program adds signatures to the db if doesn't already
   exist and assigns a cluster

### Setup

Go into <i> classifier.py </i> and change the credentials to your login
   information
<c> sudo python setup.py install </c>
<c> python tagger.py -f test/Xamarin/com.revengdroid.XamarinHelloWorld.apk | python classifier.py </c>


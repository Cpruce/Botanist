# Botanist 
## APK toolchain fingerprinting and clustering program

# WORK IN PROGRESS

### About

Botanist is a program to determine the tools that were used to produce an Android Application Package binary. These include IDE's, packers, compilers, and libraries. The program is split into two parts: creating a set of signatures for a given apk and then integrating that data into the stored collection. 

The name Botanist was chosen for several attributes.

1. Brevity
2. Relevance to categorization
3. Homage to growing software 

Ideally, these clusters will be graphically displayed and tools can be viewed
along with variations that exist in the wild. The main function takes in an APK
and says what tools were used, if previously seen. This project assumes data on
several instances and the ability to store instances for future reference.

### Dependencies

Botanist uses:

* Androguard, currently using stable release v2.0 aka version 3.0, for apk/dex analysis
* radare2 python bindings for elf analysis
* MySQL for non-volatile storage of clusters
* python-mysql for interaction with past instances and storing purposes


### Components

#### API

1. <i>APKInfo</i> - contains apk name, architecture, shared object files, and
   the library signatures
2. <i>SOFile</i> - contains information on the shared object file
3. <i>ToolSig</i> - contains a signature of a particular dynamic library, the
   name of that library, and the name of the APK
3. <i> Controller.py </i> - adds signatures to the db if doesn't already exist and assigns a cluster 

#### Scripts

1. <i> Tagging </i> - creates the set of signatures. A simple dex signature can
   be made using <i>DexTagger.py</i>.  However, this does not capture as much information as the first
   method called in the dynamically-loaded library. <i>ElfTagger.py</i>
   continues by dumping the .so files, finding the first call into the library
   after the System.loadLibrary call, and creates a signature based on the
   first 40 opcodes of the initializing method.
2. <i> Classifying </i> - provides the interface between the Tagger and Controller

### Tested Architectures

          
 ARM | ARM64 | x86 | x64 | MIPS
----------------------------------
 initial test |       |     |     |
    

### Setup

1. ```sudo python setup.py install```
2. ```python bottools/tag/ElfTagger.py -f test/Xamarin/com.revengdroid.XamarinHelloWorld.apk | python bottools/classify/Classifier.py -u {USERNAME} -p {PASSWORD}```


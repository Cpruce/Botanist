# Botanist 
## APK toolchain fingerprinting and clustering program

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

## Web Service

If the user's intent is to store lots of APK's and do analyses via a service,
   go to the readme in the webservice directory.

### Dependencies

Botanist uses:

* Androguard - https://github.com/androguard/androguard/releases/tag/v2.0
* r2pipe - pip install r2pipe
* elftools - pip install pyelftools
* MySQL <i>OR</i> MongoDB 
* python-mysql <i>OR</i> pymongo - pip install <i>python_driver</i>

### Components

#### API

1. <i>APKInfo</i> - contains apk name, architecture, shared object files, and
   the library signatures
2. <i>LibSO</i> - contains information on the shared object file, including a
   signature
3. <i> Classifying </i> - provides means for creating relationships between entities

#### Scripts

1. <i>ElfTagger.py</i> - continues by dumping the .so files, finding the first call into the library
   after the System.loadLibrary call, and creates a signature based on the
   opcodes of the initializing method.

#### DB Access

1. <i>MongoController</i>
2. <i>MySQLController</i>

### Install

1. ```sudo python setup.py install```

### Test

1. python bulk_test.py {{APK_DIR}}

## Individual Components

1. TO BE FINISHED: ```python bottools/scripts/ElfTagger.py -f test/Xamarin/com.revengdroid.XamarinHelloWorld.apk | python bottools/control/MongoController.py -a```


# Botanist Visualization
## APK toolchain fingerprinting and clustering webservice

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

Botantist visualization requires:

* Node.js, use npm
* Express.js
* d3.js
* mongoDB
* all of the dependencies that come with the package

### Run

1. npm install
2. npm run

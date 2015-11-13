#!/bin/bash


dir="$(dirname -- $(readlink -fn -- "$0"; echo x))"

db_path=${dir}/data
rm -rf ${db_path}
mkdir -p ${db_path} 

# startup mongo daemon
mongod --dbpath ${dir}/data &

#sleep 30

# "press enter" to bring back prompt
#echo -ne '\n'

# populate database
#mongo db_pop.js

#!/bin/bash

./clear_collections.sh

ps aux | grep 'mongod' | awk '{print $2}' | xargs kill

rm -rf data

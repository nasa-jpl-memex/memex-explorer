#!/usr/bin/env bash

set -o nounset

cd $1
echo "Running from: `pwd`"
./script/start_crawler.sh $2 $3 $4


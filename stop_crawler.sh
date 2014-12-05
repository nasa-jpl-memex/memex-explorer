#!/usr/bin/env bash

set -o nounset

cd $1
echo "Running from: `pwd`"
./script/stop_crawler.sh

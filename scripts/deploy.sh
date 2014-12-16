#!/usr/bin/env bash
export scriptdir=/vagrant/scripts

echo "test for" > /echo.txt # 2112 test, if this file exists on the VM then this script ran

# this only needs to be done once
sudo apt-get update

# Add your deployment scripts here:
sudo $scriptdir/debian.sh
$scriptdir/conda.sh
$scriptdir/supervisor.sh


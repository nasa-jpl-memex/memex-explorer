#!/usr/bin/env bash
export scriptdir=/vagrant/scripts

echo "test for" > /echo.txt # 2112 test, if this file exists on the VM then this script ran

# this only needs to be done once
sudo apt-get update

# Add your deployment scripts here:
sudo $scriptdir/debian.sh
sudo $scriptdir/conda.sh
sudo $scriptdir/supervisor.sh

# TODO make necessary directories
mkdir -p image_space/uploads
mkdir seeds
mkdir models
mkdir configs
mkdir crawls

chmod a+rwX -R image_space
chmod a+rwX -R seeds
chmod a+rwX -R models
chmod a+rwX -R configs
chmod a+rwX -R crawls

ln -s /vagrant/data /data
ln -s /vagrant/UPLOADED_DATA /UPLOADED_DATA

#!/usr/bin/env bash
echo "Installing Debian dependencies"

apt-get -y install git &> /dev/null
apt-get -y install make &> /dev/null
apt-get -y install cmake &> /dev/null
apt-get -y install mc vim &> /dev/null
apt-get -y install supervisor &> /dev/null

# Install a Java runtime enviornment
sudo apt-get -y install openjdk-6-jdk
export JAVA_HOME=/usr/lib/jvm/java-6-openjdk-amd64
echo JAVA_HOME=/usr/lib/jvm/java-6-openjdk-amd64 | sudo tee -a /etc/environment


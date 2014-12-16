#!/usr/bin/env bash


if [ `grep -c '^vagrant:' /etc/passwd` ]; then
    scriptdir=/vagrant/scripts
    pushd $scriptdir/../
    sh home_install.sh
    popd
else
    echo "I AM LOST"
    pushd ../
    sh home_install.sh
    popd
fi


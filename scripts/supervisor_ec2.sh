#!/usr/bin/env bash
scriptdir=/mnt/ebola-tweets/MEMEX_EBOLA/memex-jpl/ebola/scripts

echo "Installing Supervisord dependencies"

service supervisor restart
cp $scriptdir/supervisor_ebola_space_ec2.conf /etc/supervisor/conf.d/ebola_space.conf
supervisorctl reread
supervisorctl update

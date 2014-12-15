#!/usr/bin/env bash
scriptdir=/mnt/ebola-tweets/memex-explorer/scripts

echo "Installing Supervisord dependencies"

service supervisor restart
cp $scriptdir/supervisor_memex_explorer_ec2.conf /etc/supervisor/conf.d/memex_explorer.conf
supervisorctl reread
supervisorctl update

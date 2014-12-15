#!/usr/bin/env bash
scriptdir=/vagrant/scripts

echo "Installing Supervisord dependencies"

service supervisor restart
cp $scriptdir/supervisor_memex_explorer.conf /etc/supervisor/conf.d/memex_explorer.conf
supervisorctl reread
supervisorctl update

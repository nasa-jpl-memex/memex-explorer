#!/usr/bin/env bash
scriptdir=/vagrant/scripts

echo "Installing Supervisord dependencies"

service supervisor restart
cp $scriptdir/supervisor_ebola_space.conf /etc/supervisor/conf.d/ebola_space.conf
supervisorctl reread
supervisorctl update

#!/usr/bin/env bash
scriptdir=/vagrant/scripts

echo "Installing Supervisord dependencies"
PATH=~/anaconda/bin:$PATH
source activate memex-explorer

pushd $scriptdir
mkdir -p supervisord_child_logs
supervisord -c /vagrant/scripts/supervisor_memex_explorer.conf
popd

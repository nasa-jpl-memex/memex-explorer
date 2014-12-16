#!/usr/bin/env bash
scriptdir=/vagrant/scripts

echo "Installing Supervisord dependencies"
PATH=~/anaconda/bin:$PATH
source activate memex-explorer

cp $scriptdir/supervisor_memex_explorer.conf $scriptdir/supervisord.conf
pushd $scriptdir
mkdir -p supervisord_child_logs
supervisord
popd

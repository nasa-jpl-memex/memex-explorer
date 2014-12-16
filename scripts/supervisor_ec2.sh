#!/usr/bin/env bash
scriptdir=/mnt/data/memex-explorer/scripts

echo "Installing Supervisord dependencies"
PATH=~/anaconda/bin:$PATH
source activate memex-explorer

pushd $scriptdir
mkdir -p supervisord_child_logs
supervisord -c /mnt/data/memex-explorer/scripts/supervisor_memex_explorer_ec2.conf
popd

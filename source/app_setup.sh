#!/bin/bash
pushd ../
conda update conda;
conda install conda-env -y;
conda env update --file local-environment.yml;
npm install -g log.io
popd

pushd ../deploy
python logio_settings.py
popd

source activate memex;
python manage.py migrate;

pushd memex
cp settings_files/dev_settings.py settings.py;
popd

source deactivate

#!/bin/bash
pushd ../;
conda update conda -y;
conda install conda-env -y;
conda env update --file environment.yml;
popd;

pushd memex;
cp settings_files/dev_settings.py settings.py;
popd;

source activate memex;
npm install -g log.io
python manage.py migrate;

pushd ../deploy;
python logio_settings.py;
popd;

source deactivate;

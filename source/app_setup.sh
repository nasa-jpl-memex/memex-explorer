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
python manage.py migrate;

source deactivate;

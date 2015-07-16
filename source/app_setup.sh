#!/bin/bash
pushd ../
conda env update --file local-environment.yml;
popd

source activate memex;
python manage.py migrate;

pushd memex
cp settings_files/dev_settings.py settings.py;
popd

source deactivate

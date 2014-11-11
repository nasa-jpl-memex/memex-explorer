 #!/usr/bin/env bash

conda create -n memex-viewer python=2.7 pip ipython --yes
source activate memex-viewer
conda install flask pip pymongo pytables pygments ipython-notebook bokeh requests sqlalchemy numpy pandas psutil unicodecsv blaze dynd-python libdynd h5py pytables multipledispatch datashape toolz cytoolz --yes
conda install -c https://conda.binstar.org/bokeh/channel/dev bokeh --yes
pip install git+https://github.com/ContinuumIO/blaze.git --upgrade
pip install git+https://github.com/ContinuumIO/datashape.git --upgrade --no-deps
pip install flask-sqlalchemy tld sqlalchemy-migrate Flask-WTF flask-mail webhelpers

echo `which python`
python utilities/db_create.py

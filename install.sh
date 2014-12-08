 #!/usr/bin/env bash

if [ ! -d /opt/anaconda ]; then
    wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O /opt/miniconda.sh
    bash /opt/miniconda.sh -b -p /opt/anaconda/
    echo "export PATH=/opt/anaconda/bin/:$PATH" | sudo tee -a /etc/bashrc
    echo "export PATH=/opt/anaconda/bin/:$PATH" | sudo tee -a /etc/environment
    /opt/anaconda/bin/conda config --set always_yes yes
    /opt/anaconda/bin/conda config --add create_default_packages pip --add create_default_packages ipython
    /opt/anaconda/bin/conda update conda --yes
fi

conda create -n memex-explorer python=2.7 pip ipython --yes
source activate memex-explorer
conda install flask pip pymongo pytables pygments ipython-notebook bokeh requests sqlalchemy numpy pandas psutil unicodecsv blaze dynd-python libdynd h5py pytables multipledispatch datashape toolz cytoolz --yes
conda install -c https://conda.binstar.org/bokeh/channel/dev bokeh --yes
pip install git+https://github.com/ContinuumIO/blaze.git --upgrade
pip install git+https://github.com/ContinuumIO/datashape.git --upgrade --no-deps
pip install flask-sqlalchemy tld sqlalchemy-migrate Flask-WTF flask-mail webhelpers

echo `which python`
python utilities/db_create.py

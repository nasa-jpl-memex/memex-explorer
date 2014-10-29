#!/usr/bin/env bash
echo "Installing Anaconda"


if [ ! -d /opt/anaconda ]; then
    wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O /opt/miniconda.sh
    bash /opt/miniconda.sh -b -p /opt/anaconda/
    echo "export PATH=/opt/anaconda/bin/:$PATH" | sudo tee -a /etc/bashrc
    echo "export PATH=/opt/anaconda/bin/:$PATH" | sudo tee -a /etc/environment
    /opt/anaconda/bin/conda config --set always_yes yes
    /opt/anaconda/bin/conda config --add create_default_packages pip --add create_default_packages ipython
    /opt/anaconda/bin/conda update conda --yes
fi

/opt/anaconda/bin/conda install futures
/opt/anaconda/bin/conda install blaze bokeh flask requests sqlalchemy numpy pandas
/opt/anaconda/bin/conda install dynd-python h5py pymongo toolz pytables pygments
/opt/anaconda/bin/conda install -c https://conda.binstar.org/bokeh/channel/dev  bokeh
/opt/anaconda/bin/conda install ipython pip

# weird install problem with installing blaze dev
rm /opt/anaconda/lib/python2.7/site-packages/multipledispatch-0.4.7-py2.7.egg-info
/opt/anaconda/bin/conda install -c blaze blaze

#pip
/opt/anaconda/bin/pip install  Flask-SQLAlchemy flask-wtf sqlalchemy-migrate flask-mail webhelpers
/opt/anaconda/bin/pip install psutil
/opt/anaconda/bin/pip install git+https://github.com/ContinuumIO/blaze.git --upgrade

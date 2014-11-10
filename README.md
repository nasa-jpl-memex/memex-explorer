memex-viewer
============

Viewers for statistics and dashboarding of Domain Search Engine data

# Usage
 
 ```
usage: run.py [-h] [-s]

EBOLA DATA SPACE

optional arguments:
  -h, --help  show this help message and exit
  -s, --show  Auto-raise app in a browser window
```

## Testing

`python run_tests.py`

## Install

```
wget http://bit.ly/miniconda
bash Miniconda-latest-Linux-x86_64.sh
bash install.sh
```

## Dependencies

### conda
- blaze
- flask
- pip
- libdynd
- dynd-python
- h5py
- pymongo
- toolz
- pytables
- pygments
- unicodecsv

### Conda Channels
- conda install -c https://conda.binstar.org/bokeh/channel/dev  bokeh

### Pip
- flask-sqlalchemy
- sqlalchemy-migrate
- Flask-WTF
- flask-mail
- webhelpers
- tld



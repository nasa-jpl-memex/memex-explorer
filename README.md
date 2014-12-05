memex-explorer
============

# Install

## (mini)conda
```
wget http://bit.ly/miniconda
bash Miniconda-latest-Linux-x86_64.sh
bash install.sh
```

## Dependencies
```
conda env create -n memex -f environment.yml
```

# Usage
 
```
usage: run.py [-h] [-s]

MEMEX Explorer

optional arguments:
  -h, --help  show this help message and exit
  -s, --show  Auto-raise app in a browser window
```
# Testing

`python run_tests.py`


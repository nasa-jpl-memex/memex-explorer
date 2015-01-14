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


# Deploying on EC2

Everything should **just work** by running:

```bash
./deploy.sh
```

## Deploy Setup

 - conda bootstrap: conda.sh .  Everything is pushed into `install.sh` and `environment.yml` file for conda and env setupd
 - debian.sh: git, supervisor, make, JAVA
 - supervisor_ec2.sh: moves conf files and calls supervisor -- conf file is hard-coded to use env setup in `environment.yml` 

## Docker Build Instructions

### OSX
```
export DOCKER_TLS_VERIFY=1
```

```
docker build -t memex_explorer .
docker run -p 80:5000 memex_explorer
```
Point browser at `DOCKER_HOST` -- for example: `http://192.168.59.103`

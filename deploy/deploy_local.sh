export HOSTNAME='example.com'
export IP_ADDR='0.0.0.0'
export ROOT_MEMEX_PORT='8000'
export LOCAL_SETTINGS_PATH='~/memex-explorer/source/memex/local_settings.py'

sudo add-apt-repository -y ppa:keithw/mosh
sudo apt-get update -y
sudo apt-get install -y nginx docker git silversearcher-ag python-software-properties mosh tig

wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
chmod +x ./Miniconda-latest-Linux-x86_64.sh
./Miniconda-latest-Linux-x86_64.sh -b
export PATH="~/miniconda/bin:/usr/bin:$PATH"
echo 'export PATH="~/miniconda/bin:/usr/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
~/miniconda/bin/conda env update --name root --file ~/memex-explorer/environment.yml
~/miniconda/bin/python ~/memex-explorer/source/manage.py migrate

~/miniconda/bin/python ~/memex-explorer/source/manage.py refresh_nginx

chmod +x ~/memex-explorer/deploy/install-docker.sh
~/memex-explorer/deploy/install-docker.sh
sudo docker pull elasticsearch
sudo docker pull continuumio/tika
sudo docker pull continuumio/kibana

echo 'alias dj="~/miniconda/bin/python ~/memex-explorer/source/manage.py"' >> ~/.bashrc
redis-server && celery -A ~/memex-explorer/source/memex worker && dj runserver 0.0.0.0:$ROOT_PORT

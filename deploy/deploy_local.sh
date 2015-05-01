export HOSTNAME='example.com'
export IP_ADDR='0.0.0.0'
export ROOT_MEMEX_PORT='8000'
export LOCAL_SETTINGS_PATH='~/memex-explorer/source/memex/local_settings.py'

sudo add-apt-repository -y ppa:keithw/mosh
sudo apt-get update -y
sudo apt-get install nginx docker git silversearcher-ag python-software-properties mosh tig

wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
chmod +x ./Miniconda-latest-Linux-x86_64.sh
./Miniconda-latest-Linux-x86_64.sh -b
export PATH="~/miniconda/bin:/usr/bin:$PATH"
echo 'export PATH="~/miniconda/bin:/usr/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
~/miniconda/bin/conda env update --name root --file ~/memex-explorer/environment.yml
echo "ROOT_PORT = '$ROOT_MEMEX_PORT'" >> $LOCAL_SETTINGS_PATH
echo "IP_ADDR = '$IP_ADDR'" >> $LOCAL_SETTINGS_PATH
echo "HOSTNAME = '$HOSTNAME'" >> $LOCAL_SETTINGS_PATH
~/miniconda/bin/python ~/memex-explorer/source/manage.py migrate

#TODO might fail here.
~/miniconda/bin/python ~/memex-explorer/source/manage.py generate_initial_nginx  "~/memex-explorer/source/base/deploy_templates/nginx-reverse-proxy.conf.jinja2" "~/memex-explorer/deploy/initial_nginx.conf"


sudo cp ~/memex-explorer/deploy/initial_nginx.conf /etc/nginx/sites-enabled/default
sudo service nginx restart

chmod +x ~/memex-explorer/install-docker.sh
~/memex-explorer/install-docker.sh
sudo docker pull elasticsearch
sudo docker pull continuumio/tika
sudo docker pull continuumio/kibana

echo 'alias dj=\"~/miniconda/bin/python ~/memex-explorer/source/manage.py\"' >> ~/.bashrc
redis-server && celery -A ~/memex-explorer/source/memex worker && dj runserver 0.0.0.0:$ROOT_PORT

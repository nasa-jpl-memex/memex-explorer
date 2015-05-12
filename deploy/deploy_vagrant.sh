export HOSTNAME='example.com'
export IP_ADDR='0.0.0.0'
export ROOT_MEMEX_PORT='8000' #if you change this it must be updated in Vagrantfile as well
export LOCAL_SETTINGS_PATH='/vagrant/source/memex/local_settings.py'
export HOME=/home/vagrant

sudo add-apt-repository -y ppa:keithw/mosh
sudo apt-get update -y
sudo apt-get install -y nginx docker git silversearcher-ag python-software-properties mosh tig

wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
chmod +x ./Miniconda-latest-Linux-x86_64.sh
./Miniconda-latest-Linux-x86_64.sh -b -f
/home/vagrant/miniconda/bin/conda env create --name memex --file /vagrant/environment.yml

export PATH="/home/vagrant/miniconda/envs/memex/bin:/usr/bin:$PATH"
echo 'export PATH="/home/vagrant/miniconda/envs/memex/bin:/usr/bin:$PATH"' >> /home/vagrant/.bashrc
source /home/vagrant/.bashrc
export PYTHON=/home/vagrant/envs/memex/bin/python

ln -s /vagrant/source/memex/settings_files/deploy_settings.py /vagrant/source/memex/settings.py
$PYTHON /vagrant/source/manage.py migrate

echo 'yes' | $PYTHON /vagrant/source/manage.py collectstatic
$PYTHON /vagrant/source/manage.py refresh_nginx
$PYTHON /vagrant/source/manage.py create_apps_Tika_ES_Kibana

chmod +x /vagrant/deploy/install-docker.sh
/vagrant/deploy/install-docker.sh
sudo ln -s /home/vagrant/miniconda/bin/docker-compose /bin/docker-compose
sudo docker pull elasticsearch
sudo docker pull continuumio/tika
sudo docker pull continuumio/kibana

echo 'alias dj="$PYTHON /vagrant/source/manage.py"' >> /home/vagrant/.bashrc

cd /vagrant/source/
/sbin/start-stop-daemon --chuid vagrant --background --oknodo --start --exec $(which redis-server)
/sbin/start-stop-daemon --chuid vagrant --background --oknodo --start --exec $(which celery) -- --workdir="/vagrant/source" -A memex worker


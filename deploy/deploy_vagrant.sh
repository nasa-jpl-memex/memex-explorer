export HOSTNAME='example.com'
export IP_ADDR='0.0.0.0'
export ROOT_MEMEX_PORT='8000'
export LOCAL_SETTINGS_PATH='/vagrant/source/memex/local_settings.py'
export HOME=/home/vagrant

sudo add-apt-repository -y ppa:keithw/mosh
sudo apt-get update -y
sudo apt-get install -y nginx docker git silversearcher-ag python-software-properties mosh tig

wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
chmod +x ./Miniconda-latest-Linux-x86_64.sh
./Miniconda-latest-Linux-x86_64.sh -b -f
export PATH="/home/vagrant/miniconda/bin:/usr/bin:$PATH"
echo 'export PATH="/home/vagrant/miniconda/bin:/usr/bin:$PATH"' >> /home/vagrant/.bashrc
source /home/vagrant/.bashrc
/home/vagrant/miniconda/bin/conda env update --name root --file /vagrant/environment.yml
ln -s /vagrant/source/memex/settings_files/deploy_settings.py /vagrant/source/memex/settings.py
/home/vagrant/miniconda/bin/python /vagrant/source/manage.py migrate

echo 'yes' | /home/vagrant/miniconda/bin/python /vagrant/source/manage.py collectstatic
/home/vagrant/miniconda/bin/python /vagrant/source/manage.py refresh_nginx
/home/vagrant/miniconda/bin/python /vagrant/source/manage.py create_apps_Tika_ES_Kibana

chmod +x /vagrant/deploy/install-docker.sh
/vagrant/deploy/install-docker.sh
sudo ln -s /home/vagrant/miniconda/bin/docker-compose /bin/docker-compose
sudo docker pull elasticsearch
sudo docker pull continuumio/tika
sudo docker pull continuumio/kibana

echo 'alias dj="/home/vagrant/miniconda/bin/python /vagrant/source/manage.py"' >> /home/vagrant/.bashrc

cd /vagrant/source/
/sbin/start-stop-daemon --chuid vagrant --background --oknodo --start --exec $(which redis-server)
/sbin/start-stop-daemon --chuid vagrant --background --oknodo --start --exec $(which celery) -- --workdir="/vagrant/source" -A memex worker
/home/vagrant/miniconda/bin/python ./manage.py runserver 0.0.0.0:8000

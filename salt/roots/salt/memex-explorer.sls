/vagrant/source/memex/settings.py:
  file.copy:
    - source: /vagrant/source/memex/settings_files/deploy_settings.py

LOCAL_PATH:
  file.append:
    - name: /home/vagrant/.bashrc
    - text: export PATH="/home/vagrant/miniconda/envs/memex/bin:$PATH"

local_settings_path:
   environ.setenv:
     - name: LOCAL_SETTINGS_PATH
     - value: /vagrant/source/memex/local_settings.py


# TODO: The create_apps_Tika_ES_Kibana is not idempotent.  This needs
# to be fixed or the command needs to be protected so that it only
# executes when the applications need to be created.
# As a workaround, the SQL database is currently reset on each provision.

reset:
  cmd.run:
    - name: |
          rm /vagrant/source/db.sqlite3

migrate:
  cmd.run:
    - name: |
        /home/vagrant/miniconda/envs/memex/bin/python /vagrant/source/manage.py migrate
    - cwd: /home/vagrant
    - user: vagrant
    - require:
        - sls: conda-memex

collectstatic:
  cmd.run:
    - name: |
        echo yes | /home/vagrant/miniconda/envs/memex/bin/python /vagrant/source/manage.py collectstatic
    - cwd: /home/vagrant
    - user: vagrant
    - require:
        - sls: conda-memex

refresh_nginx:
  cmd.run:
    - name: |
        /home/vagrant/miniconda/envs/memex/bin/python /vagrant/source/manage.py refresh_nginx
    - cwd: /home/vagrant
    - user: vagrant
    - require:
        - sls: conda-memex

create_apps:
  cmd.run:
    - name: |
        /home/vagrant/miniconda/envs/memex/bin/python /vagrant/source/manage.py create_apps_Tika_ES_Kibana
    - cwd: /home/vagrant
    - user: vagrant
    - require:
        - sls: conda-memex

/bin/docker-compose:
  file.copy:
    - source: /home/vagrant/miniconda/envs/memex/bin/docker-compose

docker-containers:
  cmd.run:
    - name: |
         docker pull elasticsearch
         docker pull continuumio/tika
         docker pull continuumio/kibana
    - require:
        - pkg: docker.io

redis-server:
  cmd.run:
    - name: /sbin/start-stop-daemon --chuid vagrant --background --oknodo --start --exec /home/vagrant/miniconda/envs/memex/bin/redis-server
    - cwd: /vagrant/source
    - require:
        - sls: conda-memex

celery:
  cmd.run:
    - name: /sbin/start-stop-daemon --chuid vagrant --background --oknodo --start --exec /home/vagrant/miniconda/envs/memex/bin/celery  -- --workdir="/vagrant/source" -A memex worker
    - cwd: /vagrant/source
    - require:
        - sls: conda-memex

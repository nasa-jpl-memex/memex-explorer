conda-memex:
  cmd.run:
    - name: |
        /home/vagrant/miniconda/bin/conda env create --name memex --file /vagrant/environment.yml
    - unless: test -e /home/vagrant/miniconda/envs/memex
    - cwd: /home/vagrant
    - user: vagrant
    - require:
        - sls: miniconda
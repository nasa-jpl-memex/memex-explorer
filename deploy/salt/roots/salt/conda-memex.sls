remove-old-env:
  cmd.run:
    - name: |
        /home/vagrant/miniconda/bin/conda env remove --name memex
    - onlyif: test -e /home/vagrant/miniconda/envs/memex
    - cwd: /home/vagrant
    - user: vagrant
    - require:
        - sls: miniconda

conda-memex:
  cmd.run:
    - name: |
        /home/vagrant/miniconda/bin/conda env create --name memex --file /vagrant/environment.yml
    - cwd: /home/vagrant
    - user: vagrant
    - require:
        - sls: miniconda

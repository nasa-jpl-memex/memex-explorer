miniconda-download:
  cmd.run:
    - name: |
        wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
        chmod +x ./Miniconda-latest-Linux-x86_64.sh
        ./Miniconda-latest-Linux-x86_64.sh -b -f
    - unless: test -e /home/vagrant/miniconda
    - cwd: /home/vagrant
    - user: vagrant
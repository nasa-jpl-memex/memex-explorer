docker.io-installed:
  pkg.installed:
    - name: docker.io

docker-io-running:
  service.running:
    - name: docker.io
    - require:
        - pkg: docker.io

docker-py:
  pip.installed:
    - name: docker-py == 0.5.0
    - reload_modules: True

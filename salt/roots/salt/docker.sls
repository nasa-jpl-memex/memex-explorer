docker.io:
  pkg.installed:
    - name: docker
    - version: 1.5-1

docker-py:
  pip.installed:
    - name: docker-py == 0.5.0
    - reload_modules: True

docker-compose:
  pip.installed:
    - name: docker-compose == 1.2

docker.io:
  pkg.installed:
    - name: docker.io
  service:
    - running

docker-py:
  pip.installed:
    - name: docker-py == 0.5.0
    - reload_modules: True

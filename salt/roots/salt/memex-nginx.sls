/etc/nginx/sites-enabled/default:
  file.copy:
    - force: True
    - makedirs: True
    - source: /vagrant/deploy/dockerless/default

nginx:
  pkg:
    - installed
  service:
    - running
    - watch:
        - pkg: nginx
        - file: /etc/nginx/sites-enabled/default



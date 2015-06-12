/etc/nginx/sites-enabled/default:
  file.copy:
    - force: True
    - makedirs: True
    - source: /vagrant/deploy/nginx.conf

/etc/nginx/.htpasswd:
  file.copy:
    - force: True
    - makedirs: True
    - source: /vagrant/deploy/dot-htpasswd

nginx:
  pkg:
    - installed
  service:
    - running
    - watch:
        - pkg: nginx
        - file: /etc/nginx/sites-enabled/default



nginx:
  pkg:
    - installed

/etc/nginx/sites-enabled/default:
  file.copy:
    - source: /vagrant/deploy/dockerless/default

reload:
  nginx.signal

# npm-gyp fails if "node" doesn't resolve to nodejs.  This fixes that issue
nodejs-legacy:
  pkg.installed

npm:
  pkg.installed:
    - require:
        - pkg: nodejs-legacy

# npm.installed does NOT do the right thing here, hardcoding an install
logio:
  cmd.run:
    - name: "sudo npm install -g log.io"
    - require:
      - pkg: npm


log.io-harvester-config:
  file.managed:
    - name: /home/vagrant/.log.io/harvester.conf
    - contents: |
        exports.config = {
          nodeName: "application_server",
          logStreams: {
            nutch: [
            "/<anaconda_location>/envs/<environment_name>/lib/nutch/logs/hadoop.log"
            ]
          },
          server: {
            host: '0.0.0.0',
            port: 28777
          }
        }

log.io-harvester-service-config:
  file.managed:
    - name: /etc/init/log.io-harvester.conf
    - contents: |
        description "start log.io harvester"
        start on runlevel [2345]
        stop on runlevel [016]
        respawn
        
        exec su -s /bin/sh -c 'exec "$0" "$@"' vagrant -- /usr/local/bin/log.io-harvester

log.io-server-service-config:
  file.managed:
    - name: /etc/init/log.io-server.conf
    - contents: |
        description "start log.io server"

        start on runlevel [2345]
        stop on runlevel [016]
        respawn
        
        exec su -s /bin/sh -c 'exec "$0" "$@"' vagrant -- /usr/local/bin/log.io-server
        
log.io-harvester:
  service.running

log.io-server:
  service.running
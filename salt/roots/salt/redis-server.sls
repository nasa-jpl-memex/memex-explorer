install-redis-server:
  pkg.installed:
    - name: redis-server

run-redis-server:
  service.running:
    - name: redis-server
    - require:
        - pkg: redis-server

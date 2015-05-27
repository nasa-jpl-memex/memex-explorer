elasticsearch-pulled:
  docker.pulled:
    - name: elasticsearch
    - image: elasticsearch
    - tag: latest
    - require:
        - sls: docker

tika-pulled:
  docker.pulled:
    - name: continuumio/tika
    - image: continuumio/tika
    - tag: latest
    - require:
        - sls: docker

kibana-pulled:
  docker.pulled:
    - name: continuumio/kibana
    - image: continuumio/kibana
    - tag: latest
    - require:
        - sls: docker

elasticsearch-running:
  cmd.run:
    - name: docker run -d -p 9200:9200 -p 9300:9300 -v /home/ubuntu/memex-explorer/source/container_volumes/elasticsearch/data:/data --name=elasticsearch elasticsearch
    - unless: docker ps | grep elasticsearch
    - require:
        - docker: elasticsearch-pulled

tika-running:
  cmd.run:
    - name: docker run -d -p 9998:9998 continuumio/tika
    - unless: docker ps | grep continuumio/tika
    - require:
        - docker: tika-pulled

kibana-running:
  cmd.run:
    - name: docker run -d -p 9999:80 -e KIBANA_SECURE=false --link elasticsearch:es  continuumio/kibana
    - unless: docker ps | grep continuumio/kibana
    - require:
        - docker: kibana-pulled

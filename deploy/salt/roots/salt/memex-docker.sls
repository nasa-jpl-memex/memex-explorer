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
    - name: docker run -d -p 9200:9200 -p 9300:9300 -v /vagrant/source/container_volumes/elasticsearch/data:/data --name=elasticsearch_1 elasticsearch
    - unless: docker start elasticsearch_1
    - require:
        - docker: elasticsearch-pulled

tika-running:
  cmd.run:
    - name: docker run -d -p 9998:9998 --name tika_1 continuumio/tika
    - unless: docker start tika_1
    - require:
        - docker: tika-pulled

kibana-running:
  cmd.run:
    - name: docker run -d -p 9999:80 -e KIBANA_SECURE=false --link elasticsearch_1:es --name kibana_1 continuumio/kibana
    - unless: docker start kibana_1
    - require:
        - docker: kibana-pulled

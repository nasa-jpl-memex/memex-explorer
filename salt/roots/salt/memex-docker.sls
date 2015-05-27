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
  docker.running:
    - image: "elasticsearch:latest"
    - name: "continuumio/elasticsearch"
    - ports:
        - "9200/tcp":
            HostIp: ""
            HostPort: "9200"
        - "9300/tcp":
            HostIp: ""
            HostPort: "9300"
    - volumes:
        - /home/ubuntu/memex-explorer/source/container_volumes/elasticsearch/data: /data
    - require:
        - docker: elasticsearch-pulled

tika-running:
  docker.running:
    - name: "continuumio/tika"
    - image: "continuumio/tika:latest"
    - ports:
        - "9998/tcp":
            HostIp: ""
            HostPort: "9998"
    - require:
        - docker: tika-pulled

kibana-running:
  docker.running:
    - image: "continuumio/kibana:latest"
    - name: "continuumio/kibana"
    - ports:
        - "80/tcp":
            HostIp: ""
            HostPort: "9999"
    - environment:
        - KIBANA_SECURE: false
    - links:
        - elasticsearch_1: es
    - require:
        - docker: kibana-pulled

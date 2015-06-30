tad-pulled:
  docker.pulled:
    - name: autonlab/tad
    - image: autonlab/tad
    - tag: latest
    - require:
        - sls: docker

tad-running:
  cmd.run:
    - name: docker run -d -p 5000:5000 --name tad_1 autonlab/tad
    - unless: docker start tad_1
    - require:
        - docker: tad-pulled

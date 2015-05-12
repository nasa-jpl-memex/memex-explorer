#######################################
Integrating additional apps with docker
#######################################

Project: a memex-explorer project as shown in the interface
App: an application like elasticsearch, kibana, or tika that can be spun up in a...
Container: A particular docker container running an app for a paticular project.

When a project is created, a container is created for every app by
1) Instantiating container objects in a celery task kicked off by a post-save signal
   2) Generating a docker-compose.yml from the container objects and running `docker-compose up`.
      3) Generating an nginx conf from the container objects which expose a port publicly at a certain URL, then restarting nginx.

         To integrate a service, first create a docker image for it and then write out the yml that would be added to the docker compose file to spin it up. See intro to docker-compose & docker-compose.yml reference. Then, when you start up the memex-explorer app, create database entries for that in the models App, AppPort, AppLink, and VolumeMount. See the command to create those entries for tika, kibana, and elasticsearch as a reference.

         To get started on this now without worrying about the hard-coding, you could simply add on to create_apps_Tika_ES_Kibana.py. Then, when a project is created, 4 containers will be created: the ones for your container and the vestigial ones for tika, elasticsearch, and kibana.


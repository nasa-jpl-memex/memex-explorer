########## DON'T MODIFY THIS SECTION, SCROLL DOWN ###########
# The next configurations do some configuring that can take a
# bit of time, so best make modifications AFTER them to allow
# utilization of cached steps.
#
# Note: As of 2015/03/05 this is Ubuntu 14.04.
FROM ubuntu
MAINTAINER Aron Ahmadia <aahmadia@continuum.io>

#------------ Install development software --------------#
USER root
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get install -y \
    curl \
    g++ \
    git \
    libssl-dev \
    make \
    nginx \
    openjdk-7-jdk \
    pkg-config \
    rabbitmq-server \
    wget

RUN groupadd -r explorer -g 433 && \
    useradd -u 431 -m -r -g explorer -d /home/explorer -s /bin/bash -c "Docker image user" explorer && \
chown -R explorer:explorer /home/explorer
RUN adduser explorer sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER explorer

WORKDIR /home/explorer
RUN wget https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
RUN bash ./Miniconda-latest-Linux-x86_64.sh -b
RUN git clone https://github.com/memex-explorer/memex-explorer

WORKDIR /home/explorer/memex-explorer/

WORKDIR /home/explorer/memex-explorer
ENV PATH /home/explorer/miniconda2/bin:$PATH
RUN conda update conda -y
RUN conda install conda-env -y
RUN conda env update

WORKDIR /home/explorer/memex-explorer/source/memex
RUN cp settings_files/dev_settings.py settings.py

WORKDIR /home/explorer/memex-explorer/source
#replaces source activate... sorta
ENV PATH /home/explorer/miniconda2/envs/memex/bin:$PATH
ENV CONDA_DEFAULT_ENV memex
ENV CONDA_ENV_PATH /home/explorer/miniconda2

# move these into another environment.yaml?  Or better, apply them as a patch?
RUN conda install -c memex ddt
# TAD dependencies
RUN pip install celery fisher elasticsearch flask flask_restful

# ready for deployment
RUN python manage.py migrate
RUN python manage.py collectstatic -v0 --noinput

# Install elasticdump
RUN npm install -g elasticdump

#------------- Pull TAD software --------------#
USER root
RUN mkdir -p /service/build
WORKDIR /service/build
RUN git clone https://github.com/autonlab/tad.git

# Build and install TAD library.
RUN ln -s /service/build/tad/service /service/tad
RUN mkdir /service/tad/config

# Explorer configuration
USER explorer
COPY supervisord.conf /home/explorer/memex-explorer/source/supervisord.conf
COPY docker_settings.py /home/explorer/memex-explorer/source/memex/settings.py
# patched in
WORKDIR /home/explorer/memex-explorer
RUN conda install markdown
RUN markdown_py CHANGES.md > source/base/changes.html
WORKDIR /home/explorer/memex-explorer/docs
RUN make html
RUN mv build/html ../source/base/static/docs

# TAD configuration
COPY tad.cfg /service/tad/config/tad.cfg


# UNCOMMENT THIS SECTION TO PRELOAD THE ELASTICSEARCH INSTANCE
# ------------------------------------------------------------- #

# Now bring over elasticsearch index data
# COPY elasticdump.json /home/explorer/elasticdump.json

# Load data
# Elasticsearch data
# COPY populate_elasticsearch.sh /home/explorer/populate_elasticsearch.sh
# WORKDIR /home/explorer
# RUN /bin/bash ./populate_elasticsearch.sh
# ------------------------------------------------------------- #


# ------------------------------------------------------------- #
# UNCOMMENT THIS SECTION TO PRELOAD CRAWL DATA
# Crawl data
# COPY resources /home/explorer/memex-explorer/source/resources/
# ------------------------------------------------------------- #


# ------------------------------------------------------------- #
# UNCOMMENT THIS SECTION TO PRELOAD SQL DATABASE
# SQLite (Django)
# COPY db.sqlite3 /home/explorer/memex-explorer/source/db.sqlite3
# ------------------------------------------------------------- #

# TAD run script
COPY tad_run /home/explorer/miniconda2/envs/memex/bin/tad

COPY nginx.conf /etc/nginx/sites-enabled/default
# uncomment these to install secrets into the container
# COPY secrets/nginx.crt /etc/nginx/ssl/nginx.crt
# COPY secrets/nginx.key /etc/nginx/ssl/nginx.key
# COPY secrets/htpasswd /etc/nginx/htpasswd

# Permissions clean-up
USER root
RUN chown -R explorer /service
RUN chown -R explorer /home/explorer/memex-explorer/source
RUN chmod +x /home/explorer/miniconda2/envs/memex/bin/tad
RUN chown -R explorer /home/explorer/miniconda2/envs/memex/bin/tad

##################### INSTALLATION END #####################

# Expose the default ports
EXPOSE 80
EXPOSE 443

# Set default container command
USER explorer
WORKDIR /home/explorer/memex-explorer/source
ENV HTTP_PROTOCOL http
ENV WS_PROTOCOL ws
ENV INLINE 1
ENTRYPOINT "supervisord"
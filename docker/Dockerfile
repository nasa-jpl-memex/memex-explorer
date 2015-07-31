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
    openjdk-7-jdk \
    pkg-config \
    wget

RUN groupadd -r explorer -g 433 && \
    useradd -u 431 -m -r -g explorer -d /home/explorer -s /bin/bash -c "Docker image user" explorer && \
chown -R explorer:explorer /home/explorer

USER explorer

WORKDIR /home/explorer
RUN wget https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
RUN bash ./Miniconda-latest-Linux-x86_64.sh -b
RUN git clone https://github.com/memex-explorer/memex-explorer

WORKDIR /home/explorer/memex-explorer/
RUN git checkout origin/ahmadia/tad_integration_master

WORKDIR /home/explorer/memex-explorer
ENV PATH /home/explorer/miniconda/bin:$PATH
RUN conda update conda -y
RUN conda install conda-env -y
RUN conda env update --file local-environment.yml

WORKDIR /home/explorer/memex-explorer/source/memex
RUN cp settings_files/dev_settings.py settings.py

WORKDIR /home/explorer/memex-explorer/source
#replaces source activate... sorta
ENV PATH /home/explorer/miniconda/envs/memex/bin:$PATH
ENV CONDA_DEFAULT_ENV memex
ENV CONDA_ENV_PATH /home/explorer/miniconda
RUN npm install -g log.io
RUN python manage.py migrate

WORKDIR /home/explorer/memex-explorer/deploy
RUN python logio_settings.py

# Need a special supervisord.conf that knows how to bind to 0.0.0.0
COPY supervisord.conf /home/explorer/memex-explorer/source/supervisord.conf

# Now bring over elasticsearch index data
COPY elasticdump.json /home/explorer/elasticdump.json

# Install elasticdump
RUN npm install -g elasticdump

# Load data
# Elasticsearch data
COPY populate_elasticsearch.sh /home/explorer/populate_elasticsearch.sh
WORKDIR /home/explorer
RUN /bin/bash ./populate_elasticsearch.sh
# Crawl data 
COPY resources /home/explorer/memex-explorer/source/resources/
# SQLite (Django)
COPY db.sqlite3 /home/explorer/memex-explorer/source/db.sqlite3

# Permissions clean-up
USER root
RUN chown -R explorer /home/explorer/memex-explorer/source

##################### INSTALLATION END #####################

# Expose the default ports
EXPOSE 8000
EXPOSE 9200
EXPOSE 9300
EXPOSE 5601
EXPOSE 8084

# Set default container command
USER explorer
WORKDIR /home/explorer/memex-explorer/source
ENTRYPOINT "supervisord"

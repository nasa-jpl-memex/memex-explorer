FROM continuumio/miniconda

MAINTAINER Benjamin Zaitlen <ben.zaitlen@continuum.io>

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install openjdk-7-jdk curl


RUN export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64 | tee -a /etc/bashrc
RUN echo JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64 | tee -a /etc/environment

RUN conda update conda conda-env

RUN conda install -c memex solr --yes
EXPOSE 8983

CMD ["solr", "-f", "-V", "-d", "/opt/conda/solr_pkg"]

FROM ubuntu:14.04

MAINTAINER Benjamin Zaitlen <ben.zaitlen@continuum.io>

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install git && \
    apt-get -y install make && \
    apt-get -y install cmake && \
    apt-get -y install mc vim && \
    apt-get -y install openjdk-6-jdk

RUN apt-get -y install wget bzip2

RUN export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64 | sudo tee -a /etc/bashrc
RUN echo JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64 | sudo tee -a /etc/environment

# Set environment variables.
ENV HOME /root

# Define working directory.
WORKDIR /root
RUN echo 'export PATH=/root/anaconda/bin:$PATH' > /etc/profile.d/conda.sh

RUN wget --quiet http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /root/anaconda && \
    rm miniconda.sh

ENV PATH /root/anaconda/bin:$PATH

RUN conda config --set always_yes yes
RUN conda config --add create_default_packages pip --add create_default_packages ipython
RUN conda update conda
RUN conda install pip

RUN git clone https://github.com/ContinuumIO/memex-explorer.git

# Set the default directory where CMD will execute
WORKDIR /root/memex-explorer

# installs memex-explorer conda env (all dependencies)
RUN bash home_install.sh

# Run the server
CMD ["/root/anaconda/envs/memex-explorer/bin/python", "run.py"]

# Expose ports
EXPOSE 80
EXPOSE 5000

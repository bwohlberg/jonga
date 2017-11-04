FROM andrewosh/binder-base

# This Dockerfile based on binder-project/example-dockerfile-two

MAINTAINER Brendt Wohlberg <brendt@ieee.org>

USER root

# Add dependency
RUN apt-get update
RUN apt-get install -y python-pygraphviz

USER main

# Install requirements
# RUN /home/main/anaconda/envs/python3/bin/pip install -r requirements.txt
# RUN /home/main/anaconda/envs/python3/bin/pip install pygraphviz

# Install jonga
RUN /home/main/anaconda/envs/python3/bin/python setup.py install

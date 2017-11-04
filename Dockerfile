FROM andrewosh/binder-base

# This Dockerfile based on binder-project/example-dockerfile-two

MAINTAINER Brendt Wohlberg <brendt@ieee.org>

USER root

# Add dependency
RUN apt-get update
RUN apt-get install -y python-pygraphviz

USER main

# Install requirements
RUN /home/main/anaconda/envs/python3/bin/pip install matplotlib

# The notebooks should be run from the current version of jonga in the
# GitHub repo, but since the correct configuration for mybinder.org is
# not documented, for now we just install the latest release using pip
RUN /home/main/anaconda/envs/python3/bin/pip install jonga

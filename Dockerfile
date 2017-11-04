FROM andrewosh/binder-base

# This Dockerfile based on binder-project/example-dockerfile-two

MAINTAINER Brendt Wohlberg <brendt@ieee.org>

USER root

# Add dependency
RUN apt-get update
RUN apt-get install -y python-pygraphviz

USER main

FROM debian:jessie

MAINTAINER Ben Rowland "browland@partners.org"

# set up neurodebian package repositories
RUN echo 'deb http://neuro.debian.net/debian jessie main contrib non-free' > /etc/apt/sources.list.d/neurodebian.sources.list
RUN echo 'deb http://neuro.debian.net/debian data main contrib non-free' >> /etc/apt/sources.list.d/neurodebian.sources.list
RUN apt-key adv --recv-keys --keyserver pgp.mit.edu 0xA5D32F012649A5A9

# install fsl
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get -y install fsl-5.0-core

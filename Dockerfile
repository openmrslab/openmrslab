FROM jupyter/scipy-notebook

MAINTAINER Ben Rowland "browland@partners.org"

USER root

# set up neurodebian package repositories
RUN echo 'deb http://neuro.debian.net/debian jessie main contrib non-free' > /etc/apt/sources.list.d/neurodebian.sources.list
RUN echo 'deb http://neuro.debian.net/debian data main contrib non-free' >> /etc/apt/sources.list.d/neurodebian.sources.list
RUN apt-key adv --recv-keys --keyserver pgp.mit.edu 0xA5D32F012649A5A9

# install fsl
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get -y install fsl-5.0-core \
    # Run configuration script for normal usage
    && echo ". /etc/fsl/5.0/fsl.sh" >> /home/jovyan/.bashrc

# Configure environment
ENV FSLDIR=/usr/share/fsl/5.0/
ENV FSLOUTPUTTYPE=NIFTI_GZ
ENV PATH=$PATH:/usr/lib/fsl/5.0
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/fsl/5.0

RUN wget --quiet https://sourceforge.net/projects/tarquin/files/TARQUIN_4.3.10/TARQUIN_Linux_4.3.10.tar.gz/download -O /tmp/tarquin.tar.gz && \
    mkdir /etc/tarquin && \
    tar -zxvf /tmp/tarquin.tar.gz -C /etc/tarquin --strip-components=1

ENV PATH /etc/tarquin:$PATH

RUN apt-get install -y libxml2-dev libxslt1-dev

# copy the examples directory in to the notebook root and change the owner
COPY ./examples /home/$NB_USER/work/examples/
RUN chown $NB_USER -R /home/$NB_USER/work/examples/

USER $NB_USER

#RUN pip install nibabel traits nose future simplejson lxml prov pbr mock xvfbwrapper

RUN pip install https://github.com/nipy/nipype/archive/master.zip

RUN pip install https://github.com/darcymason/pydicom/archive/master.zip

RUN git clone https://github.com/openmrslab/suspect.git /home/jovyan/suspect && \
    pip install suspect==0.3

RUN /bin/bash -c "source activate python2 && pip install pygamma"



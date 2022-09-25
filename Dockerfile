FROM ubuntu:20.04
MAINTAINER admin@lnorb.com

ARG ORB_VERSION
ARG OS_NAME

RUN apt-get update
RUN apt-get install curl sudo -y

########### orb-0.21.12-ubuntu-20.04-x86_64.tar.gz
ENV TARBALL=orb-${ORB_VERSION}-${OS_NAME}-x86_64.tar.gz

COPY tmp/${TARBALL} .
RUN tar xvf ${TARBALL}
RUN rm -f ${TARBALL}

WORKDIR /orb

ENV ORB_NO_DEVICE_ID_WARNING=1
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata

RUN useradd -ms /bin/bash orb

RUN bash bootstrap_ubuntu_20_04.sh

USER orb
WORKDIR /home/orb

CMD ["/usr/bin/python3", "/orb/main.py"]

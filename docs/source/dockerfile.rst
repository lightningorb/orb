Dockerfile
==========

.. code::

    FROM ubuntu:20.04

    RUN apt-get update
    RUN apt-get install curl -y

    RUN curl https://lnorb.s3.us-east-2.amazonaws.com/customer_builds/orb-0.21.5-ubuntu-20.04-x86_64.tar.gz > orb-0.21.5-ubuntu-20.04-x86_64.tar.gz 

    RUN tar xvf orb-0.21.4-ubuntu-20.04-x86_64.tar.gz

    WORKDIR orb

    RUN apt-get update;
    ENV ORB_NO_DEVICE_ID_WARNING=1
    ARG DEBIAN_FRONTEND=noninteractive
    RUN bash bootstrap_ubuntu_20_04.sh

Then some commands to get you started:

.. code::

    $ docker build -t orb .
    $ alias orb='docker run --rm -v `pwd`/orb_data:/root/.config -p 8080:8080 -it orb python3.9 main.py ${*}'
    $ orb --help
    $ orb test run-all-tests
    $ orb node create-orb-public cln rest
    $ orb node info
    $ orb node create-orb-public lnd rest
    $ orb web serve

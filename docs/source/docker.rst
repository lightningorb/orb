Docker
======

Orb CLI
~~~~~~~

Setting yourself up with Docker is very easy, although only allows :ref:`CLI` interactions, and spawing :ref:`web`.

.. image:: https://www.docker.com/wp-content/uploads/2022/03/vertical-logo-monochromatic.png
    :width: 100px
    :align: center

.. code::

    # pull the latest image
    docker pull lnorb/orb

    # add the following to your ~/.bashrc
    alias orb='docker run -v ${HOME}/.config:/home/orb/.config/ --rm -it lnorb/orb python3 /orb/main.py ${*}'
    
    # try out some commands
    orb node create-orb-public lnd rest
    orb channel list-forwards

Getting a list of tags
----------------------

.. code::

    curl -L -s 'https://registry.hub.docker.com/v2/repositories/lnorb/orb/tags?page_size=1024'|jq '."results"[]["name"]'

Orb VNC
~~~~~~~

Running Orb in VNC is an easy and convenient way of getting up and running. It is also a convenient way to keep Orb running for node automation.

.. image:: https://upload.wikimedia.org/wikipedia/en/5/51/Virtual_Network_Computing_%28logo%29.svg
    :width: 100px
    :align: center

.. code::

    docker run \
        -d \
        -h orb \
        --name orb-vnc \
        -p 6080:80 \
        -e USER=ubuntu \
        -e HTTP_PASSWORD=moneyprintergobrrr \
        -e HOSTNAME=signet.lnd.lnorb.com \
        -e NODE_TYPE=lnd \
        -e PROTOCOL=rest \
        -e NETWORK=signet \
        -e REST_PORT=8080 \
        -e GRPC_PORT=10009 \
        -e MAC_FILE_PATH=/certs/data/chain/bitcoin/signet/admin.macaroon \
        -e CERT_FILE_PATH=/certs/tls.cert \
        -v /dev/shm:/dev/shm \
        -v ${HOME}/dev/plebnet-playground-docker/volumes/lnd_datadir:/certs \
        lnorb/orb-vnc

Getting a list of tags
----------------------

.. code::

    curl -L -s 'https://registry.hub.docker.com/v2/repositories/lnorb/orb-vnc/tags?page_size=1024'|jq '."results"[]["name"]'

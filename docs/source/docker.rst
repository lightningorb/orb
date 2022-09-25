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

Docker
======

Setting yourself up with Docker is very easy, although only allows :ref:`CLI` interactions, and spawing :ref:`web`.

.. image:: https://www.docker.com/wp-content/uploads/2022/03/vertical-logo-monochromatic.png
    :width: 100px
    :align: center

.. code::

    docker pull lnorb/orb
    alias orb='docker run --rm -it lnorb/orb ${*}'
    orb node create-orb-public lnd rest
    orb channel list-forwards

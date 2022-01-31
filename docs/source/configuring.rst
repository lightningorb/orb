.. contents:: Table of Contents
    :depth: 2

Configuring
===========

Orb needs to connect to your node from the outside world (from outside the node, unlike Umbrel which runs on the node itself). To do so, lnd.conf needs to be modified to allow outside connections.

.. note::

    Please note this is not a security liability, as Orb encrypts your certificate and macaroon using an RSA key unique to your device (unique to the device connecting to your node).

LND
---

Step 1:
.......

SSH into your node.


Step 2:
.......

Edit your `lnd.conf` and enter your node's externally visible IP as an entry:

.. code:: bash

    tlsextraip=<your_node_ip>


(please note the `tlsextraip=` line may appear multiple times).

Step 3:
.......

Shut down lnd.


Step 4:
.......

Delete `.lnd/tls.cert`.


Step 5:
.......

Start lnd.


Umbrel
------

TODO.

Raspblitz
---------



Step 1:
.......

SSH into your node.


Step 2:
.......

Edit your `lnd.conf`, and enter your node's externally visible IP as an entry:

.. code:: bash

    tlsextraip=<your_node_ip>


(please note the `tlsextraip=` line may appear multiple times).

Step 3:
.......

Restart lnd.


Connection Settings
-------------------

In Orb, now click on `app > settings`, and add the following information:


IP Address
..........

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_08-03-31.png
   :alt: ip address
   :align: center

Protocol
........

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_08-15-39.png
   :alt: protocol
   :align: center

Port
........

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_08-24-25.png
   :alt: protocol
   :align: center

TLS Certificate
...............

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_08-25-55.png
   :alt: protocol
   :align: center

Macaroon
........

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_08-25-23.png
   :alt: protocol
   :align: center

Click `close` and restart Orb.
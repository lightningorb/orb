.. contents:: Table of Contents
    :depth: 2

Configuring
===========

Orb needs to connect to your node from the outside world (from outside the node, unlike Umbrel which runs on the node itself). To do so, lnd.conf needs to be modified to allow outside connections.

This is very typical, e.g the steps are similar to connecting `ZapHQ's Desktop Wallet <https://docs.zaphq.io/docs-desktop-lnd-configure>`_. Please cross-reference these steps with those listed in Zap's documentation, as Zap's may currently be more complete.

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

   tlsextraip=[YOUR_NODE_IP]

   or 
   
   tlsextradomain=[YOUR_NODE_DOMAIN]


(please note the `tlsextraip=` or `tlsextradomain` lines may appear multiple times).

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


Step 1:
.......

SSH into your node.


Step 2:
.......

Edit your `~/umbrel/lnd/lnd.conf` and enter your node's externally visible IP as an entry:

.. code:: bash

   tlsextraip=[YOUR_NODE_IP]

   or 
   
   tlsextradomain=[YOUR_NODE_DOMAIN]

(please note the `tlsextraip=` or `tlsextradomain` lines may appear multiple times).


Step 3:
.......

Shut down lnd.


Step 4:
.......

Delete `~/umbrel/lnd/tls.cert`.


Step 5:
.......

`Restart LND <https://community.getumbrel.com/t/how-to-restart-lnd-after-a-config-change/3097>`_:

.. code:: bash

   cd ~/umbrel;
   docker-compose restart lnd;

Raspblitz
---------



Step 1:
.......

SSH into your node.


Step 2:
.......

Edit your `lnd.conf`, and enter your node's externally visible IP as an entry:

.. code:: bash

   tlsextraip=[YOUR_NODE_IP]

   or 
   
   tlsextradomain=[YOUR_NODE_DOMAIN]

(please note the `tlsextraip=` or `tlsextradomain` lines may appear multiple times).

Step 3:
.......

Restart lnd.


Connection Settings
-------------------

In Orb, now click on `app > settings`, and add the following information:


IP Address
..........

Enter your node's IP or domain name:

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_08-03-31.png
   :alt: ip address
   :align: center

Protocol
........

Select the protocol. Desktop users can use both GRPC and REST, while mobile users can only connect via REST.

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_08-15-39.png
   :alt: protocol
   :align: center

Port
........

The ports can most likely be left untouched, unless you have selected a different port for security reasons.

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
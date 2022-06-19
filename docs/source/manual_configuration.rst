.. _manual-configuration:

Manual configuration
--------------------

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

Make sure it contains the following settings:

.. code:: bash

   tlsautorefresh=1
   rpclisten=0.0.0.0:10009
   restlisten=0.0.0.0:8080

Step 3:
.......

Shut down lnd.


Step 4:
.......

.. code:: bash

   mv .lnd/tls.cert .lnd/tls.cert.backup
   mv .lnd/tls.key .lnd/tls.key.backup


Step 5:
.......

Start lnd.

In Orb, now click on `app > connection settings`, and add the following information:


Node type and IP Address
........................

Enter your node's IP or domain name:

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-03-27_11-22-49.png
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

Orb requires you to copy your TLS certificate over from your node, and ingest it into Orb. Since we take security seriously, the certificate is encrypted using a unique RSA key.

Thus you'll first need to install the python3 rsa module on your node:

.. code:: bash

   pip3 install rsa

Next copy the command:

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-03-13_10-06-38.png
   :alt: protocol
   :align: center

You can refer to :ref:`connection-string` if you are curious to know what the connection command does).

Paste it in your node's terminal, and run it.

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/term_2022-03-13_11-03-45.png
   :alt: protocol
   :align: center

This should output multiple lines ending with two equal signs, `==`. Copy those lines, and paste them into Orb:

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-03-13_10-13-48.png
   :alt: protocol
   :align: center

If you carried out those steps successfully, the dialog should say 'Certificate correctly formatted'.

Macaroon
........

The steps for the Macaroon are identical to those for the certificate.

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_08-25-23.png
   :alt: protocol
   :align: center

Click `close` and restart Orb.
.. _umbrel-lndconnect:

Umbrel / lndconnect URL
=======================

Core Lightning
--------------

CLN users simply need to click on 'connect wallet'.

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Lightning_Node__Umbrel_2022-09-19_09-05-22.png
   :alt: protocol
   :align: center

Then copy the hex macaroon.

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Core_Lightning_-_Umbrel_2022-09-19_09-07-12.png
   :alt: protocol
   :align: center

Then the easiest approach would be to invoke the `orb node create` command.

.. asciinema:: /_static/orb-node-create.cln.umbrel.cast


LND
---

In your Umbrel interface:

- open your LND app
- at the top right, click on the 3 dots
- in the dropdown, click on 'Connect wallet'

.. image:: https://lnorb.s3.us-east-2.amazonaws.com/docs/Lightning+Node+%E2%80%94+Umbrel+2022-06-19+13-17-51.png
   :alt: protocol
   :align: center

Next, copy the lndconnect URL:

.. image:: https://lnorb.s3.us-east-2.amazonaws.com/docs/Lightning+Node+%E2%80%94+Umbrel+2022-06-19+13-19-21.png
   :alt: protocol
   :align: center

In Orb, click on:

- Orb > Umbrel node / lndconnect

.. image:: https://lnorb.s3.us-east-2.amazonaws.com/docs/Orb+2022-06-19+13-21-10.png
   :alt: protocol
   :align: center

- Paste the URL
- Click Save

.. image:: https://lnorb.s3.us-east-2.amazonaws.com/docs/Orb+2022-06-19+13-21-51.png
   :alt: protocol
   :align: center

- Restart Orb

Your node should be connected.


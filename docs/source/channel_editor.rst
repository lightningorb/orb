Channel Editor
==============

The Channel Editor opens when you click on a peer. It displays useful information, and allows you to set your fees as well as many other attributes.

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_11-27-29.png
   :align: center

Stats
-----

Fees earned
...........

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_11-22-50.png
   :align: center

The fees earned field displays how many sats were made routing out of the selected channel.


Fees
----

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_11-23-47.png
   :align: center


``Fee Rate Milli Msat``, ``Fee Base Msat``, ``Min HTLC msat``, ``Max HTLC msat`` and ``Time Lock Delta`` can be altered via the Channel Editor, by modifying the value and pressing enter.

Pay Through Channel
-------------------


.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_11-30-56.png
   :align: center


This specifies whether the channel is used for payments, or not. For example, you ought to switch it off for drains, since it would be difficult to re-gain outbound.

Aim for Ratio (local / capacity)
--------------------------------

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_11-31-59.png
   :align: center
   :scale: 80%

This is the ratio at which the channel is considered **balanced**. For example, with a ``1 BTC`` channel, a ratio of ``0.1`` signifies the channel is considered **balanced** once the local balance reaches ``0.1 BTC`` and remote balance reaches ``0.9 BTC``.

This setting is used during automatic channel selection for payments and rebalancing.

Other
-----

The rest of the settings, that have not been detailed on this page are read-only. 
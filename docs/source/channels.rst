Channels
========

Channels are one of the most important building blocks in lightning, and thus in Orb, too.

.. image:: single_channel.png
   :align: center
   :scale: 50%

Above is a channel between `peer_0` and our `mock_node`.

.. note::

    The first thing to note is that Orb currently makes no distinction between **peers** and **channels**. So if your node has multiple channels to the same peer, then the peer appears multiple times.

    The distinction might be made in future versions, where multiple channels to the same peer will be clearly visible.


Channel Liquidity
-----------------

The green dots represent **1 Million Satoshis**.


Fee Widget
----------

.. image:: fee_widget.png
   :align: center

The widget with two handles represents the **outgoing fees**.

Fees can be adjusted by click & dragging the handles inwards or outwards.

The size of the fee widget is proportional, meaning the largest fee widgets represent the largest fees that are currently set, while the smallest fee widgets represent the smallest fees; that is, regardless of how big or small those actually are.

Directionality
--------------

By default, the ``local balance`` or ``outbound liquidity`` appears in green, on the side of the peer.

.. image:: single_channel.png
   :align: center
   :scale: 50%

When Sats move into the channel, you can think of a syringe pulling in liquidity: the fee widget moves closer to your node.

When Sats move out of that channel, you can think of a synringe injecting liquidity into that peer: the fee widget moves closer to the peer.

Inverted Channels
~~~~~~~~~~~~~~~~~

If this mental model doesn't work for you, you can reverse it by toggling: ``app > settings > display > inverted channels``.

Sent / Received
---------------

.. image:: sent_received.png
   :align: center
   :scale: 50%

The lines extending out of the peers represent the total liquidty sent & received through those peers. 

Their visibity can be toggled via: `app > settings > display > show sent / received`.
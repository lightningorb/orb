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

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-01-31_08-42-50.png
   :alt: sent received
   :align: center

Their visibity can be toggled via: `app > settings > display > show sent / received`.

One green line indicates the channel made 10k sats in fees by routing out. One blue line indicates the channel routed in, and those routing events contributed to other channels making 100k sats in fees.


Sort Criteria
-------------

Ratio
~~~~~

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-07-26_11-58-16.png
   :align: center
   :width: 500px

The default sort criteria for Channels is by ratio (`local / capacity`). This has several strong advantages for gaining an intuitive sense of your liquidity:

- Aesthetically pleasing: this mode is easier on the eyes than the other modes.
- Clearly communicates imbalances: 

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-07-26_12-03-43.png
   :align: center
   :width: 500px

The disadvantages are that the channels keep on moving when their liquidities change, making it impossible to track which channel is which.

Capacity
~~~~~~~~

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-07-26_12-11-42.png
   :align: center
   :width: 500px

Sorting channels by capacity has the avantage of enabling you, the operator, to focus on capacity clusters: for example you could spend time manually rebalancing channels between 3M and 5M.


Total Sent / Total Recieved
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Toggling between Total Sent and Total Reieved is a good way to get a sense of which are the channels that route the most.

out-ppm / Alias
~~~~~~~~~~~~~~~

Alias is very useful in case you would like your channels to stay in the same place in the Orb, so you can refer to them easily without having to look for them in the UI.

However unless you have a very balanced node at all times, this may become visualy disturbing.



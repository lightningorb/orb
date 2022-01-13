Fee Distribution
================

The `Fee Distribution` dialog (``Lightning > Forwarding History > Fee Distribution``):

- discretizes routing events to ``10k sats``
- calculates frequencies and probabilities
- calculates normalized frequencies and probabilities (gaussian distribution)
- graphs the probabilities

.. image:: fee_distribution.png
   :align: center

Discretization
--------------

Discretization means the node's historical routing events are all converted to ``10k sat`` routing events. So a `100k` routing event would get converted into ``10x 10k`` routing events. This is to get a stronger signal from our routing data.

Utility
-------

The highest probability fee should be the `preferred` fee that is used on the channel. The higher the PPM the better (a PPM of 0 would tend to get the highest routing frequency, but that's not useful in terms of making sats).

In this particular example, we can see that ``ln.nicehash.com`` has historically routed the most at ``150 PPM``. This is the fee that should be set when the channel's ratio tends to the node's global ratio.

Interpretations
---------------

A smooth curve with many points suggests the channel has a good fee setting algorithm, and that routing event fee distributions are highly predictable based on fees.

Ideally you'll want the curve to be a traditional bell-shape, with the head of the bell curve aligned with the node's global ratio.

An erratic curve suggests an unpredictable relationship between fees and routing.

A very simple curve (e.g a line) suggests the channel only has a few different fees set.
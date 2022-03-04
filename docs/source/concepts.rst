Concepts
========

Fortunately there aren't many new concepts in Orb, and rightly so: there is no re-inventing of the wheel necessary here.

However it is worth getting a firm grasp of the terms `channel ratio`, `override ratio`, `global ratio` and `balanced ratio` as they are used a lot.

.. note::
   
   This section is somewhat technical. It is placed upstream of the practical guides as understanding these concepts first is a technical pre-requisite, however it is not a strict one, so feel free to skip ahead and return to these concepts later to gain a better understanding.

.. contents:: Table of Contents
    :depth: 3

Channel Ratio
-------------

When discussing a channel's liquidity, we think of it as comprising:

- a capacity
- a local balance
- a remote balance

A channel's **capacity** equals its **local balance** + **remote balance**. Please note it's a little more complex as technically we would need to account for commit fees if we are the channel initiator, also the balances do not include pending HTLCs, but we can ignore these details for now, as we are focussing on the concept.

A channel's **ratio** equals its **local balance** divided by its **capacity**. Thus a channel with no outbound has a ratio of `0` whilst a channel that is `100%` outbound has a ratio of `1`. Thus a perfectly balanced channel has a ratio of `0.5`.

Dealing with channel ratios has several advantages:

- Values are between 0 and 1
- When discussing channel balancedness, the discreet local remote and outbound values are irrelevant.

Override Ratio
--------------

The override ratio is where the node runner wants the ratio to be. It is a way for the node runner to dictate the desired ratio for a channel.

Global Ratio
------------

Global ratio is the exact same concept as channel ratio, but for the whole node. So the global ratio is the **total local balance** divided by the **total capacity** of the node.

A global ratio of `0.5` signals the node has the same amount of outbound as inbound. A small value signals the node's liquidity is skewed towards the inbound, while a large global ratio signals the node's liquidity is skewed towards the outbound.

Balanced Ratio
--------------

The term **balanced ratio** signals where the ratio should ideally be, were the channel perfectly balanced. The **balanced ratio** is the channel's **optimal** ratio.

Let's work through some simple examples, as it will help elucidate these concepts.

Example 1
~~~~~~~~~

Let's begin with a simple node setup, with 4 balanced channels of 10M each. This gives us a capacity of 40M, and outbound of 20M, inbound of 20M, and a global ratio of .5.


.. image:: https://lnorb.s3.us-east-2.amazonaws.com/docs/2022-03-04+12.43.50.jpg
   :align: center
   :scale: 80%


Now let's say channel A is a strong drain. It then makes sense to specify an override ratio of .8 (for example). This helps keep more liquidity outbound, which is where it is of use. However those extra 3M need to be borrowed from B, C and D, leaving us with balanced ratios of .4.

In other words, if we want a ratio of .8 on A, we need ratios of .4 on all the other channels.


Example 2
~~~~~~~~~

This example is identical to the previous one, although channel A now has a capacity of 20M. 


.. image:: https://lnorb.s3.us-east-2.amazonaws.com/docs/2022-03-04+12.44.00.jpg
   :align: center
   :scale: 80%


Therefore this time, we need to borrow double the amount from other channels.


Example 3
~~~~~~~~~

This example is slightly more realistic; it features a broad range of capacities: 20M, 100M, 10M, 10M. The starting ratios are: .4, .1, .5, .6. The goal is to:

- Override A's ratio to 0.8 (since it is a drain)
- Keep B's ratio to 0.1 (for example, someone could have opened a very large channel to your node)
- Keep the ratios of the other channels (C, D) 'balanced'.

.. image:: https://lnorb.s3.us-east-2.amazonaws.com/docs/2022-03-04+12.44.07.jpg
   :align: center
   :scale: 80%

It turns out the balanced ratios for C and D are 0.35.

Bonus: in example 3, we are explicitely setting B's ratio to 0.1. If we do not set it explicitely, then balanced ratios for B, C and D are: 0.142.

If example 3 felt hard, that's because it is. By now you should be getting a sense that calculating liquidities for channels is kind of a hard problem for an operator to do by hand, and gets increasingly difficult the more channels there are, with many channels sizes, liquidities etc. while for the computer this is an easy task.

How is this useful
------------------

Balanced ratio is extremely useful in the day to day of running a node, since it enables node operators to dictate where they want the ratios of certain channels to be, while letting the ratios of other channels be computed for them.

The balanced ratios of channels are also used by Orb when automatically selecting channels for payments. For example, if the operator lets Orb pick outgoing channels for payments, then Orb will prefer selecting channels with balances that are greater than their balanced ratio.

Likewise, for circular rabalances, if Orb gets to automatically pick the from and to channels, it prefers to select channels where the ratios are above, and below their respective balanced ratios.

Balanced ratios are also used in automated fee setting, to try and nudge channel liquidities back towards their balanced ratios.
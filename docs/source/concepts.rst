Concepts
========

Fortunately there aren't many new concepts in Orb, and rightly so: there is no re-inventing of the wheel necessary here.

However it is worth getting a firm grasp of the terms `channel ratio`, `global ratio` and `balanced ratio` as they are used a lot.

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

Global Ratio
------------

Global ratio is the exact same concept as channel ratio, but for the whole node. So the global ratio is the **total local balance** divided by the **total capacity** of the node.

A global ratio of `0.5` signals the node has the same amount of outbound as inbound. A small value signals the node's liquidity is skewed towards the inbound, while a large global ratio signals the node's liquidity is skewed towards the outbound.

Balanced Ratio
--------------

The term **balanced ratio** applies to channels: it represents where the ratio should ideally be, were the channel perfectly balanced.

Orb uses channel balanced ratios when automatically picking channels for payments, for example, or rebalances. It also uses the balanced ratio in automated fee-setting, to try and nudge the channel's liquidity towards its balanced ratio.

With a global ratio of `0.5`, the balanced ratio of each channel would also be `0.5`. However let's think of a real world scenario where manipulating balanced ratios becomes very useful.

Let's say you have the following channels:

.. code::

   Channel / Peer: A,    B,    C,    D,    E
   Capacity:       100,  100,  200   300,  200
   Local Balance:  50,   50,   100,  150,  50

Notice all channels are balanced, with the exception of E. Now let's say we want to force the ratios of B and D to remain `0.1`.

For example, B and D could be disproportionally huge LNBIG channels that were opened to our node. To avoid all our liquidity getting sucked up in huge channels, we can set their ratio to a very low value.

TBD
Channel Highlighter
===================

.. contents:: Table of Contents
    :depth: 3


This feature enables you to write simple expressions to highlight channels. This is extremely useful to unearth vital information about your channels, and their performance.

**Lightning > Channels > Highlighter**

It is important to familiarize yourself with the Channel Highlighter as a stepping stone towards using :ref:`automated-fees` and :ref:`automated-rebalancing`.

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-02-18_08-11-50.png
    :align: center

Syntax
------

The syntax is a Python expression; it is simply evaluated against all channels by being put through an `eval`; if the expression evaluates as `True` then the channel is highlighted, if `False` then it isn't.

The expression is re-run every 30 seconds, so as channel attributes change, so do the highlights.

The expression has access to the `channel` (or `c` object for short). That is, the :py:mod:`orb.misc.channel.Channel` object. You can refer to :py:mod:`orb.misc.channel.Channel` to see all the attributes available. However we'll try and cover the most common ones here.


By alias
--------

Let's say you want to highlight all your LNBIG channels:

.. code:: python

    'LNBIG' in c.alias

By pubkey
---------

Highlighting channels by pubkey will be very useful later on, to ignore specific channels during rebalances for example:

.. code:: python

    c.remote_pubkey == '021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d'


By Channel ID
-------------

.. code:: python

    c.chan_id == 785824259055878146


Inactive channels
-----------------

.. code:: python

    not c.active

Or 

.. code:: python

    c.active == False


Unbalanced channels
-------------------

Highlighting low outbound channels can be done using either *ratios* or absolute *sat values*.

.. code:: python

    c.ratio < 0.1

The channel ratio is the channel's: `local balance / capacity`. By default, local balance doesn't including pending remote HTLCs, so this would result in your channel highlights blinking as HTLCs make the ratio cross the `0.1` threshold. To mitigate for this behavior, you can use:

.. code:: python

    c.ratio_include_pending < 0.1


Unbalanced channels using balanced ratios
-----------------------------------------

Orb interally computes the ideal ratios for your channels; these are referred to as the **balanced ratios**. If all your channels are at their balanced ratios, then your node is perfectly balanced.

The following highlights all your channels who's ratios are below their balanced ratios:

.. code:: python

    c.ratio < c.balanced_ratio

Likewise with channels with ratios above their balanced ratios:

.. code:: python

    c.ratio > c.balanced_ratio


Unbalanced channels using absolute sat values
---------------------------------------------

The following expression highlights channels with less than `100k` sats.

.. code:: python

    c.local_balance < 100_000

Once again, if you'd like to include pending HTLCs to avoid blinking highlights:

.. code:: python

    c.local_balance_include_pending < 100_000


Channels that are earning
-------------------------

Orb internally tracks transactions and payments, and exposes that information for easy access. Thus highlighting channels that made more than 1000 sats in routing fees is easy:

.. code:: python

    c.earned > 1000

If you often connect to drains, then your channels may be better at routing in than out, in which case you can use:

.. code:: python

    c.helped_earn > 100_000


Channels that are earning both ways
-----------------------------------

By combining expressions, we can find channels that earn both in and outbound:

.. code:: python

    c.earned > 1000 and c.helped_earn > 100_000


Channels that are not earning
-----------------------------

Orb can easily help you identify channels that are not earning, and therefore ought to be closed:

.. code:: python

    c.earned < 1000 and c.helped_earn < 10_000

By capacity
-----------

You can highlight very large, or small channels:

.. code:: python

    c.capacity >= 100_000_000

Or channels between certain capacities:

.. code:: python

    c.capacity >= 1_000_000 and c.capacity <= 1_000_000



Pending HTLCs
-------------

.. code:: python

    c.pending_htlcs != []


Pending in
----------

.. code:: python

    [x for x in c.pending_htlcs if x.incoming] != []


Pending out
-----------

.. code:: python

    [x for x in c.pending_htlcs if not x.incoming] != []


With satoshis sent / received
-----------------------------

.. code:: python

    c.total_satoshis_sent > 1_000_000


.. code:: python

    c.total_satoshis_received > 1_000_000


Unsettled balance
-----------------

.. code:: python

    c.unsettled_balance > 1_000_000


Commit fee
----------

.. code:: python

    c.commit_fee > 1000


Initiator
---------

.. code:: python

    c.initiator


.. code:: python

    not c.initiator

Balanced ratio
--------------

.. code:: python

    c.balanced_ratio <= 0.1

Fee Rate
--------

.. code:: python

    c.fee_rate_milli_msat <= 100_000

Time Lock Delta
---------------

.. code:: python

    c.time_lock_delta >= 40

Min HTLC
--------

.. code:: python

    c.min_htlc_msat > 1_000

Max HTLC
--------

.. code:: python

    c.max_htlc_msat > 1_000_000_000

Fee Base
--------

.. code:: python

    c.fee_base_msat > 100_000



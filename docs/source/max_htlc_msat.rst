Auto Max HTLC MSat
==================

.. note::

   The most important feature of this app is to disable your channels when they no longer have any outbound.

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-07-26_11-31-48.png
   :align: center
   :width: 500px


Set to 0 when depleted
----------------------

This is an important option for the health of your node and the health of the network. It specifies that once the outbound ratio (i.e the `outbound liquidity / capacity`) goes below this threshold, the max_htlc_msat should be set to 0.

When `outbound liquidity / capacity` is greater than this ratio, then the policy is used.

Policy
------

The policy dicates where the max_htlc_msat value should automatically be set.

Balanced Ratio
~~~~~~~~~~~~~~

max_htlc_msat is set to the channel's `outbound * balanced ratio`.

Half Capacity
~~~~~~~~~~~~~~

max_htlc_msat is set to the channel's `outbound * 0.5`.

Local Balance
~~~~~~~~~~~~~~

NOT RECOMMENDED. This sets your max_htlc_msat to your local balance; technically it's the best setting for properly advertising liquidity, however it is the worst possible setting for privacy, and should not be used.
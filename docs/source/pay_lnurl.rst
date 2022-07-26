Paying with LNURL
=================

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-07-26_09-37-01.png
   :align: center
   :height: 500px


LNURL
-----

This is the LNURL you wish to pay, please note the format is:

LNURL***************[...]

Not:

user@domain.com

This is the same format as LNURL QR codes.

.. note::

   The `user@domain.com` format can be implemented in a future version. If this is required, the please make the request.

Rate Limitting
--------------

Getting an LN Invoice from an LNURL involves querying a third party endpoint; it is very common for these endpoints to be rate-limitted. 5 seconds seems to be the most common rate-limit.

Satoshis
--------

The total value to be sent, denominated in Sats.

Chunks
------

The number of chunks in which the number of satoshis should be broken up.

For example:

`1_000_000 Satoshis` and
`10 Chunks`
=
`10 x 100_000 Sat` payments.

Fee Rate PPM
------------

This is the maximum fee rate that will be used for the payment.

Threads
-------

This is the total number of simultaneous threads on which to carry out the payments.

For example:

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Monosnap_2022-07-26_10-16-50.png
   :align: center

Max Paths
---------

The number of routes to try before giving up.

First Hop Channel
------------------

Paying invoices has two modes:

- Specifying a 'First Hop Channel' (manual)
- 'First Hop Channel' being set to 'any' (auto)

These two payment mechanism work very differently, so please read through this page carefully before attempting to make payments.

Specifying 'First Hop Channel'
------------------------------

This specifies you only intend on paying one invoice, through the specified channel. In this mode, no more than 1 thread is recommended.

'First Hop Channel' any
-----------------------

With First Hop Channel 'any' Orb uses its Channel Selector to automatically pick channels through which to make payments. Please note the current method is:

- Pick channels where the `outbound - payment size + max_fee_rate < outbound * balanced_ratio`.
- Pick channels that don't currently have outgoing payments.

Time Preference
---------------

With a low time preference (-1) LND performs a very exhaustive path search, starting with very cheap paths.

With a normal time preference (0, the default prior to LND v0.15.0) LND performs the path search as it did in versions prior to v0.15.0.

With a high time preference (1) LND performs a non-exhaustive path search, thereby prefering more expensive routes with a higher chance of success.

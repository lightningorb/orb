Automated Fees
==============

Orb includes a simple yet powerful rule-based fee setting engine.

*Apps > auto > fees*

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-02-10_11-38-01.png
   :align: center
   :scale: 80%

Upon first launch, the auto-fees dialog is fairly empty. Let's take a look at some settings.


Engine Settings
---------------

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-02-10_11-46-47.png
   :align: center
   :scale: 80%

Run frequency
~~~~~~~~~~~~~

This is how often you'd like the engine to look at your channel fees, and decide whether they ought to be updated. Please note the value is in seconds, and allows valid Python syntax (within an eval).


Time before next update
~~~~~~~~~~~~~~~~~~~~~~~

This is the delay between each update. Let's say `run frequency` is set to `60` seconds, but `time before next update` is set to `600` seconds, then if a channel needs its fees updated, but hasn't been updated within the last 10 minutes, its fees get updated immediately.

This is useful, as you'd want fee adjustments to be *reactive* to liquidity changes. However if the fees required updating again 60 seconds later, that update won't happen until the 10 minutes have elapsed. This is to keep fee changes reactive, yet prevent spamming the network.


Fee drop factor
~~~~~~~~~~~~~~~

Let's say your current fees on channels are at `1000 PPM` and you were to drop them to `100 PPM`, then a drop factor of `0.1` would represent a `10%` drop, so the channel's outgoing fees would get adjusted to `900 PPM`.

A small `fee drop factor` is a good idea, because it skews your fee distribution upwards (we'll discuss fee distributions later), and protects your liquidity.

Fee bump factor
~~~~~~~~~~~~~~~

Same as `fee drop factor` but when the desired fee is higher than the current fee rate. It's a good idea to keep a high number, since raising fees is usually done to protect liquidity.


Adding rules
------------

Let's add a simple rule:

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-02-10_12-10-13.png
   :align: center
   :scale: 80%

Match Rule Settings
~~~~~~~~~~~~~~~~~~~

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-02-10_12-11-54.png
   :align: center
   :scale: 80%

Rule Name
.........

This can be anything you want, simply to remind you what the rule does. Try to be descriptive as you'll need to remind yourself later.

Fee Rate PPM
............

This is the desired fee rate. We'll discuss `best_fee` later.

Match Rule
..........

This is a Python expression used to match with channels. It is run on all channels, and if one or many channels match, then this rule is applied to them. The default value is `False` meaning the current rule will never be applied. Setting this to `True` would apply this rule to every channel.

Here are some example match rules.

This matches LOOP's pubkey, so the rule is applied to LOOP only:

.. code:: python

  channel.remote_pubkey == '021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d'


-------------------------------------------------------------------------

This matches okcoin's alias, so the rule is applied to okcoin:

.. code:: python

  channel.alias == 'okcoin'

-------------------------------------------------------------------------

This matches to all LNBig channels:

.. code:: python

  'LNBIG' in channel.alias

-------------------------------------------------------------------------

This matches low outbound channels.

.. code:: python

  channel.ratio < 0.1

By default, LND reports a channel's local balance minus it's pending outgoing HTLCs. If you want to ignore pending HTLCs, use:


.. code:: python

  channel.ratio_including_pending < 0.1


This has the disadvantage of being less precise, and possibly resulting in more temporary channel failures. However it has the advantage of being less noisy to the network.

-------------------------------------------------------------------------

This matches channels with a local balance smaller than or equal to `100_000` SATS. 

.. code:: python

  channel.local_balance <= 100_000

Matching on many criteria
.........................

It is possible to match on multiple criteria. For example, to match channels with less than 100k sats, or with a ratio below 0.1:

.. code:: python

  channel.local_balance < 100_000 or channel.ratio < 0.1


To find out what channel properties are available, please refer to the :class:`orb.misc.channel.Channel` class documenation.


"Best" fee
----------

The "best" fee feature is currently undocumented. Use at own risk.


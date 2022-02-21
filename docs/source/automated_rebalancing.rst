.. _automated-rebalancing:

Automated Rebalancing
=====================

Before delving into rebalancing, make sure you familiarize yourself with the :ref:`channel-highlighter`, as you'll need to be familiar with the syntax, and the rebalancing expressions can be pasted directly into the highlighter to preview what channels will get selected.

*Apps > auto > balance*

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-02-10_15-29-17.png
   :align: center
   :scale: 80%


Engine Settings
---------------

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-02-10_15-32-02.png
   :align: center
   :scale: 80%

Number of rebalances
~~~~~~~~~~~~~~~~~~~~

How many rebalance threads should run at once.


'Ignore' rules settings
-----------------------


.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-02-10_16-13-25.png
   :align: center
   :scale: 80%


Ignore rules are useful when you are sure you never want to rebalance either to or from a channel.

Rule Name
~~~~~~~~~

This is simply an alias for the rule. Be descriptive as it will come in handy when returning to this dialog later.

Rule
~~~~

This field expects a valid Python expression. The expression is run against each channel, and if it evaluates as True, then the channel is ignored.

In this case, we are ignoring the LOOP channel.

.. code:: python

  channel.remote_pubkey == '021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d'


This could be achieved with:

.. code:: python

  channel.alias == 'LOOP'

This example would ignore channels that have earned less than 10k SATS:

.. code:: python

  channel.earned < 10_000

N.B: Using 'earned' requires querying a database containing the entire routing history. Currently this may result in the Engine becoming too slow to use. Use with care.


'From To' rules settings
------------------------


.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-02-10_16-45-32.png
   :align: center
   :scale: 80%


Rule Name
~~~~~~~~~

This is simply an alias for the rule. Be descriptive as it will come in handy when returning to this dialog later.

Fee Rate (PPM)
~~~~~~~~~~~~~~

The fee rate at which to perform the rebalance.

Amount (SAT)
~~~~~~~~~~~~

The amount of Sats to rebalance.


From / To Rule:
~~~~~~~~~~~~~~~

A python expression that is run again each channel to find candidates from / to channels for rebalancing.

In this example, the expressions are:

.. code:: python

  channel.ratio > 0.5

and

.. code:: python

  channel.ratio < 0.1

The above rules would simply rebalance from any channel with more than 50% outbound towards channels with less than 10% outbound.


Start the Engine
----------------

To start the rebalancing engine:


.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-02-10_15-42-16.png
   :align: center
   :scale: 80%


Stop the Engine
---------------

To stop the rebalancing engine:

.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-02-10_15-53-51.png
   :align: center
   :scale: 80%

Fees
====

Orb includes a simple yet powerful rule-based fee setting engine.

fees.yaml
---------

To enable the fee-setting engine, create a file called ``fees.yaml`` in the source directory.

Rules
-----

Single peer fixed PPM
.....................

Let's create a simple rule that sets ``LNBig.com [lnd-12]`` to ``100ppm``.

.. code:: yaml

    rules:
    - !Match
      alias: LNBig.com [lnd-12]
      fee_rate: 100
      rule: channel.remote_pubkey == '034ea80f8b148c750463546bd999bf7321a0e6dfc60aaf84bd0400a2e8d376c0d5'

Simple enough.

Low Outbound Peers
..................

Let's add a rule that borks channels with low outbound.

.. code:: yaml

    - !Match
      alias: Low Outbound
      fee_rate: 100_000
      priority: 100
      rule: channel.local_balance < 1_000_000 or (channel.local_balance / channel.capacity
        < 0.1)

Nice. Whenever the ``local balance`` falls below ``1M`` or the channels ``ratio`` goes below ``10%``, we set the fees to ``100k PPM``.

This is a high priority rule, because it prevents those annoying ``temporary channel failures``, so it should override all other rules, thus we set it to priority ``100``.


Low Inbound Peers
.................

Now let's say we desperately don't want to fall below ``10% inbound``, we can simply specify:

.. code:: yaml

    - !Match
      alias: Low Inbound
      fee_rate: 0
      rule: channel.local_balance / channel.capacity > 0.9

So whenever the ``ratio`` goes above ``90%`` we set our PPM to ``0``.


Lowbound Fee Discovery
......................

Experimental.

.. code:: yaml

  - !Match
    alias: Downward fee discovery
    all:
    - channel.local_balance >= 1_000_000
    - channel.local_balance / channel.capacity >= 0.1
    - channel.local_balance / channel.capacity <= 0.9
    - self.meta.last_routed == None or (self.meta.last_routed and arrow.utcnow().dehumanize(self.meta.last_routed)
      > arrow.utcnow().dehumanize('a day ago'))
    any: []
    fee_rate: min(self.policy_to.fee_rate_milli_msat * 0.9, 1000)
    priority: 10
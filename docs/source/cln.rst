Core Lightning
==============

Orb now supports Core Lightning.

c-lightning-REST
----------------

If you have a custom (e.g non-umbrel) CLN setup, you'll need to install `c-ligthning-REST <https://github.com/Ride-The-Lightning/c-lightning-REST>`_ on your node to connect to it.

.. note:: 

    This will have to be version >= v0.9.1 as we have a `closed pull-request <https://github.com/Ride-The-Lightning/c-lightning-REST/pull/142>`_ and at the time of writing, the latest version is v0.9.0.

c-lightning-events
------------------

Additionally you'll require `c-lightning-events <https://github.com/rbndg/c-lightning-events>`_ if you'd like to see live HTLC events (recommended).

Once installed, add the following info to your `orb_<pubkey>.ini` file:

.. code::

    [c-lightning-events]

    hostname=<your ip or hostname>
    protocol=<ws or wss>
    port=<events plugin port number>


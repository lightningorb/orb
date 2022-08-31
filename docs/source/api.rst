Orb API
=======

Node Factory
------------

The first step to connecting to a node via the Python API is registering its connection details via :ref:`CLI`.

Once you have registered some nodes (e.g one of Orb's public nodes) you can create instances of :class:`orb.ln.ln.Ln` using the **factory** function:

.. code:: python

    from orb.ln import factory

    ln = factory("02234cf94dd9a4b76cb4767bf3da03b046c299307063b17c9c2e1886829df6a23a")


Executing Orb API scripts
-------------------------

Since Orb's API or source code are not yet publically available, you can simply use the orb binary as you would the Python interpreter:

.. code:: bash

    $ orb my_script.py

Implementation heterogeneity
----------------------------

LN features a homogenous protocol with heterogenous implementations and programming languages; in other words, the protocol is the same, but different entities create their own implementations using different programming languages.

Famously, LND from `Lightning Labs <https://lightning.engineering>`_ is written in GoLang, and Core-Lightning from `Blockstream <https://blockstream.com>`_ is written in C. The miracle is that different entities have the freedom to do things their own way while speaking the same protocol. The disadvantage is that users need to choose their implementation.

Orb's API and CLI make picking your lightning implementation less important since Orb's :class:`orb.ln.ln.Ln` class provides a homogenous interface that hides whether you are interacting with an LND or CLN node.

Accessing node information
--------------------------

Let's begin by loading in a node, and printing basic info:

.. code:: python

    from orb.ln import factory

    cln = factory("02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764")

    print(cln.get_info())

Output:

.. code:: json

    {
        "alias": "regtest.cln.lnorb.com",
        "block_height": 174,
        "color": "02613d",
        "identity_pubkey": "02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764",
        "network": "regtest",
        "num_active_channels": 6,
        "num_inactive_channels": 0,
        "num_peers": 3,
        "num_pending_channels": 0,
        "version": "v0.11.2"
    }

And now with an LND node:

.. code:: python

    from orb.ln import factory

    lnd = factory("0227750e13a6134c1f1e510542a88e3f922107df8ef948fc3ff2a296fca4a12e47")

    print(lnd.get_info())

Output:

.. code:: json

    {
        "alias": "signet.lnd.lnorb.com",
        "block_height": 63387,
        "color": "3399ff",
        "identity_pubkey": "0227750e13a6134c1f1e510542a88e3f922107df8ef948fc3ff2a296fca4a12e47",
        "network": "mainnet",
        "num_active_channels": 4,
        "num_inactive_channels": 0,
        "num_peers": 4,
        "num_pending_channels": 0,
        "version": "0.15.0-beta.rc2 commit=v0.15.0-beta.rc2"
    }

The API calls and data returned are "massaged" in the :class:`orb.ln.ln.Ln` class and :mod:`orb.ln.types` module. In some cases the functionality or data are the intersection of the capabilities of implementations, in some cases the Union, in some cases, neither.

Accessing concrete implementations
----------------------------------

For this reason, you can decide to work directly with the implementation of your node with the `concrete` attibute.

.. code:: python

    from orb.ln import factory

    cln = factory("02234cf94dd9a4b76cb4767bf3da03b046c299307063b17c9c2e1886829df6a23a")

    print(cln.concrete.get_info())

.. code:: json

    {
        "address": [
            {
                "address": "c3uyrt5x4r4rbecgwi5q7dvyamrrvkf7xtirp6jfvpy3ymyuwquo4yyd.onion",
                "port": 9735,
                "type": "torv3"
            }
        ],
        "alias": "Orb (CLN)",
        "api_version": "0.8.0",
        "binding": [
            {
                "address": "127.0.0.1",
                "port": 9735,
                "type": "ipv4"
            }
        ],
        "blockheight": 751991,
        "color": "03fbff",
        "fees_collected_msat": "26607041msat",
        "id": "03fbffb45604f2e0d481c323612e6681fd77eacf9bbe853e83300991de75cc7f78",
        "lightning-dir": "/home/......./.lightning/bitcoin",
        "msatoshi_fees_collected": 26607041,
        "network": "bitcoin",
        "num_active_channels": 72,
        "num_inactive_channels": 0,
        "num_peers": 73,
        "num_pending_channels": 0,
        "our_features": {
            "channel": "",
            "init": "080a69a2",
            "invoice": 2000000024100,
            "node": "800000080a69a2"
        },
        "version": "v0.11.2"
    }

This returns the data the way you expect it for the given impementation.


Sending coins from LND to CLN in one line of code
-------------------------------------------------

In this tutorial we'll learn how to send coins from LND to CLN in 1 line of code. One of the great things about having a single API that can work with multiple nodes, is that mult-node operations can be performed in just a few lines.

We'll start by generating address:

.. code:: python

    from orb.ln import factory

    lnd = factory("02234cf94dd9a4b76cb4767bf3da03b046c299307063b17c9c2e1886829df6a23a")
    cln = factory("03fbffb45604f2e0d481c323612e6681fd77eacf9bbe853e83300991de75cc7f78")

    cln_address = cln.new_address()
    print(cln_address)

Super easy: 5 lines of code thus far. Now let's send.

.. code:: python

    from orb.ln import factory

    lnd = factory("02234cf94dd9a4b76cb4767bf3da03b046c299307063b17c9c2e1886829df6a23a")
    cln = factory("03fbffb45604f2e0d481c323612e6681fd77eacf9bbe853e83300991de75cc7f78")

    cln_address = cln.new_address()

    res = lnd.send_coins(
        addr=cln_address.address,
        satoshi=100_000,
        sat_per_vbyte=1,
    )

    print(res)


And that's it. We are done. Let's condense our code a little bit.


.. code:: python

    from orb.ln import factory

    lnd = factory("02234cf94dd9a4b76cb4767bf3da03b046c299307063b17c9c2e1886829df6a23a")
    cln = factory("03fbffb45604f2e0d481c323612e6681fd77eacf9bbe853e83300991de75cc7f78")

    print(lnd.send_coins(
        addr=cln.new_address().address,
        satoshi=100_000,
        sat_per_vbyte=1,
    ))

We're down to 3 lines of code (if we don't count the import). Let's bring this down to a one liner:


.. code:: python

    from orb.ln import factory as fa

    print(fa("pk1").send_coins(fa("pk2").new_address().address,100_000,1))

The point here is not code-golf, but to prove Orb API is **succinct**, and as Paul reminds us `succinctness is power <http://www.paulgraham.com/power.html>`_ (because we can do more with less code).

.. note::

    Same as for the CLI, the API will likely continue changing until v1. Once Orb reaches v1, the classes that have been included as being part of the official API will not change between minor versions, but only between major versions.

    Major version upgrades will also come with code migration guides.
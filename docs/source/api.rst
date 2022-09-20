Orb API
=======

Node Factory
------------

The first step to connecting to a node via the Python API is registering its connection details via :ref:`CLI`.

Once you have registered some nodes (e.g one of Orb's public nodes) you can create instances of :class:`orb.ln.ln.Ln` using the **factory** method:

.. code:: python

    from orb.ln import factory

    ln = factory("02234cf94dd9a4b76cb4767bf3da03b046c299307063b17c9c2e1886829df6a23a")

    print(cln.get_info())


Executing Orb API scripts
-------------------------

Since Orb's API or source code are not yet publically available, you can simply use the orb binary as you would the Python interpreter:

.. code:: bash

    $ orb my_script.py

Implementation heterogeneity
----------------------------

LN features a homogenous protocol with heterogenous implementations and programming languages; in other words, the protocol is the same, but different entities create their own implementations using different programming languages.

Famously, LND from `Lightning Labs <https://lightning.engineering>`_ is written in GoLang, and Core-Lightning from `Blockstream <https://blockstream.com>`_ is written in C. The miracle is that different entities have the freedom to do things their own way while speaking the same protocol; technological heterogeneity that adheres to the same protocol also (likely) leads to a more robust network and ecosystem (in the same way polycrops are likely more robust than monocrops). The disadvantage is that migrating from one node-type to another is currently impossible, and userbases may not communicate enough across implementations as they ought to.

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

For this reason, you can decide to directly access the implementation with the `concrete` attibute.

.. note::

    Please note the attribute name `concrete` may not be technically the correct one, since we're using composition, as opposed to an Abstract & Concrete relationship model.

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

Class Hierarchy
---------------

The class hierarchy is very shallow, with only :class:`orb.lnd.lnd_base.LndBase` and :class:`orb.cln.cln_base.ClnBase` base classes. The :class:`orb.ln.ln.Ln` class abstracts away all the implementation details, and its methods ultimately return an object from the :mod:`orb.ln.types` module.

.. mermaid::

    classDiagram
        LndBase <|-- LndGRPC
        LndBase <|-- LndREST
        ClnBase <|-- ClnGRPC
        ClnBase <|-- ClnREST

    Lnd --|> LndGRPC : Factory Method
    Lnd --|> LndREST : Factory Method
    Cln --|> ClnGRPC : Factory Method
    Cln --|> ClnREST : Factory Method

    Ln --|> LndGRPC : Execute
    Ln --|> LndREST : Execute
    Ln --|> ClnGRPC : Execute
    Ln --|> ClnREST : Execute

    Ln --|> Lnd : Factory Method
    Ln --|> Cln : Factory Method
    
    Ln --|> Types : Returns

The :meth:`orb.lnd.lnd.Lnd` and :meth:`orb.cln.cln.Cln` are `factory methods <https://en.wikipedia.org/wiki/Factory_(object-oriented_programming)>`_ that construct the correct type of object.

The :class:`orb.ln.ln.Ln` class wrangles method calls to the correct (LndGRPC, LndREST, ClnGRPC or ClnREST) class to make the implementations look alike.

A note for CLN REST developers
------------------------------

Orb's CLN REST API assumes `c-lightning-REST <https://github.com/Ride-The-Lightning/c-lightning-REST>`_, and methods that are not implemented in the class fallback to the `/v1/rpc <https://github.com/Ride-The-Lightning/c-lightning-REST#rpc>`_ endpoint.

As such, every rpc can be executed as `documented <https://lightning.readthedocs.io/>`_ using native Python syntax (so truely an RPC).


.. code:: python

    from orb.ln import factory

    cln = factory("02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764").concrete

    print(cln.feerates(style='perkb'))

Output:

.. code:: json

    {
        "api_version": "0.8.0",
        "onchain_fee_estimates": {
            "htlc_success_satoshis": 178,
            "htlc_timeout_satoshis": 168,
            "mutual_close_satoshis": 170,
            "opening_channel_satoshis": 177,
            "unilateral_close_satoshis": 151
        },
        "perkb": {
            "delayed_to_us": 1012,
            "htlc_resolution": 1012,
            "max_acceptable": 4294967295,
            "min_acceptable": 1012,
            "mutual_close": 1012,
            "opening": 1012,
            "penalty": 1012,
            "unilateral_close": 1012
        }
    }


.. code:: python

    from orb.ln import factory

    cln = factory(
        "02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764"
    ).concrete

    print(
        cln.getroute(
            id="0287c3e11b3fd5d879c8d1ee6e696048dab713be2f541ef0d2c4fff093120f216f",
            msatoshi=100_000,
            riskfactor=0,
        )
    )


Output:

.. code:: json

    {
        "api_version": "0.8.0",
        "route": [
            {
                "amount_msat": "100000msat",
                "channel": "163x1x1",
                "delay": 9,
                "direction": 0,
                "id": "0287c3e11b3fd5d879c8d1ee6e696048dab713be2f541ef0d2c4fff093120f216f",
                "msatoshi": 100000,
                "style": "tlv"
            }
        ]
    }


Once again, thanks to Python's `__getattr__` and the way RPCs are handled in Core Lightning (and its unofficial REST API) CLN REST developers can call every RPC method as documented on the core lightning read the docs site.

A note for REST developers
--------------------------

Both the ClnREST and LndREST class expose `_get` and `_post` methods, to call API endpoints directly. the `_post` method takes a `data` keyword argument, that takes a dict.

.. code:: python

    from orb.ln import factory

    cln = factory("02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764")

    print(cln._get("/v1/getBalance"))


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



Closing channels inactive channels
----------------------------------

Let's imagine a scenario where you opened channels, and are not even able to send payments through them at a reasonable PPM.

After some time, you may want to ask the following questions:

- Which channels have a high ratio?
- Of these, which sent less than 100_000 sats?

Then prompt the user whether to close them:

.. code:: python
    from orb.ln import factory

    ln = factory("03fbffb45604f2e0d481c323612e6681fd77eacf9bbe853e83300991de75cc7f78")

    for c in ln.get_channels():
        ratio = c.local_balance / c.capacity
        if ratio > 0.8:
            alias = ln.get_node_alias(c.remote_pubkey)
            print(alias)
            print(f"Total amount sent:     {c.total_satoshis_sent:_}")
            print(f"Total amount received: {c.total_satoshis_received:_}")
            if c.total_satoshis_sent < 100_000:
                if input(f"Close channel with: {alias} y/n: ").strip() == "y":
                    print(f"Closing: {c.chan_id}")
                    result = ln.close_channel(c.chan_id)
                    print(result)


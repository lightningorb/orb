Orb API
=======

Why Python
----------

Python is a simple and elegantly designed language that has stood the test of time. it is the `most searched language on the web <https://pypl.github.io/PYPL.html>`_, is broadly used in every field / industry / sector worldwide.

So in short, lindy effect, simplicity, and a great language if we want more lightning adoption.

Sending coins from LND to CLN in one line of code
-------------------------------------------------

Orb's API is the same whether we're interacting with an LND or Core-Lightning node. In this tutorial we'll learn how to send coins from LND to CLN in 1 line of code.

Let's begin by loading in a node, and printing basic info:

.. code:: python

    from orb.ln import factory

    lnd = factory("02234cf94dd9a4b76cb4767bf3da03b046c299307063b17c9c2e1886829df6a23a")

    print(lnd.get_info())

That's really easy. Now let's load in another node, and generate an address.

.. code:: python

    from orb.ln import factory

    lnd = factory("02234cf94dd9a4b76cb4767bf3da03b046c299307063b17c9c2e1886829df6a23a")
    cln = factory("03fbffb45604f2e0d481c323612e6681fd77eacf9bbe853e83300991de75cc7f78")

    cln_address = cln.new_address()
    print(cln_address)

Again, super easy: 5 lines of code thus far. Now let's send.

.. code:: python

    from orb.ln import factory

    lnd = factory("02234cf94dd9a4b76cb4767bf3da03b046c299307063b17c9c2e1886829df6a23a")
    cln = factory("03fbffb45604f2e0d481c323612e6681fd77eacf9bbe853e83300991de75cc7f78")

    cln_address = cln.new_address()

    res = lnd.send_coins(
        addr=cln_address.address,
        amount=100_000,
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
        amount=100_000,
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
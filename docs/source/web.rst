.. _web:

Orb Web
=======

Orb currently provides a simple Web interface into the currently active node.


You can view these pages live for `regtest.cln.lnorb.com <https://regtest.cln.lnorb.com>`_ and `signet.lnd.lnorb.com <https://regtest.cln.lnorb.com>`_.


.. image:: https://s3-us-east-2.amazonaws.com/lnorb/docs/Orb_2022-09-01_12-42-54.png
   :align: center
   :width: 800px


----------------------------------

To spawn the web interrace:

.. code:: bash

    $ orb web serve # --help

Writing a backend with FastAPI
------------------------------

Since Orb easily and homogenously interacts with LND's and CLN's APIs, it's fairly easy to extend the examples provided in the API documention to build Lightning-powered sites, apps and tooling of your own.

Let's begin by providing an `/api/info` backend point that delivers node info:

.. code:: python

    # my_ln_webapp.py

    import uvicorn
    from fastapi import FastAPI
    from orb.ln import factory


    webapp = FastAPI()
    ln = factory("02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764")


    @webapp.get("/api/info")
    def info():
        return ln.get_info().todict()


    if __name__ == "__main__":
        uvicorn.run(
            "my_ln_webapp:webapp", host="0.0.0.0", port=8080, reload=True, debug=True
        )

You can test your backend with:

.. code:: bash

    $ orb my_ln_webapp.py

.. code:: bash

    $ curl localhost:8080/api/info


Building a reactive frontend
----------------------------

Reactive frontends came in vogue with jquery, ajax, web2.0, nodejs, react etc. and web users became habituated to websites that behave like regular applications (DOM mutations taking place without page reloads or URL redirects).

Sadly, this movement has lead to a lot of web bloat. Lightning being a forward thinking ecosystem that is mindful of the web, Orb strong recommends the use of `Svelte <https://svelte.dev>`_ due to its very fast rendering speeds, and very low size footprint.

Svelte can be thought of more as a compiler than a framework, as it compiles the code into a very small `bundle.js` file (often around 80kb). This sets it a world apart from the bloat commonly generated with the node and NPM ecosystem.

WORK IN PROGRESS









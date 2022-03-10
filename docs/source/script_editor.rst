Script Editor
=============

.. warning::

    The script editor is currently at the 'experimental' stage. It works well for very small scripts, e.g maximum 4 or 5 lines. However for longer scripts, the current recommendation is to write an app using your favorite editor.

    The script editor cannot match the comfort of using an editor or IDE such as Sublime Text, MS Studio Code, Atom, PyCharm etc.

    It is also currently a little buggy. e.g Sometimes pasting code results in blank lines, etc.

.. image:: script_editor.png
   :align: center


The script editor enables users to write short scripts, and execute them within Orb's runtime environment.

.. note::

    The script editor's code is currently run using Python's ``exec``. Further research needs to be carried out to evaluate the pros and cons of ``exec`` over ``importlib.__import__``.

Below is a template that can be used to run many of the examples in LND's documentation.

.. code:: python

    import codecs, grpc, os
    from grpc_generated import lightning_pb2 as lnrpc
    from grpc_generated import lightning_pb2_grpc as lightningstub
    from orb.misc.prefs import hostname, cert, macaroon, grpc_port

    os.environ['GRPC_SSL_CIPHER_SUITES'] = 'HIGH+ECDSA'
    ssl_creds = grpc.ssl_channel_credentials(cert())
    channel = grpc.secure_channel(f'{hostname()}:{grpc_port()}', ssl_creds)
    stub = lightningstub.LightningStub(channel)

    print(stub)

To run the code, simply do: ``ctrl a`` followed by ``enter``, and clicking ``view > run``.

Script Editor Sizing Issues
---------------------------

The script editor may experience sizing issues if the screen resolution is changed. In this case, simply do ``View > Reset Split Size`` and restart Orb.

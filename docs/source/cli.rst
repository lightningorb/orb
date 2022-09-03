Orb CLI
=======

You should familiarise yourself with the Orb CLI (command line interface) as it enables you to perform some operations a lot more quickly than via the GUI (graphical user interface).

.. asciinema:: /_static/orb-cli-demo.cast

Locating the executable in a terminal
.....................................

If you have freshly installed Orb, you may want to open a terminal, and locate the executable.

OSX:

.. code:: bash

     /Applications/lnorb.app/Contents/MacOS/lnorb

Windows:

.. code:: bash

    C:\Users\Administrator\Downloads\orb-<version>-windows-<edition>-x86_64/lnorb/lnorb.exe

Linux:

.. code:: bash

    ~/Downloads/orb/main.py

.. note::

    In a future release of Orb, expect the executable to be named `orb`. Until then, mentally substitute `orb` with the correct executable name. In Linux and OSX, create an `Alias <https://www.tecmint.com/create-alias-in-linux/>`_. In Windows add your install directory to the `PATH <https://stackoverflow.com/questions/44272416/how-to-add-a-folder-to-path-environment-variable-in-windows-10-with-screensho>`_.


Running tests
.............

Orb comes with its pytest suite included, so that the build system can test the binary before making it available to the public, and so that users can test the build on their setup, too.

The test are safe to run: if you have existing nodes setup, the tests will not touch them; they'll only use alter the public nodes.

.. code:: bash

   $ orb test run-all-tests


Connecting to Orb's public nodes
................................

LND
~~~

To connect to LND via REST:

.. code:: bash

   $ orb node create-orb-public lnd rest 

Or to connect via GRPC:

.. code:: bash

   $ orb node create-orb-public lnd rest

Core-Lightning
--------------

To connect to Orb public Core-Lightning node via REST:

.. code:: bash

   $ orb node create-orb-public cln rest 

(please note, we are somewhat ignoring Core-Lighting's GRPC interface as it is still very new, and Orb can use all the existing RPC endpoints via REST).

------------------------

Showing node information
........................

The next thing you'll want to do is see what nodes are available to Orb:

.. code:: bash

   $ orb node list

Or show more information:

.. code:: bash

    $ orb node list --show-info

You may notice the information displayed is the same regardless of whether you are interacting with an LND or Core-Lightning node, and regardless of whether connecting over REST or GRPC.

Orb abstracts the implementation type, enabling you to get on with your daily operations in an implementation-independent way.

Commands and sub-commands
.........................

You may (or may not) be familiar with `git`. It uses commands, and subcommands, e.g:

.. code:: bash

    $ git origin add

Orb CLI works in exactly the same way.

.. code:: bash

    $ orb <command> <sub-command>

Arguments and Options
.....................

Arguments come after a sub-command, and do not require to be preceded by two dashes. Options on the other hand are preceded by two dashes, e.g `--use-node`.

CLI changes
...........

Deciding on how to group commands and sub-commands, and what should be an argument vs. an option etc. are hard design decisions, thus expect argument / option names, order etc. to change quite a lot for as long as Orb remains in v0.x.x.

Once Orb reaches v1, the API and CLI will become stable, and if there are breaking changes then Orb's major version will be incremented (to v2, v3 etc.).

This is a strict requirement, as a stable CLI / API enables you to use Orb in your own automation workflows without the fear of breaking changes when updating minor versions.

Getting help
............


.. code:: bash

    $ orb --help


Getting help on commands
~~~~~~~~~~~~~~~~~~~~~~~~~


.. code:: bash

    $ orb node --help


Getting help on sub-commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code:: bash

    $ orb node ssh-wizard --help

CLI reference
~~~~~~~~~~~~~

Now that are you are a bit more familiar with Orb's CLI, here's the full command reference.

**Usage**:

.. code:: console

    $ orb [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--install-completion``: Install completion for the current shell.
-  ``--show-completion``: Show completion for the current shell, to copy
   it or customize the installation.
-  ``--help``: Show this message and exit.

**Commands**:

-  ``chain``
-  ``channel``
-  ``invoice``
-  ``node``: Commands to perform operations on nodes.
-  ``pay``
-  ``peer``
-  ``rebalance``
-  ``test``
-  ``web``

``orb chain``
-------------

**Usage**:

.. code:: console

    $ orb chain [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``balance``: Get on-chain balance.
-  ``deposit``: Get an on-chain address to deposit BTC.
-  ``fees``: Get mempool chain fees.
-  ``send``: Send coins on-chain.

``orb chain balance``
~~~~~~~~~~~~~~~~~~~~~

Get on-chain balance.

**Usage**:

.. code:: console

    $ orb chain balance [OPTIONS] [PUBKEY]

**Arguments**:

-  ``[PUBKEY]``: The pubkey of the node. If not provided, use the
   default node.

**Options**:

-  ``--help``: Show this message and exit.

``orb chain deposit``
~~~~~~~~~~~~~~~~~~~~~

Get an on-chain address to deposit BTC.

**Usage**:

.. code:: console

    $ orb chain deposit [OPTIONS]

**Options**:

-  ``--pubkey TEXT``: [default: ]
-  ``--help``: Show this message and exit.

``orb chain fees``
~~~~~~~~~~~~~~~~~~

Get mempool chain fees. Currently these are the fees from mempool.space

**Usage**:

.. code:: console

    $ orb chain fees [OPTIONS]

**Options**:

-  ``--help``: Show this message and exit.

``orb chain send``
~~~~~~~~~~~~~~~~~~

Send coins on-chain.

**Usage**:

.. code:: console

    $ orb chain send [OPTIONS] ADDRESS SATOSHI SAT_PER_VBYTE [PUBKEY]

**Arguments**:

-  ``ADDRESS``: [required]
-  ``SATOSHI``: Amount to send, expressed in satoshis, or 'all'.
   [required]
-  ``SAT_PER_VBYTE``: Sat per vbyte to use for the transaction.
   [required]
-  ``[PUBKEY]``: The pubkey of the node. If not provided, use the
   default node.

**Options**:

-  ``--help``: Show this message and exit.

``orb channel``
---------------

**Usage**:

.. code:: console

    $ orb channel [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``list-forwards``: List forwards for the node.
-  ``open``: Open a channel.

``orb channel list-forwards``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List forwards for the node.

**Usage**:

.. code:: console

    $ orb channel list-forwards [OPTIONS] [PUBKEY]

**Arguments**:

-  ``[PUBKEY]``: The pubkey of the node. If not provided, use the
   default node.

**Options**:

-  ``--index-offset INTEGER``: Start index. [default: 0]
-  ``--num-max-events INTEGER``: Max number of events to return.
   [default: 100]
-  ``--help``: Show this message and exit.

``orb channel open``
~~~~~~~~~~~~~~~~~~~~

Open a channel.

**Usage**:

.. code:: console

    $ orb channel open [OPTIONS] PEER_PUBKEY AMOUNT_SATS SAT_PER_VBYTE

**Arguments**:

-  ``PEER_PUBKEY``: [required]
-  ``AMOUNT_SATS``: [required]
-  ``SAT_PER_VBYTE``: [required]

**Options**:

-  ``--pubkey TEXT``: [default: ]
-  ``--help``: Show this message and exit.

``orb invoice``
---------------

**Usage**:

.. code:: console

    $ orb invoice [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``generate``: Generate a bolt11 invoice.

``orb invoice generate``
~~~~~~~~~~~~~~~~~~~~~~~~

Generate a bolt11 invoice.

**Usage**:

.. code:: console

    $ orb invoice generate [OPTIONS] [SATOSHIS] [PUBKEY]

**Arguments**:

-  ``[SATOSHIS]``: The amount of Satoshis for this invoice. [default:
   1000]
-  ``[PUBKEY]``: The pubkey of the node. If not provided, use the
   default node.

**Options**:

-  ``--help``: Show this message and exit.

``orb node``
------------

Commands to perform operations on nodes.

**Usage**:

.. code:: console

    $ orb node [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``create``: Create node.
-  ``create-from-cert-files``: Create node and use certificate files.
-  ``create-orb-public``: Create public testnet node.
-  ``delete``: Delete node information.
-  ``info``: Get node information.
-  ``list``: Get a list of nodes known to Orb.
-  ``ssh-wizard``: SSH into the node, copy the cert and mac, and...
-  ``use``: Use the given node as default.

``orb node create``
~~~~~~~~~~~~~~~~~~~

Create node.

**Usage**:

.. code:: console

    $ orb node create [OPTIONS]

**Options**:

-  ``--hostname TEXT``: IP address or DNS-resolvable name for this host.
   [required]
-  ``--mac-hex TEXT``: The node macaroon in hex format. [required]
-  ``--node-type TEXT``: cln or lnd. [required]
-  ``--protocol TEXT``: rest or grpc. [required]
-  ``--network TEXT``: IP address or DNS-resovable name for this host.
   [required]
-  ``--cert-plain TEXT``: Plain node certificate. [required]
-  ``--rest-port INTEGER``: REST port. [default: 8080]
-  ``--grpc-port INTEGER``: GRPC port. [default: 10009]
-  ``--use-node / --no-use-node``: Whether to set as default. [default:
   True]
-  ``--help``: Show this message and exit.

``orb node create-from-cert-files``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create node and use certificate files.

**Usage**:

.. code:: console

    $ orb node create-from-cert-files [OPTIONS]

**Options**:

-  ``--hostname TEXT``: IP address or DNS-resolvable name for this host.
   [required]
-  ``--mac-file-path TEXT``: Path to the node macaroon. [required]
-  ``--node-type TEXT``: cln or lnd. [required]
-  ``--protocol TEXT``: rest or grpc. [required]
-  ``--network TEXT``: IP address or DNS-resovable name for this host.
   [required]
-  ``--cert-file-path TEXT``: Path to the node certificate. [required]
-  ``--rest-port INTEGER``: REST port. [default: 8080]
-  ``--grpc-port INTEGER``: GRPC port. [default: 10009]
-  ``--use-node / --no-use-node``: Whether to set as default. [default:
   True]
-  ``--help``: Show this message and exit.

``orb node create-orb-public``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create public testnet node.

**Usage**:

.. code:: console

    $ orb node create-orb-public [OPTIONS] NODE_TYPE PROTOCOL

**Arguments**:

-  ``NODE_TYPE``: lnd or cln. [required]
-  ``PROTOCOL``: rest or grpc. [required]

**Options**:

-  ``--use-node / --no-use-node``: Set this node as the default.
   [default: True]
-  ``--help``: Show this message and exit.

``orb node delete``
~~~~~~~~~~~~~~~~~~~

Delete node information.

**Usage**:

.. code:: console

    $ orb node delete [OPTIONS] [PUBKEY]

**Arguments**:

-  ``[PUBKEY]``: The pubkey of the node. If not provided, use the
   default node.

**Options**:

-  ``--help``: Show this message and exit.

``orb node info``
~~~~~~~~~~~~~~~~~

Get node information.

**Usage**:

.. code:: console

    $ orb node info [OPTIONS] [PUBKEY]

**Arguments**:

-  ``[PUBKEY]``: The pubkey of the node. If not provided, use the
   default node.

**Options**:

-  ``--help``: Show this message and exit.

``orb node list``
~~~~~~~~~~~~~~~~~

Get a list of nodes known to Orb.

**Usage**:

.. code:: console

    $ orb node list [OPTIONS]

**Options**:

-  ``--show-info / --no-show-info``: If True, then connect and print
   node information [default: False]
-  ``--help``: Show this message and exit.

``orb node ssh-wizard``
~~~~~~~~~~~~~~~~~~~~~~~

SSH into the node, copy the cert and mac, and create the node.

**Usage**:

.. code:: console

    $ orb node ssh-wizard [OPTIONS]

**Options**:

-  ``--hostname TEXT``: IP address or DNS-resolvable name for this host.
   [required]
-  ``--node-type TEXT``: cln or lnd. [required]
-  ``--ssh-cert-path PATH``: Certificate to use for the SSH session.
-  ``--ssh-password TEXT``: Password to use for the SSH session.
-  ``--ln-cert-path PATH``: Path of the node certificate on the target
   host.
-  ``--ln-macaroon-path PATH``: Path of the node macaroon on the target
   host.
-  ``--network TEXT``: IP address or DNS-resovable name for this host.
   [required]
-  ``--protocol TEXT``: rest or grpc. [required]
-  ``--rest-port INTEGER``: REST port. [default: 8080]
-  ``--grpc-port INTEGER``: GRPC port. [default: 10009]
-  ``--ssh-user TEXT``: Username for SSH session. [default: ubuntu]
-  ``--ssh-port INTEGER``: Port for SSH session. [default: 22]
-  ``--use-node / --no-use-node``: Whether to set as default. [default:
   True]
-  ``--help``: Show this message and exit.

``orb node use``
~~~~~~~~~~~~~~~~

Use the given node as default.

**Usage**:

.. code:: console

    $ orb node use [OPTIONS] [PUBKEY]

**Arguments**:

-  ``[PUBKEY]``: The pubkey of the node.

**Options**:

-  ``--help``: Show this message and exit.

``orb pay``
-----------

**Usage**:

.. code:: console

    $ orb pay [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``invoices``: Pay Ingested Invoices
-  ``lnurl``: Generate bolt11 invoices from LNURL, and pay...

``orb pay invoices``
~~~~~~~~~~~~~~~~~~~~

Pay Ingested Invoices

**Usage**:

.. code:: console

    $ orb pay invoices [OPTIONS]

**Options**:

-  ``--chan-id TEXT``
-  ``--max-paths INTEGER``: [default: 10000]
-  ``--fee-rate INTEGER``: [default: 500]
-  ``--time-pref FLOAT``: [default: 0]
-  ``--num-threads INTEGER``: [default: 5]
-  ``--pubkey TEXT``: [default: ]
-  ``--help``: Show this message and exit.

``orb pay lnurl``
~~~~~~~~~~~~~~~~~

Generate bolt11 invoices from LNURL, and pay them.

**Usage**:

.. code:: console

    $ orb pay lnurl [OPTIONS] URL

**Arguments**:

-  ``URL``: [required]

**Options**:

-  ``--total-amount-sat INTEGER``: [default: 100000000]
-  ``--chunks INTEGER``: [default: 100]
-  ``--num-threads INTEGER``: [default: 5]
-  ``--rate-limit INTEGER``: [default: 5]
-  ``--pubkey TEXT``: [default: ]
-  ``--wait / --no-wait``: [default: True]
-  ``--chan-id TEXT``
-  ``--max-paths INTEGER``: [default: 10000]
-  ``--fee-rate INTEGER``: [default: 500]
-  ``--time-pref FLOAT``: [default: 0]
-  ``--help``: Show this message and exit.

``orb peer``
------------

**Usage**:

.. code:: console

    $ orb peer [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``connect``: Connect to a peer.
-  ``list``: List peers.

``orb peer connect``
~~~~~~~~~~~~~~~~~~~~

Connect to a peer.

**Usage**:

.. code:: console

    $ orb peer connect [OPTIONS] PEER_PUBKEY

**Arguments**:

-  ``PEER_PUBKEY``: [required]

**Options**:

-  ``--pubkey TEXT``: [default: ]
-  ``--help``: Show this message and exit.

``orb peer list``
~~~~~~~~~~~~~~~~~

List peers.

**Usage**:

.. code:: console

    $ orb peer list [OPTIONS]

**Options**:

-  ``--pubkey TEXT``: [default: ]
-  ``--help``: Show this message and exit.

``orb rebalance``
-----------------

**Usage**:

.. code:: console

    $ orb rebalance [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``rebalance``: Rebalance the node

``orb rebalance rebalance``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Rebalance the node

**Usage**:

.. code:: console

    $ orb rebalance rebalance [OPTIONS]

**Options**:

-  ``--amount INTEGER``: [default: 1000]
-  ``--chan-id TEXT``
-  ``--last-hop-pubkey TEXT``
-  ``--max-paths INTEGER``: [default: 10000]
-  ``--fee-rate INTEGER``: [default: 500]
-  ``--time-pref FLOAT``: [default: 0]
-  ``--node TEXT``: [default:
   0227750e13a6134c1f1e510542a88e3f922107df8ef948fc3ff2a296fca4a12e47]
-  ``--help``: Show this message and exit.

``orb test``
------------

**Usage**:

.. code:: console

    $ orb test [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``run-all-tests``: Run all tests.

``orb test run-all-tests``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Run all tests.

**Usage**:

.. code:: console

    $ orb test run-all-tests [OPTIONS]

**Options**:

-  ``--help``: Show this message and exit.

``orb web``
-----------

**Usage**:

.. code:: console

    $ orb web [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``serve``: Serve the Orb web app.

``orb web serve``
~~~~~~~~~~~~~~~~~

Serve the Orb web app.

**Usage**:

.. code:: console

    $ orb web serve [OPTIONS]

**Options**:

-  ``--host TEXT``: The allowed host. [default: 0.0.0.0]
-  ``--port INTEGER``: The port to serve. [default: 8080]
-  ``--reload / --no-reload``: Live reloading (dev). [default: False]
-  ``--debug / --no-debug``: Show debug info (dev). [default: False]
-  ``--workers INTEGER``: Number of web workers. [default: 1]
-  ``--help``: Show this message and exit.

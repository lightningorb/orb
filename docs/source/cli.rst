CLI
===

**Usage**:

.. code:: console

    $ [OPTIONS] COMMAND [ARGS]...

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

``chain``
---------

**Usage**:

.. code:: console

    $ chain [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``deposit``: Get an on-chain address to deposit BTC.
-  ``fees``: Get mempool chain fees.
-  ``send``: Send coins on-chain.

``chain deposit``
~~~~~~~~~~~~~~~~~

Get an on-chain address to deposit BTC.

            orb chain.deposit

deposit\_address tb1q0wfpxdeh8wyvfcaxdxfrxj7qp753s47vu683ax deposit\_qr:

█▀▀▀▀▀█ ▄█▄ ▄▄█ ██ █▀▀▀▀▀█ ... ▀▀▀▀▀▀▀ ▀▀▀ ▀ ▀▀▀▀ ▀ ▀▀

**Usage**:

.. code:: console

    $ chain deposit [OPTIONS]

**Options**:

-  ``--pubkey TEXT``: [default: ]
-  ``--help``: Show this message and exit.

``chain fees``
~~~~~~~~~~~~~~

Get mempool chain fees. Currently these are the fees from mempool.space

            orb chain.fees

fastestFee : 7 sat/vbyte halfHourFee : 1 sat/vbyte hourFee : 1 sat/vbyte
economyFee : 1 sat/vbyte minimumFee : 1 sat/vbyte

**Usage**:

.. code:: console

    $ chain fees [OPTIONS]

**Options**:

-  ``--help``: Show this message and exit.

``chain send``
~~~~~~~~~~~~~~

Send coins on-chain.

            orb chain.send --amount 10\_000 --sat-per-vbyte 1 --address
            tb1q0wfpxdeh8wyvfcaxdxfrxj7qp753s47vu683ax

{ "txid":
"41ffa0fa564db85e65515fb3c3e2fe95d6a403c0f3473575dcad2bbde962c052" }

**Usage**:

.. code:: console

    $ chain send [OPTIONS] ADDRESS AMOUNT SAT_PER_VBYTE

**Arguments**:

-  ``ADDRESS``: [required]
-  ``AMOUNT``: [required]
-  ``SAT_PER_VBYTE``: [required]

**Options**:

-  ``--pubkey TEXT``: [default: ]
-  ``--help``: Show this message and exit.

``channel``
-----------

**Usage**:

.. code:: console

    $ channel [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``open``: Open a channel.

``channel open``
~~~~~~~~~~~~~~~~

Open a channel.

**Usage**:

.. code:: console

    $ channel open [OPTIONS] PEER_PUBKEY AMOUNT_SATS SAT_PER_VBYTE

**Arguments**:

-  ``PEER_PUBKEY``: [required]
-  ``AMOUNT_SATS``: [required]
-  ``SAT_PER_VBYTE``: [required]

**Options**:

-  ``--pubkey TEXT``: [default: ]
-  ``--help``: Show this message and exit.

``invoice``
-----------

**Usage**:

.. code:: console

    $ invoice [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``generate``: Generate a bolt11 invoice.

``invoice generate``
~~~~~~~~~~~~~~~~~~~~

Generate a bolt11 invoice.

**Usage**:

.. code:: console

    $ invoice generate [OPTIONS] [SATOSHIS] [PUBKEY]

**Arguments**:

-  ``[SATOSHIS]``: The amount of Satoshis for this invoice. [default:
   1000]
-  ``[PUBKEY]``: The pubkey of the node. If not provided, use the
   default node.

**Options**:

-  ``--help``: Show this message and exit.

``node``
--------

Commands to perform operations on nodes.

**Usage**:

.. code:: console

    $ node [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``balance``: Get total balance, for both on-chain and...
-  ``create``: Create node.
-  ``create-from-cert-files``: Create node and use certificate files.
-  ``create-orb-public``: Create public testnet node.
-  ``delete``: Delete node information.
-  ``info``: Get node information.
-  ``list``: Get a list of nodes known to Orb.
-  ``ssh-wizard``: SSH into the node, copy the cert and mac, and...
-  ``use``: Use the given node as default.

``node balance``
~~~~~~~~~~~~~~~~

Get total balance, for both on-chain and balance in channels.

WIP: this is not yet implemented for CLN.

**Usage**:

.. code:: console

    $ node balance [OPTIONS] [PUBKEY]

**Arguments**:

-  ``[PUBKEY]``: The pubkey of the node. If not provided, use the
   default node.

**Options**:

-  ``--help``: Show this message and exit.

``node create``
~~~~~~~~~~~~~~~

Create node.

**Usage**:

.. code:: console

    $ node create [OPTIONS]

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

``node create-from-cert-files``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create node and use certificate files.

**Usage**:

.. code:: console

    $ node create-from-cert-files [OPTIONS]

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

``node create-orb-public``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Create public testnet node.

**Usage**:

.. code:: console

    $ node create-orb-public [OPTIONS] NODE_TYPE PROTOCOL

**Arguments**:

-  ``NODE_TYPE``: lnd or cln. [required]
-  ``PROTOCOL``: rest or grpc. [required]

**Options**:

-  ``--use-node / --no-use-node``: Set this node as the default.
   [default: True]
-  ``--help``: Show this message and exit.

``node delete``
~~~~~~~~~~~~~~~

Delete node information.

**Usage**:

.. code:: console

    $ node delete [OPTIONS] [PUBKEY]

**Arguments**:

-  ``[PUBKEY]``: The pubkey of the node. If not provided, use the
   default node.

**Options**:

-  ``--help``: Show this message and exit.

``node info``
~~~~~~~~~~~~~

Get node information.

**Usage**:

.. code:: console

    $ node info [OPTIONS] [PUBKEY]

**Arguments**:

-  ``[PUBKEY]``: The pubkey of the node. If not provided, use the
   default node.

**Options**:

-  ``--help``: Show this message and exit.

``node list``
~~~~~~~~~~~~~

Get a list of nodes known to Orb.

**Usage**:

.. code:: console

    $ node list [OPTIONS]

**Options**:

-  ``--show-info / --no-show-info``: If True, then connect and print
   node information [default: False]
-  ``--help``: Show this message and exit.

``node ssh-wizard``
~~~~~~~~~~~~~~~~~~~

SSH into the node, copy the cert and mac, and create the node.

**Usage**:

.. code:: console

    $ node ssh-wizard [OPTIONS]

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

``node use``
~~~~~~~~~~~~

Use the given node as default.

**Usage**:

.. code:: console

    $ node use [OPTIONS] [PUBKEY]

**Arguments**:

-  ``[PUBKEY]``: The pubkey of the node.

**Options**:

-  ``--help``: Show this message and exit.

``pay``
-------

**Usage**:

.. code:: console

    $ pay [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``invoices``: Pay Ingested Invoices
-  ``lnurl``: Generate bolt11 invoices from LNURL, and pay...

``pay invoices``
~~~~~~~~~~~~~~~~

Pay Ingested Invoices

**Usage**:

.. code:: console

    $ pay invoices [OPTIONS] C

**Arguments**:

-  ``C``: [required]

**Options**:

-  ``--chan-id TEXT``
-  ``--max-paths INTEGER``: [default: 10000]
-  ``--fee-rate INTEGER``: [default: 500]
-  ``--time-pref FLOAT``: [default: 0]
-  ``--num-threads INTEGER``: [default: 5]
-  ``--node TEXT``: [default:
   02234cf94dd9a4b76cb4767bf3da03b046c299307063b17c9c2e1886829df6a23a]
-  ``--help``: Show this message and exit.

``pay lnurl``
~~~~~~~~~~~~~

Generate bolt11 invoices from LNURL, and pay them.

**Usage**:

.. code:: console

    $ pay lnurl [OPTIONS] C URL

**Arguments**:

-  ``C``: [required]
-  ``URL``: [required]

**Options**:

-  ``--total-amount-sat INTEGER``: [default: 100000000]
-  ``--chunks INTEGER``: [default: 100]
-  ``--num-threads INTEGER``: [default: 5]
-  ``--rate-limit INTEGER``: [default: 5]
-  ``--pubkey TEXT``: [default:
   02234cf94dd9a4b76cb4767bf3da03b046c299307063b17c9c2e1886829df6a23a]
-  ``--wait / --no-wait``: [default: True]
-  ``--chan-id TEXT``
-  ``--max-paths INTEGER``: [default: 10000]
-  ``--fee-rate INTEGER``: [default: 500]
-  ``--time-pref FLOAT``: [default: 0]
-  ``--help``: Show this message and exit.

``peer``
--------

**Usage**:

.. code:: console

    $ peer [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``connect``: Connect to a peer.
-  ``list``: List peers.

``peer connect``
~~~~~~~~~~~~~~~~

Connect to a peer.

**Usage**:

.. code:: console

    $ peer connect [OPTIONS] PEER_PUBKEY

**Arguments**:

-  ``PEER_PUBKEY``: [required]

**Options**:

-  ``--pubkey TEXT``: [default: ]
-  ``--help``: Show this message and exit.

``peer list``
~~~~~~~~~~~~~

List peers.

**Usage**:

.. code:: console

    $ peer list [OPTIONS]

**Options**:

-  ``--pubkey TEXT``: [default: ]
-  ``--help``: Show this message and exit.

``rebalance``
-------------

**Usage**:

.. code:: console

    $ rebalance [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``rebalance``: Rebalance the node

``rebalance rebalance``
~~~~~~~~~~~~~~~~~~~~~~~

Rebalance the node

**Usage**:

.. code:: console

    $ rebalance rebalance [OPTIONS] C

**Arguments**:

-  ``C``: [required]

**Options**:

-  ``--amount INTEGER``: [default: 1000]
-  ``--chan-id TEXT``
-  ``--last-hop-pubkey TEXT``
-  ``--max-paths INTEGER``: [default: 10000]
-  ``--fee-rate INTEGER``: [default: 500]
-  ``--time-pref FLOAT``: [default: 0]
-  ``--node TEXT``: [default:
   02234cf94dd9a4b76cb4767bf3da03b046c299307063b17c9c2e1886829df6a23a]
-  ``--help``: Show this message and exit.

``test``
--------

**Usage**:

.. code:: console

    $ test [OPTIONS] COMMAND [ARGS]...

**Options**:

-  ``--help``: Show this message and exit.

**Commands**:

-  ``run-all-tests``: Run all tests.

``test run-all-tests``
~~~~~~~~~~~~~~~~~~~~~~

Run all tests.

**Usage**:

.. code:: console

    $ test run-all-tests [OPTIONS]

**Options**:

-  ``--help``: Show this message and exit.

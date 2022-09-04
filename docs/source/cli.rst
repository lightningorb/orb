Orb CLI
=======

You should familiarise yourself with the Orb CLI (command line interface) as it enables you to perform some operations a lot more quickly than via the GUI (graphical user interface).

.. asciinema:: /_static/orb-cli-demo.cast

Locating the executable in a terminal
-------------------------------------

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
-------------

Orb comes with its pytest suite included, so that the build system can test the binary before making it available to the public, and so that users can test the build on their setup, too.

The test are safe to run: if you have existing nodes setup, the tests will not touch them; they'll only use alter the public nodes.

.. code:: bash

   $ orb test run-all-tests


Connecting to Orb's public nodes
--------------------------------

LND
^^^

To connect to LND via REST:

.. code:: bash

   $ orb node create-orb-public lnd rest 

Or to connect via GRPC:

.. code:: bash

   $ orb node create-orb-public lnd rest

Core-Lightning
^^^^^^^^^^^^^^

To connect to Orb public Core-Lightning node via REST:

.. code:: bash

   $ orb node create-orb-public cln rest 

(please note, we are somewhat ignoring Core-Lighting's GRPC interface as it is still very new, and Orb can use all the existing RPC endpoints via REST).

------------------------

Showing node information
------------------------

The next thing you'll want to do is see what nodes are available to Orb:

.. code:: bash

   $ orb node list

Or show more information:

.. code:: bash

    $ orb node list --show-info

You may notice the information displayed is the same regardless of whether you are interacting with an LND or Core-Lightning node, and regardless of whether connecting over REST or GRPC.

Orb abstracts the implementation type, enabling you to get on with your daily operations in an implementation-independent way.

Commands and sub-commands
-------------------------

You may (or may not) be familiar with `git`. It uses commands, and subcommands, e.g:

.. code:: bash

    $ git origin add

Orb CLI works in exactly the same way.

.. code:: bash

    $ orb <command> <sub-command>

Arguments and Options
---------------------

Arguments come after a sub-command, and do not require to be preceded by two dashes. Options on the other hand are preceded by two dashes, e.g `--use-node`.

CLI changes
-----------

Deciding on how to group commands and sub-commands, and what should be an argument vs. an option etc. are hard design decisions, thus expect argument / option names, order etc. to change quite a lot for as long as Orb remains in v0.x.x.

Once Orb reaches v1, the API and CLI will become stable, and if there are breaking changes then Orb's major version will be incremented (to v2, v3 etc.).

This is a strict requirement, as a stable CLI / API enables you to use Orb in your own automation workflows without the fear of breaking changes when updating minor versions.

Getting help
------------


.. code:: bash

    $ orb --help


Getting help on commands
^^^^^^^^^^^^^^^^^^^^^^^^


.. code:: bash

    $ orb node --help


Getting help on sub-commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. code:: bash

    $ orb node ssh-wizard --help

CLI reference
=============

Now that are you are a bit more familiar with Orb's CLI, here's the full command reference.


.. toctree::
   :maxdepth: 1
   :glob:
   :caption: Sub Commands:

   cli/orb_chain_balance
   cli/orb_chain_deposit
   cli/orb_chain_fees
   cli/orb_chain_send
   cli/orb_channel_list-forwards
   cli/orb_channel_open
   cli/orb_invoice_generate
   cli/orb_network_get-route
   cli/orb_node_create
   cli/orb_node_create-from-cert-files
   cli/orb_node_create-orb-public
   cli/orb_node_delete
   cli/orb_node_info
   cli/orb_node_list
   cli/orb_node_ssh-wizard
   cli/orb_node_use
   cli/orb_pay_invoices
   cli/orb_pay_lnurl
   cli/orb_peer_connect
   cli/orb_peer_list
   cli/orb_rebalance_rebalance
   cli/orb_test_run-all-tests
   cli/orb_web_serve

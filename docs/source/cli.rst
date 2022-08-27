ORB CLI
========



The ORB CLI executes similarly regardless of the node
implementation. Currently only LND and CLN are supported.

Setting an alias
----------------

You may want to consider creating an alias, to run Orb
from any path on your system. On Linux you'd want to
add this to your .bashrc:

alias orb='/opt/orb/main.py ${*}'

Listing Commands
----------------

Appending `-l` lists all the available commands.

orb -l


Listing Collection Commands
---------------------------

Appending `-l` followed by the name of the collection
lists all commands available in the given collection.

orb -l node


Getting help on individual commands
-----------------------------------

To get help on individual commands, prepend the command
with `--help`.

orb --help node.use


``orb chain.fees``
-----------

.. code:: bash

    Usage: main.py [--core-opts] chain.fees [other tasks here ...]
    
    Docstring:
      Get mempool chain fees. Currently these are the fees from
      mempool.space
    
      >>> orb chain.fees
    
      fastestFee      : 7 sat/vbyte
      halfHourFee     : 1 sat/vbyte
      hourFee         : 1 sat/vbyte
      economyFee      : 1 sat/vbyte
      minimumFee      : 1 sat/vbyte
    
    Options:
      none
    
    

``orb chain.deposit``
-----------

.. code:: bash

    Usage: main.py [--core-opts] chain.deposit [--options] [other tasks here ...]
    
    Docstring:
      Get an on-chain address to deposit BTC.
    
      >>> orb chain.deposit
    
      deposit_address tb1q0wfpxdeh8wyvfcaxdxfrxj7qp753s47vu683ax
      deposit_qr:
    
      █▀▀▀▀▀█ ▄█▄  ▄▄█  ██  █▀▀▀▀▀█
      ...
      ▀▀▀▀▀▀▀ ▀▀▀  ▀   ▀▀▀▀    ▀ ▀▀
    
    Options:
      -p STRING, --pubkey=STRING
    
    

``orb chain.send``
-----------

.. code:: bash

    Usage: main.py [--core-opts] chain.send [--options] [other tasks here ...]
    
    Docstring:
      Send coins on-chain.
    
      >>> orb chain.send --amount 10_000 --sat-per-vbyte 1 --address tb1q0wfpxdeh8wyvfcaxdxfrxj7qp753s47vu683ax
    
      {
          "txid": "41ffa0fa564db85e65515fb3c3e2fe95d6a403c0f3473575dcad2bbde962c052"
      }
    
    Options:
      -a STRING, --address=STRING         The destination address
      -m STRING, --amount=STRING          The amount to send in satoshis (for CLN
                                          this can be 'all')
      -p STRING, --pubkey=STRING          The node pubkey from which to send coins
      -s STRING, --sat-per-vbyte=STRING   Sats per vB (for CLN this can be slow,
                                          normal, urgent, or None)
    
    

``orb node.delete``
-----------

.. code:: bash

    Usage: main.py [--core-opts] node.delete [--options] [other tasks here ...]
    
    Docstring:
      Delete node information.
    
    Options:
      -p STRING, --pubkey=STRING
    
    

``orb node.list``
-----------

.. code:: bash

    Usage: main.py [--core-opts] node.list [--options] [other tasks here ...]
    
    Docstring:
      Get a list of nodes known to Orb.
    
    
      >>> orb node.list
    
      0227750e13a6134c1f1e510542a88e3f922107df8ef948fc3ff2a296fca4a12e47
      02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764
    
      >>> orb node.list --show-info
    
      Showing info for: 0227750e13a6134c1f1e510542a88e3f922107df8ef948fc3ff2a296fca4a12e47:
      alias: signet.lnd.lnorb.com
      ...
    
      Showing info for: 02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764:
      alias: regtest.cln.lnorb.com
      ...
    
    Options:
      -s, --show-info   If True, then connect and return node information
    
    

``orb node.info``
-----------

.. code:: bash

    Usage: main.py [--core-opts] node.info [--options] [other tasks here ...]
    
    Docstring:
      Get node information.
    
      >>> orb node.info
    
      alias: signet.lnd.lnorb.com
      identity_pubkey: 0227750e13a6134c1f1e510542a88e3f922107df8ef948fc3ff2a296fca4a12e47
      ...
    
    Options:
      -p STRING, --pubkey=STRING   The Pubkey to use as the default pubkey for all
                                   Orb commands
    
    

``orb node.balance``
-----------

.. code:: bash

    Usage: main.py [--core-opts] node.balance [--options] [other tasks here ...]
    
    Docstring:
      Get total balance, for both on-chain and balance in channels.
    
    Options:
      -p STRING, --pubkey=STRING
    
    

``orb node.use``
-----------

.. code:: bash

    Usage: main.py [--core-opts] node.use [--options] [other tasks here ...]
    
    Docstring:
      Use the given node as default.
    
    Options:
      -p STRING, --pubkey=STRING   The Pubkey to use as the default pubkey for all
                                   Orb commands
    
    

``orb node.create-orb-public``
-----------

.. code:: bash

    Usage: main.py [--core-opts] node.create-orb-public [--options] [other tasks here ...]
    
    Docstring:
      Create public testnet node.
    
      >>> orb node.create-orb-public rest lnd
    
      Encrypting mac
      Encrypting cert
      Connecting to: signet.lnd.lnorb.com
      Connected to: 0227750e13a6134c1f1e510542a88e3f922107df8ef948fc3ff2a296fca4a12e47
      orb_0227750e13a6134c1f1e510542a88e3f922107df8ef948fc3ff2a296fca4a12e47 created
      orb_0227750e13a6134c1f1e510542a88e3f922107df8ef948fc3ff2a296fca4a12e47/orb_0227750e13a6134c1f1e510542a88e3f922107df8ef948fc3ff2a296fca4a12e47.ini created
      Setting 0227750e13a6134c1f1e510542a88e3f922107df8ef948fc3ff2a296fca4a12e47 as default
    
      >>> orb node.create-orb-public grpc lnd # Also valid
      >>> orb node.create-orb-public rest cln # Also valid
    
    Options:
      -n STRING, --node-type=STRING   lnd or cln
      -p STRING, --protocol=STRING    rest or grpc
      -u, --[no-]use-node             Set this node as the default. (Default: True)
    
    

``orb node.create``
-----------

.. code:: bash

    Usage: main.py [--core-opts] node.create [--options] [other tasks here ...]
    
    Docstring:
      Create node.
    
      >>> orb node.create         --hostname regtest.cln.lnorb.com         --node-type cln         --protocol rest         --network regtest         --rest-port 3001         --mac-hex ...         --cert-plain ...
    
      Encrypting mac
      Encrypting cert
      Connecting to: regtest.cln.lnorb.com
      Connected to: 02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764
      /Users/w/Library/Application Support/orb_02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764 created
      /Users/w/Library/Application Support/orb_02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764/orb_02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764.ini created
      Setting 02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764 as default
    
    Options:
      -c STRING, --cert-plain=STRING
      -e STRING, --network=STRING      mainnet / testnet / signet / regtest
      -g INT, --grpc-port=INT          GRPC port (default: 10009)
      -h STRING, --hostname=STRING     IP address or DNS-resovable name for this
                                       host
      -m STRING, --mac-hex=STRING      Macaroon in hex format
      -n STRING, --node-type=STRING    cln or lnd
      -p STRING, --protocol=STRING     rest or grpc
      -r INT, --rest-port=INT          REST port (default: 8080)
      -u, --[no-]use-node              Set this node as the default (default:
                                       True).
    
    

``orb node.create-from-cert-files``
-----------

.. code:: bash

    Usage: main.py [--core-opts] node.create-from-cert-files [--options] [other tasks here ...]
    
    Docstring:
      Create node and use certificate files.
    
      Create node.
    
      >>> orb node.create-from-cert-files         --hostname regtest.cln.lnorb.com         --node-type cln         --protocol rest         --network regtest         --rest-port 3001         --mac-file-path ...         --cert-file-path ...
    
      Encrypting mac
      Encrypting cert
      Connecting to: regtest.cln.lnorb.com
      Connected to: 02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764
      /Users/w/Library/Application Support/orb_02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764 created
      /Users/w/Library/Application Support/orb_02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764/orb_02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764.ini created
      Setting 02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764 as default
    
    Options:
      -c STRING, --cert-file-path=STRING
      -e STRING, --network=STRING          mainnet / testnet / signet / regtest
      -g INT, --grpc-port=INT              GRPC port (default: 10009)
      -h STRING, --hostname=STRING         IP address or DNS-resovable name for
                                           this host
      -m STRING, --mac-file-path=STRING
      -n STRING, --node-type=STRING        cln or lnd
      -p STRING, --protocol=STRING         rest or grpc
      -r INT, --rest-port=INT              REST port (default: 8080)
      -u, --[no-]use-node                  Set this node as the default (default:
                                           True).
    
    

``orb node.ssh-wizard``
-----------

.. code:: bash

    Usage: main.py [--core-opts] node.ssh-wizard [--options] [other tasks here ...]
    
    Docstring:
      SSH into the node, and figure things out.
    
      >>> orb node.ssh-wizard         --hostname regtest.cln.lnorb.com         --node-type cln         --ssh-cert-path ...         --network regtest         --rest-port 3001         --protocol rest         --ln-cert-path /home/ubuntu/dev/regtest-workbench/certificate.pem         --ln-macaroon-path=/home/ubuntu/dev/regtest-workbench/access.macaroon 
    
      ssh session connected!
      OS:       Linux
      Hostname: ip-172-31-36-137
      Securely copying: /home/ubuntu/dev/regtest-workbench/certificate.pem
      Securely copying: /home/ubuntu/dev/regtest-workbench/access.macaroon
      Encrypting: /var/folders/6j/hb2nbc0x1hgfvkpy_kp72jpc0000gt/T/tmpmcuc9hju/certificate.pem
      Encrypting: /var/folders/6j/hb2nbc0x1hgfvkpy_kp72jpc0000gt/T/tmpmcuc9hju/access.macaroon
      Encrypting mac
      Encrypting cert
      Connecting to: regtest.cln.lnorb.com
      Connected to: 02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764
      /Users/w/Library/Application Support/orb_02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764/orb_02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764.ini created
      Setting 02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764 as default
    
    Options:
      --=STRING, --ssh-password=STRING       SSH session password (if not using a
                                             pem certificate)
      -d, --[no-]use-node                    Set this node as the default (Default:
                                             True).
      -e STRING, --network=STRING            mainnet / testnet / signet / regtest
      -g INT, --grpc-port=INT                GRPC port (default: 10009)
      -h STRING, --hostname=STRING           IP address or DNS-resovable name for
                                             this host
      -l STRING, --ln-cert-path=STRING       The path of the cert file on the
                                             target host
      -m STRING, --ln-macaroon-path=STRING   The path of the macaroon file on the
                                             target host
      -n STRING, --node-type=STRING          cln or lnd
      -o INT, --ssh-port=INT                 SSH session port to use, if not
                                             already specified in .ssh/config.
                                             (Default: 22).
      -p STRING, --protocol=STRING           Connect via rest or grpc. (Default:
                                             rest).
      -r INT, --rest-port=INT                REST port (default: 8080)
      -s STRING, --ssh-cert-path=STRING      SSH session certificate, if not
                                             already specified in .ssh/config
      -u STRING, --ssh-user=STRING           SSH session user, if not already
                                             specified in .ssh/config. (Default:
                                             22).
    
    

``orb invoice.lnurl-generate``
-----------

.. code:: bash

    Usage: main.py [--core-opts] invoice.lnurl-generate [--options] [other tasks here ...]
    
    Docstring:
      Generate bolt11 invoices from LNURL.
    
    Options:
      -c INT, --chunks=INT             The number of chunks total-amount-sat is
                                       broken up into.
      -n INT, --num-threads=INT        Make sure there are num-threads invoices
                                       available at any given time.
      -p STRING, --pubkey=STRING       The Pubkey to use as the default pubkey for
                                       all Orb commands.
      -r INT, --rate-limit=INT         Wait rate-limit seconds between each call to
                                       the LNURL generation endpoint.
      -t INT, --total-amount-sat=INT   The sum of the amount of all paid invoices
                                       should add up to total-amount-sat.
      -u STRING, --url=STRING          The LNURL in the form LNURL....
      -w, --[no-]wait                  Wait for payments to complete (setting this
                                       to False is only used for testing purposes).
    
    

``orb invoice.generate``
-----------

.. code:: bash

    Usage: main.py [--core-opts] invoice.generate [--options] [other tasks here ...]
    
    Docstring:
      Generate bolt11 invoices.
    
    Options:
      -p STRING, --pubkey=STRING   The Pubkey to use as the default pubkey for all
                                   Orb commands
      -s INT, --satoshis=INT
    
    

``orb invoice.ingest``
-----------

.. code:: bash

    Usage: main.py [--core-opts] invoice.ingest [--options] [other tasks here ...]
    
    Docstring:
      Ingest invoice into invoices DB.
    
    Options:
      -b STRING, --bolt11-invoice=STRING
      -p STRING, --pubkey=STRING           The Pubkey to use as the default pubkey
                                           for all Orb commands
    
    

``orb pay.invoices``
-----------

.. code:: bash

    Usage: main.py [--core-opts] pay.invoices [--options] [other tasks here ...]
    
    Docstring:
      Pay Ingested Invoices
    
    Options:
      -c STRING, --chan-id=STRING
      -f INT, --fee-rate=INT
      -m INT, --max-paths=INT
      -n INT, --num-threads=INT
      -o STRING, --node=STRING
      -t INT, --time-pref=INT
    
    

``orb pay.lnurl``
-----------

.. code:: bash

    Usage: main.py [--core-opts] pay.lnurl [--options] [other tasks here ...]
    
    Docstring:
      Generate bolt11 invoices from LNURL, and pay them.
    
    Options:
      -c INT, --chunks=INT             The number of chunks total-amount-sat is
                                       broken up into.
      -f INT, --fee-rate=INT
      -h STRING, --chan-id=STRING
      -i INT, --time-pref=INT
      -m INT, --max-paths=INT
      -n INT, --num-threads=INT        Make sure there are num-threads invoices
                                       available at any given time.
      -p STRING, --pubkey=STRING       The Pubkey to use as the default pubkey for
                                       all Orb commands.
      -r INT, --rate-limit=INT         Wait rate-limit seconds between each call to
                                       the LNURL generation endpoint.
      -t INT, --total-amount-sat=INT   The sum of the amount of all paid invoices
                                       should add up to total-amount-sat.
      -u STRING, --url=STRING          The LNURL in the form LNURL....
      -w, --[no-]wait                  Wait for payments to complete (setting this
                                       to False is only used for testing purposes).
    
    

``orb rebalance.rebalance``
-----------

.. code:: bash

    Usage: main.py [--core-opts] rebalance.rebalance [--options] [other tasks here ...]
    
    Docstring:
      Rebalance the node
    
    Options:
      -a INT, --amount=INT
      -c STRING, --chan-id=STRING
      -f INT, --fee-rate=INT
      -l STRING, --last-hop-pubkey=STRING
      -m INT, --max-paths=INT
      -n STRING, --node=STRING
      -t INT, --time-pref=INT
    
    

``orb channel.open``
-----------

.. code:: bash

    Usage: main.py [--core-opts] channel.open [--options] [other tasks here ...]
    
    Docstring:
      Open a channel.
    
    Options:
      -a STRING, --amount-sats=STRING     The size of the channel in sats
      -p STRING, --peer-pubkey=STRING     The Pubkey of the peer you wish to open
                                          to
      -s STRING, --sat-per-vbyte=STRING   The fee to use in sats per vbytes
      -u STRING, --pubkey=STRING          The Pubkey to use as the default pubkey
                                          for all Orb commands.
    
    

``orb peer.connect``
-----------

.. code:: bash

    Usage: main.py [--core-opts] peer.connect [--options] [other tasks here ...]
    
    Docstring:
      Connect to a peer.
    
    Options:
      -p STRING, --peer-pubkey=STRING   The Pubkey of the peer you wish to open to
      -u STRING, --pubkey=STRING        The Pubkey to use as the default pubkey for
                                        all Orb commands.
    
    

``orb peer.list``
-----------

.. code:: bash

    Usage: main.py [--core-opts] peer.list [--options] [other tasks here ...]
    
    Docstring:
      List peers.
    
    Options:
      -p STRING, --pubkey=STRING   The Pubkey to use as the default pubkey for all
                                   Orb commands.
    
    

``orb test.run-all-tests``
-----------

.. code:: bash

    Usage: main.py [--core-opts] test.run-all-tests [other tasks here ...]
    
    Docstring:
      Run all tests.
    
    Options:
      none
    
    


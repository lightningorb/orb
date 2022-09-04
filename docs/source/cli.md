

**Usage**:

```console
$ orb [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `chain`: Commands relating to on-chain activities
* `channel`
* `invoice`
* `network`
* `node`: Commands to perform operations on nodes.
* `pay`
* `peer`
* `rebalance`
* `test`
* `web`

## `orb chain`

Commands relating to on-chain activities

**Usage**:

```console
$ orb chain [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `balance`: Get on-chain balance.
* `deposit`: Get an on-chain address to deposit BTC.
* `fees`: Get mempool chain fees.
* `send`: Send coins on-chain.

### `orb chain balance`

Get on-chain balance.

**Usage**:

```console
$ orb chain balance [OPTIONS] [PUBKEY]
```

**Arguments**:

* `[PUBKEY]`: The pubkey of the node. If not provided, use the default node.

**Options**:

* `--help`: Show this message and exit.

### `orb chain deposit`

Get an on-chain address to deposit BTC.

**Usage**:

```console
$ orb chain deposit [OPTIONS]
```

**Options**:

* `--pubkey TEXT`: [default: ]
* `--help`: Show this message and exit.

### `orb chain fees`

Get mempool chain fees. Currently these are the fees from
mempool.space

**Usage**:

```console
$ orb chain fees [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `orb chain send`

Send coins on-chain.

**Usage**:

```console
$ orb chain send [OPTIONS] ADDRESS SATOSHI SAT_PER_VBYTE [PUBKEY]
```

**Arguments**:

* `ADDRESS`: [required]
* `SATOSHI`: Amount to send, expressed in satoshis, or 'all'.  [required]
* `SAT_PER_VBYTE`: Sat per vbyte to use for the transaction.  [required]
* `[PUBKEY]`: The pubkey of the node. If not provided, use the default node.

**Options**:

* `--help`: Show this message and exit.

## `orb channel`

**Usage**:

```console
$ orb channel [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `list-forwards`: List forwards for the node.
* `open`: Open a channel.

### `orb channel list-forwards`

List forwards for the node.

**Usage**:

```console
$ orb channel list-forwards [OPTIONS] [PUBKEY]
```

**Arguments**:

* `[PUBKEY]`: The pubkey of the node. If not provided, use the default node.

**Options**:

* `--index-offset INTEGER`: Start index.  [default: 0]
* `--num-max-events INTEGER`: Max number of events to return.  [default: 100]
* `--help`: Show this message and exit.

### `orb channel open`

Open a channel.

**Usage**:

```console
$ orb channel open [OPTIONS] PEER_PUBKEY AMOUNT_SATS SAT_PER_VBYTE
```

**Arguments**:

* `PEER_PUBKEY`: [required]
* `AMOUNT_SATS`: [required]
* `SAT_PER_VBYTE`: [required]

**Options**:

* `--pubkey TEXT`: [default: ]
* `--help`: Show this message and exit.

## `orb invoice`

**Usage**:

```console
$ orb invoice [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `generate`: Generate a bolt11 invoice.

### `orb invoice generate`

Generate a bolt11 invoice.

**Usage**:

```console
$ orb invoice generate [OPTIONS] [SATOSHIS] [PUBKEY]
```

**Arguments**:

* `[SATOSHIS]`: The amount of Satoshis for this invoice.  [default: 1000]
* `[PUBKEY]`: The pubkey of the node. If not provided, use the default node.

**Options**:

* `--help`: Show this message and exit.

## `orb network`

**Usage**:

```console
$ orb network [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `get-route`: This is a hard command to get right so that...

### `orb network get-route`

This is a hard command to get right so that it looks and behaves similarly in CLN and LND, and messing up a route could be a bad idea, for this reason the returned object contains the *original*, as it was returned by lnd / cln.

Sample result for LND
---------------------

.. code:: json

    {
        "hops": [
            {
                "amp_record": null,
                "amt_to_forward": 1000,
                "amt_to_forward_msat": 1000000,
                "chan_capacity": 100000000,
                "chan_id": 68345642782621696,
                "custom_records": {},
                "expiry": 63990,
                "fee": 0,
                "fee_msat": 0,
                "metadata": "",
                "mpp_record": null,
                "pub_key": "031ce6d59ad4fe4158949dcd87ea49158dc6923f4457ec69bae9b0b04c13973213",
                "tlv_payload": true
            }
        ],
        "original": {
            "hops": [
                {
                    "amp_record": null,
                    "amt_to_forward": 1000,
                    "amt_to_forward_msat": 1000000,
                    "chan_capacity": 100000000,
                    "chan_id": 68345642782621696,
                    "custom_records": {},
                    "expiry": 63990,
                    "fee": 0,
                    "fee_msat": 0,
                    "metadata": "",
                    "mpp_record": null,
                    "pub_key": "031ce6d59ad4fe4158949dcd87ea49158dc6923f4457ec69bae9b0b04c13973213",
                    "tlv_payload": true
                }
            ],
            "total_amt": 1000,
            "total_amt_msat": 1000000,
            "total_fees": 0,
            "total_fees_msat": 0,
            "total_time_lock": 63990
        },
        "total_amt": 1000,
        "total_amt_msat": 1000000,
        "total_fees": 0,
        "total_fees_msat": 0
    }


Sample result for CLN
---------------------

.. code:: json

    {
        "hops": [
            {
                "amp_record": null,
                "amt_to_forward": 1000,
                "amt_to_forward_msat": 1000000,
                "chan_capacity": 0,
                "chan_id": "162x1x1",
                "custom_records": {},
                "direction": 0,
                "expiry": 0,
                "fee": 0.0,
                "fee_msat": 0,
                "metadata": "",
                "mpp_record": null,
                "pub_key": "0280dc76984a81124699b2a8b96b3167443b9dfad03c3c98c85bb2d020e6924283",
                "tlv_payload": true
            }
        ],
        "original": {
            "api_version": "0.8.0",
            "route": [
                {
                    "amount_msat": "1000000msat",
                    "channel": "162x1x1",
                    "delay": 0,
                    "direction": 0,
                    "id": "0280dc76984a81124699b2a8b96b3167443b9dfad03c3c98c85bb2d020e6924283",
                    "msatoshi": 1000000,
                    "style": "tlv"
                }
            ]
        },
        "total_amt": 1000,
        "total_amt_msat": 1000000,
        "total_fees": 0,
        "total_fees_msat": 0
    }

--cltv
~~~~~~

The CLTV flag is required by CLN, but not LND.

--time-pref
~~~~~~~~~~~

This is also an awkward flag, as LND >= 0.15 can take a time-preference flag ranging from -1 and 1, however this flag is meaningless to CLN. So we keep the flag exposed, even though it does nothing with CLN.

**Usage**:

```console
$ orb network get-route [OPTIONS] DESTINATION
```

**Arguments**:

* `DESTINATION`: the pub_key of the node to which to find a route.  [required]

**Options**:

* `--fee-limit-msat TEXT`: the fee limit in millisatoshis.  [default: 500]
* `--source-pub-key TEXT`: the pub_key of the node from which to find a route.
* `--outgoing-chan-id TEXT`: the channel id the first hop o the route.
* `--ignored-nodes TEXT`: list of nodes to ignore.  [default: ]
* `--ignored-pairs TEXT`: list of pairs to ignore (LND only).  [default: ]
* `--last-hop-pubkey TEXT`: the last node before pub_key (LND only).  [default: ]
* `--satoshis INTEGER`: the amount in satoshis the route should accomodate.  [default: 1000]
* `--time-pref TEXT`: the time preference of the route, from 0 to 1. (LND only).  [default: 0]
* `--cltv TEXT`: absolute lock time. (CLN only).  [default: 0]
* `--pubkey TEXT`: The pubkey of the node. If not provided, use the default node.
* `--help`: Show this message and exit.

## `orb node`

Commands to perform operations on nodes.

**Usage**:

```console
$ orb node [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create node.
* `create-from-cert-files`: Create node and use certificate files.
* `create-orb-public`: Create public testnet node.
* `delete`: Delete node information.
* `info`: Get node information.
* `list`: Get a list of nodes known to Orb.
* `ssh-wizard`: SSH into the node, copy the cert and mac, and...
* `use`: Use the given node as default.

### `orb node create`

Create node.

This command is used by other commands, e.g:

:ref:`orb-node-create-orb-public`
:ref:`orb-node-create-from-cert-files`

**Usage**:

```console
$ orb node create [OPTIONS]
```

**Options**:

* `--hostname TEXT`: IP address or DNS-resolvable name for this host.  [required]
* `--mac-hex TEXT`: The node macaroon in hex format.  [required]
* `--node-type TEXT`: cln or lnd.  [required]
* `--protocol TEXT`: rest or grpc.  [required]
* `--network TEXT`: IP address or DNS-resovable name for this host.  [required]
* `--cert-plain TEXT`: Plain node certificate.  [required]
* `--rest-port INTEGER`: REST port.  [default: 8080]
* `--grpc-port INTEGER`: GRPC port.  [default: 10009]
* `--use-node / --no-use-node`: Whether to set as default.  [default: True]
* `--help`: Show this message and exit.

### `orb node create-from-cert-files`

Create node and use certificate files.

**Usage**:

```console
$ orb node create-from-cert-files [OPTIONS]
```

**Options**:

* `--hostname TEXT`: IP address or DNS-resolvable name for this host.  [required]
* `--mac-file-path TEXT`: Path to the node macaroon.  [required]
* `--node-type TEXT`: cln or lnd.  [required]
* `--protocol TEXT`: rest or grpc.  [required]
* `--network TEXT`: IP address or DNS-resovable name for this host.  [required]
* `--cert-file-path TEXT`: Path to the node certificate.  [required]
* `--rest-port INTEGER`: REST port.  [default: 8080]
* `--grpc-port INTEGER`: GRPC port.  [default: 10009]
* `--use-node / --no-use-node`: Whether to set as default.  [default: True]
* `--help`: Show this message and exit.

### `orb node create-orb-public`

Create public testnet node.

**Usage**:

```console
$ orb node create-orb-public [OPTIONS] NODE_TYPE PROTOCOL
```

**Arguments**:

* `NODE_TYPE`: lnd or cln.  [required]
* `PROTOCOL`: rest or grpc.  [required]

**Options**:

* `--use-node / --no-use-node`: Set this node as the default.  [default: True]
* `--help`: Show this message and exit.

### `orb node delete`

Delete node information.

**Usage**:

```console
$ orb node delete [OPTIONS] [PUBKEY]
```

**Arguments**:

* `[PUBKEY]`: The pubkey of the node. If not provided, use the default node.

**Options**:

* `--help`: Show this message and exit.

### `orb node info`

Get node information.

**Usage**:

```console
$ orb node info [OPTIONS] [PUBKEY]
```

**Arguments**:

* `[PUBKEY]`: The pubkey of the node. If not provided, use the default node.

**Options**:

* `--help`: Show this message and exit.

### `orb node list`

Get a list of nodes known to Orb.

**Usage**:

```console
$ orb node list [OPTIONS]
```

**Options**:

* `--show-info / --no-show-info`: If True, then connect and print node information  [default: False]
* `--help`: Show this message and exit.

### `orb node ssh-wizard`

SSH into the node, copy the cert and mac, and create the node.

**Usage**:

```console
$ orb node ssh-wizard [OPTIONS]
```

**Options**:

* `--hostname TEXT`: IP address or DNS-resolvable name for this host.  [required]
* `--node-type TEXT`: cln or lnd.  [required]
* `--ssh-cert-path PATH`: Certificate to use for the SSH session.
* `--ssh-password TEXT`: Password to use for the SSH session.
* `--ln-cert-path PATH`: Path of the node certificate on the target host.
* `--ln-macaroon-path PATH`: Path of the node macaroon on the target host.
* `--network TEXT`: IP address or DNS-resovable name for this host.  [required]
* `--protocol TEXT`: rest or grpc.  [required]
* `--rest-port INTEGER`: REST port.  [default: 8080]
* `--grpc-port INTEGER`: GRPC port.  [default: 10009]
* `--ssh-user TEXT`: Username for SSH session.  [default: ubuntu]
* `--ssh-port INTEGER`: Port for SSH session.  [default: 22]
* `--use-node / --no-use-node`: Whether to set as default.  [default: True]
* `--help`: Show this message and exit.

### `orb node use`

Use the given node as default.

**Usage**:

```console
$ orb node use [OPTIONS] [PUBKEY]
```

**Arguments**:

* `[PUBKEY]`: The pubkey of the node.

**Options**:

* `--help`: Show this message and exit.

## `orb pay`

**Usage**:

```console
$ orb pay [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `invoices`: Pay Ingested Invoices
* `lnurl`: Generate bolt11 invoices from LNURL, and pay...

### `orb pay invoices`

Pay Ingested Invoices

**Usage**:

```console
$ orb pay invoices [OPTIONS]
```

**Options**:

* `--chan-id TEXT`
* `--max-paths INTEGER`: [default: 10000]
* `--fee-rate INTEGER`: [default: 500]
* `--time-pref FLOAT`: [default: 0]
* `--num-threads INTEGER`: [default: 5]
* `--pubkey TEXT`: [default: ]
* `--help`: Show this message and exit.

### `orb pay lnurl`

Generate bolt11 invoices from LNURL, and pay them.

**Usage**:

```console
$ orb pay lnurl [OPTIONS] URL
```

**Arguments**:

* `URL`: [required]

**Options**:

* `--total-amount-sat INTEGER`: [default: 100000000]
* `--chunks INTEGER`: [default: 100]
* `--num-threads INTEGER`: [default: 5]
* `--rate-limit INTEGER`: [default: 5]
* `--pubkey TEXT`: [default: ]
* `--wait / --no-wait`: [default: True]
* `--chan-id TEXT`
* `--max-paths INTEGER`: [default: 10000]
* `--fee-rate INTEGER`: [default: 500]
* `--time-pref FLOAT`: [default: 0]
* `--help`: Show this message and exit.

## `orb peer`

**Usage**:

```console
$ orb peer [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `connect`: Connect to a peer.
* `list`: List peers.

### `orb peer connect`

Connect to a peer.

**Usage**:

```console
$ orb peer connect [OPTIONS] PEER_PUBKEY
```

**Arguments**:

* `PEER_PUBKEY`: [required]

**Options**:

* `--pubkey TEXT`: [default: ]
* `--help`: Show this message and exit.

### `orb peer list`

List peers.

**Usage**:

```console
$ orb peer list [OPTIONS]
```

**Options**:

* `--pubkey TEXT`: [default: ]
* `--help`: Show this message and exit.

## `orb rebalance`

**Usage**:

```console
$ orb rebalance [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `rebalance`: Rebalance the node

### `orb rebalance rebalance`

Rebalance the node

**Usage**:

```console
$ orb rebalance rebalance [OPTIONS]
```

**Options**:

* `--amount INTEGER`: [default: 1000]
* `--chan-id TEXT`
* `--last-hop-pubkey TEXT`
* `--max-paths INTEGER`: [default: 10000]
* `--fee-rate INTEGER`: [default: 500]
* `--time-pref FLOAT`: [default: 0]
* `--node TEXT`: [default: 02613d48576b651b45587802f86e414c662f31d9e24a9c18158724aa2d7851e764]
* `--help`: Show this message and exit.

## `orb test`

**Usage**:

```console
$ orb test [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `run-all-tests`: Run all tests.

### `orb test run-all-tests`

Run all tests.

**Usage**:

```console
$ orb test run-all-tests [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `orb web`

**Usage**:

```console
$ orb web [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `serve`: Serve the Orb web app.

### `orb web serve`

Serve the Orb web app.

**Usage**:

```console
$ orb web serve [OPTIONS]
```

**Options**:

* `--host TEXT`: The allowed host.  [default: 0.0.0.0]
* `--port INTEGER`: The port to serve.  [default: 8080]
* `--reload / --no-reload`: Live reloading (dev).  [default: False]
* `--debug / --no-debug`: Show debug info (dev).  [default: False]
* `--workers INTEGER`: Number of web workers.  [default: 1]
* `--help`: Show this message and exit.


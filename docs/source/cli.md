# `orb`

**Usage**:

```console
$ orb [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `chain`
* `channel`
* `invoice`
* `node`: Commands to perform operations on nodes.
* `pay`
* `peer`
* `rebalance`
* `test`

## `orb chain`

**Usage**:

```console
$ orb chain [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `deposit`: Get an on-chain address to deposit BTC.
* `fees`: Get mempool chain fees.
* `send`: Send coins on-chain.

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
$ orb chain send [OPTIONS] ADDRESS AMOUNT SAT_PER_VBYTE
```

**Arguments**:

* `ADDRESS`: [required]
* `AMOUNT`: [required]
* `SAT_PER_VBYTE`: [required]

**Options**:

* `--pubkey TEXT`: [default: ]
* `--help`: Show this message and exit.

## `orb channel`

**Usage**:

```console
$ orb channel [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `open`: Open a channel.

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

## `orb node`

Commands to perform operations on nodes.

**Usage**:

```console
$ orb node [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `balance`: Get total balance, for both on-chain and...
* `create`: Create node.
* `create-from-cert-files`: Create node and use certificate files.
* `create-orb-public`: Create public testnet node.
* `delete`: Delete node information.
* `info`: Get node information.
* `list`: Get a list of nodes known to Orb.
* `ssh-wizard`: SSH into the node, copy the cert and mac, and...
* `use`: Use the given node as default.

### `orb node balance`

Get total balance, for both on-chain and balance in channels.

WIP: this is not yet implemented for CLN.

**Usage**:

```console
$ orb node balance [OPTIONS] [PUBKEY]
```

**Arguments**:

* `[PUBKEY]`: The pubkey of the node. If not provided, use the default node.

**Options**:

* `--help`: Show this message and exit.

### `orb node create`

Create node.

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
* `--node TEXT`: [default: 02234cf94dd9a4b76cb4767bf3da03b046c299307063b17c9c2e1886829df6a23a]
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
* `--pubkey TEXT`: [default: 02234cf94dd9a4b76cb4767bf3da03b046c299307063b17c9c2e1886829df6a23a]
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
$ orb rebalance rebalance [OPTIONS] C
```

**Arguments**:

* `C`: [required]

**Options**:

* `--amount INTEGER`: [default: 1000]
* `--chan-id TEXT`
* `--last-hop-pubkey TEXT`
* `--max-paths INTEGER`: [default: 10000]
* `--fee-rate INTEGER`: [default: 500]
* `--time-pref FLOAT`: [default: 0]
* `--node TEXT`: [default: 02234cf94dd9a4b76cb4767bf3da03b046c299307063b17c9c2e1886829df6a23a]
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


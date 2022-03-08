# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 13:23:54
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-16 06:48:33
#!/usr/bin/env python3

from invoke import task, Context, Collection
from fabric import Connection

from commands.monkeypatch import fix_annotations

fix_annotations()

from commands import aws
from commands import btc
from commands import ssh
from commands import lnd
from commands import bos
from commands import prefs
from commands import system
from commands import tor
from commands import wallet
from commands import docs
from commands import utils
from commands import ui
from commands import lit
from commands import bot

# from commands import orb


@task(
    help=dict(
        instance_type="EC2 instance type, recommended: t3.medium",
        availability_zone="Exact zone, e.g if you're using us-east-1 as your default zone, this has to be e.g us-east-1a",
        name="EC2 instances have names, a good name would be mainnet",
        mainnet="Whether to use mainnet or testnet",
    )
)
def create_aws_node(
    c, instance_type, availability_zone, name, keypair_name, disk_size, mainnet=True
):
    """
    Creates an AWS lightning node, from start to finish (excluding the security group).

    This includes:

    - updating package information
    - creating the volume to hold the blockchain data
    - attaching the volume
    - formatting & mounting the volume
    - installing tor
    - building bitcoind from source
    - configuring bitcoind
    - installing go
    - building and install lnd
    - configuring lnd
    - installing balance of satoshis
    - install mosh
    - creating the wallet, and downloading the mnemonic and entropy to a password protected zipfile
    - saving the newly created node as the default (preferred node)
    """
    ip = aws.create(
        c,
        instance_type=instance_type,
        availability_zone=availability_zone,
        keypair_name=keypair_name,
        name=name,
    )
    with Connection(
        ip,
        **dict(connect_kwargs={"key_filename": prefs.get_key_path(name)}, user="ubuntu")
    ) as con:
        aws.create_blockchain_disk(
            con, availability_zone=availability_zone, name=name, disk_size=disk_size
        )
        aws.attach_blockchain_disk(con, disk_name=name, node_name=name)
        aws.config_blockchain_disk(con, format=True, disk_size=disk_size)
        setup_node(con, name, mainnet)


@task
def setup_node(c, name, mainnet=True):
    """
    Setup a lightning node on the given host, from scratch. It assumes
    a large enough disk is mounted on /blockchain. This includes:

    - allowing up to 512000 open files
    - configuring ufw and iptables against flooding
    - installing tor
    - building bitcoind from source
    - configuring bitcoind
    - installing go
    - building and install lnd
    - configuring lnd
    - installing balance of satoshis
    - install mosh
    - creating the wallet, and downloading the mnemonic and entropy to a password protected zipfile
    - saving the newly created node as the default (preferred node)
    """
    system.setup(c, upgrade=False, mainnet=mainnet)
    system.fd(c)
    system.ufw(c)
    system.flood_protection(c)
    tor.setup(c)
    btc.build(c)
    btc.setup(c, mainnet=mainnet)
    lnd.install_go(c)
    lnd.install(c)
    lnd.setup(c)
    lnd.start(c)
    bos.install(c)
    ssh.install_mosh(c)
    wallet.create(c, node_name=name)
    prefs.save(c, name=name)


@task
def reset(c):
    """
    Perform a full reset and uninstall (experimental).
    """
    btc.stop(c)
    btc.reset(c)
    lnd.stop(c)
    lnd.reset(c)
    tor.uninstall(c)


@task
def reset_wallet(c, name):
    """
    Performs a start to finish reset of the wallet, this includes:

    - shutting down bitcoind softly
    - shutting down lnd
    - deleting the ~/.lnd folder
    - re-running the lnd setup task
    - re-creating the wallet using the password protected secrets.zip file

    This command is mostly useful for getting a clean lnd slate while maintaining wallet information
    """
    btc.stop(c)
    lnd.stop(c)
    lnd.reset(c)
    lnd.setup(c)
    btc.start(c)
    btc.start(c)
    wallet.create(c, node_name=name)


@task
def soft_reboot(c):
    """
    Softly shut down bitcoind, and lnd, then reboot the system.
    """
    btc.stop(c)
    lnd.stop(c)
    system.reboot(c)


@task
def soft_shutdown(c):
    """
    Softly shut down bitcoind, and lnd.
    """
    btc.stop(c)
    lnd.stop(c)


@task
def generate_docs(c):
    """
    Generate this task documentation
    """
    docs.generate(c, namespace)


namespace = Collection(
    aws,
    btc,
    ssh,
    lnd,
    bos,
    tor,
    prefs,
    system,
    docs,
    generate_docs,
    reset_wallet,
    create_aws_node,
    setup_node,
    utils,
    reset,
    ui,
    soft_reboot,
    lit,
    soft_shutdown,
    bot,
)

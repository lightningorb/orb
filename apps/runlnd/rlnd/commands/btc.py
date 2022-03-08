import json
import arrow
from time import time, sleep
import os

from invoke import task
from textwrap import dedent
from fabric.transfer import Transfer
from .utils import get_conf_file_path


@task
def build(c):
    """
    Build bitcoind from source.
    Create the required /blockchain bitcoin (sub)directories.
    """
    c.sudo("apt-get update -y")
    c.sudo(
        "apt install -y git build-essential libtool autotools-dev automake pkg-config libssl-dev libevent-dev bsdmainutils libboost-system-dev libboost-filesystem-dev libboost-chrono-dev libboost-program-options-dev libboost-test-dev libboost-thread-dev libminiupnpc-dev libzmq3-dev"
    )
    if c.run("test -f bitcoin/", warn=True).ok:
        c.run("rm -rf bitcoin")

    c.run("git clone -b v0.21.0 https://github.com/bitcoin/bitcoin.git")
    with c.cd("bitcoin/"):
        c.run("./autogen.sh ")
        c.run(
            "./configure CXXFLAGS='--param ggc-min-expand=1 --param ggc-min-heapsize=32768' --enable-cxx --with-zmq --without-gui --disable-shared --with-pic --disable-tests --disable-bench --enable-upnp-default --disable-wallet"
        )
        c.run("make -j `nproc`")
    # fabric2 bug, context cd doesn't work with sudo
    c.run("cd bitcoin/ && sudo make install")
    c.run("rm -rf bitcoin")

    if c.run("test -d /blockchain", warn=True).ok:
        c.run("mkdir -p /blockchain/.bitcoin")
        c.run("mkdir -p /blockchain/.bitcoin/data")
    c.run("mkdir -p ~/.bitcoin")


@task
def reset(c, use_tor=True):
    c.run("rm -rf .bitcoin bitcoin")


@task(
    help=dict(
        use_tor="Connect with peers via the tor network",
        mainnet="If true use mainnet, else use testnet",
    )
)
def setup(c, use_tor=True, mainnet=True):
    """
    Set up bitcoin.

    This includes:

    - generating the rpcauth passwords
    - configuring ~/.bitcoin/bitcoin.conf
    - starting bitcoind
    - configuring bitcoind to start on reboot
    - setting up log rotation
    - creating log symbolic links
    - setting proper permissions on the /blockchain mount
    """
    if c.run("test -f rpcauth.py", warn=True).failed:
        c.run(
            "wget https://raw.githubusercontent.com/bitcoin/bitcoin/master/share/rpcauth/rpcauth.py"
        )
    res = c.run("python3 ./rpcauth.py bitcoinrpc").stdout.split("\n")
    c.run("rm ./rpcauth.py")
    lnd_rpc_pass = res[3].strip().replace(r"\r", "")
    btc_rpc_pass = res[1].strip().replace(r"\r", "")
    c.run(f"echo '{lnd_rpc_pass}' > lnd_password")
    conf = (
        open(get_conf_file_path("bitcoin.conf.main"))
        .read()
        .replace("{btc_rpc_pass}", btc_rpc_pass)
        .replace("{testnet}", "10"[mainnet])
    )
    if use_tor:
        bitcoin_tor_conf = open(get_conf_file_path("bitcoin.conf.tor")).read()
        bitcoin_conf = f"{conf}\n{bitcoin_tor_conf}"
    else:
        bitcoin_conf = conf

    with open("bitcoin.conf", "w") as f:
        f.write(bitcoin_conf)
    c.put("bitcoin.conf", "/home/ubuntu/.bitcoin/bitcoin.conf")
    os.unlink("bitcoin.conf")
    c.sudo("mkdir -p /blockchain/.bitcoin/data")
    c.sudo("chown ubuntu -R /blockchain")
    c.run("bitcoind")
    c.run(
        '(crontab -l 2>/dev/null; echo "@reboot /usr/local/bin/bitcoind") | crontab -'
    )
    if mainnet:
        c.run("ln -sf /blockchain/.bitcoin/data/debug.log ~/bitcoind-mainnet.log")
    else:
        c.run(
            "ln -sf /blockchain/.bitcoin/data/testnet3/debug.log ~/bitcoind-testnet.log"
        )

    c.put(
        get_conf_file_path(f"logrotate.{('test','main')[mainnet]}net"),
        "/tmp/bitcoin-debug",
    )
    c.sudo("chown root /tmp/bitcoin-debug")
    c.sudo("mv /tmp/bitcoin-debug /etc/logrotate.d/bitcoin-debug")
    c.sudo("logrotate /etc/logrotate.d/bitcoin-debug")


@task
def stop(c):
    """
    Stop bitcoind softly. This task will not return until bitcoind
    has written all its data to disk. This is to prevent having to
    re-scan the entire blockchain in case the command is followed by
    a reboot.
    """
    c.run("bitcoin-cli stop", warn=True)
    while (
        "Shutdown: done" not in c.run("tail /blockchain/.bitcoin/data/debug.log").stdout
    ):
        print("bitcoin is still shutting down")
        sleep(5)


@task
def start(c):
    """
    Start bitcoind. Block, and keep scanning the logs until bitcoind
    has indeed started successfully.
    """
    c.run("bitcoind")
    sleep(10)
    while (
        "Loading block index"
        in c.run("tail /blockchain/.bitcoin/data/debug.log").stdout
    ):
        print("Loading block index")
        sleep(5)
    while (
        "Verifying blocks" in c.run("tail /blockchain/.bitcoin/data/debug.log").stdout
    ):
        print("verifying blocks")
        sleep(5)


@task
def show_sync_progress(c):
    """
    Attempts to provide an estimated date in time for when the blockchain
    is synced (in local time). Probably highly inacurate.
    """
    length = 1000000
    deltas = []
    get_progress = lambda: int(
        json.loads(c.run(f"bitcoin-cli -getinfo", hide=True).stdout)[
            "verificationprogress"
        ]
        * length
    )
    last_p = get_progress()
    last_t = time()
    while last_p < length:
        p = get_progress()
        if last_p != p:
            deltas.append(((time() - last_t) / (p - last_p)))
            last_t = time()
            then = (
                arrow.now()
                .shift(seconds=((sum(deltas) / len(deltas))) * (length - p))
                .format("YYYY-MM-DD HH:mm")
            )
            print(f"finish date: {then}")
        else:
            print(f"syncing blockchain")
        sleep(10)
        last_p = p


@task
def logs(c):
    """
    Tail bitcion's logs until cancelled.
    """
    c.run("tail -f /home/ubuntu/bitcoind-mainnet.log")

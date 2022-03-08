# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-11-16 13:56:59
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-16 09:07:46
import os
import arrow
import json
from invoke import task
from textwrap import dedent
from .utils import get_conf_file_path
from .prefs import config_node_dir


@task
def install_go(c):
    """
    Install Go 1.16.5.
    """
    if c.run("test -d /usr/local/go", warn=True).failed:
        c.run("wget https://golang.org/dl/go1.16.5.linux-amd64.tar.gz")
        c.run("tar -xvf go1.16.5.linux-amd64.tar.gz")
        c.sudo("mv go /usr/local")
        c.run("rm go1.16.5.linux-amd64.tar.gz")
    c.run("mkdir -p ~/go")
    c.sudo("ln /usr/local/go/bin/go /usr/bin/go -sf")


@task
def logs(c):
    """
    Tail lnd logs until cancelled.
    """
    c.run("tail -f /home/ubuntu/.lnd/logs/bitcoin/mainnet/lnd.log")


@task
def install(c, version: str = "v0.14.1-beta"):
    """
    Install lnd, and configure it with systemd.
    """
    c.sudo("apt-get install -y build-essential")
    c.sudo("rm -rf lnd")
    c.run("git clone https://github.com/lightningnetwork/lnd.git")
    with c.cd("lnd"):
        c.run(f"git checkout {version}")
        c.run(
            'make install tags="autopilotrpc chainrpc invoicesrpc routerrpc signrpc'
            ' walletrpc watchtowerrpc wtclientrpc"'
        )
    c.run("mkdir -p ~/.lnd")
    if c.run("test -d /etc/systemd/system/lnd.service", warn=True).failed:
        c.put(get_conf_file_path("lnd.service"), "/tmp/lnd.service")
        c.sudo("mv /tmp/lnd.service /etc/systemd/system/lnd.service")
    c.sudo("systemctl enable lnd")
    c.run("ln -sf .lnd/logs/bitcoin/mainnet/lnd.log lnd.log")
    c.sudo("rm -rf lnd")


@task
def reset(c):
    """
    Reset lnd configuration, and re-create .lnd folder.
    """
    c.run("rm -rf ~/.lnd")
    c.run("mkdir ~/.lnd")


@task
def setup(c):
    """
    Set up lnd with lnd.conf, and bitcoind's rpc password.
    """
    lnd_pass = c.run("cat ~/lnd_password").stdout.strip()
    conf = open(get_conf_file_path("lnd.conf")).read().replace("{lnd_pass}", lnd_pass)
    with open("lnd.conf", "w") as f:
        f.write(conf)
    c.put("lnd.conf", "/home/ubuntu/.lnd/lnd.conf")
    os.unlink("lnd.conf")
    c.run("rm lnd_password")


@task
def start(c):
    """
    Start lnd.
    """
    c.sudo("systemctl start lnd")


@task
def stop(c):
    """
    Stop lnd.
    """
    c.sudo("systemctl stop lnd")


@task
def restart(c):
    """
    Restart lnd.
    """
    c.sudo("systemctl start lnd")


@task
def journal(c):
    """
    Display systemctl's journals for lnd.
    """
    c.run("journalctl -fu lnd")


@task
def backup_channels(c, node_name):
    """
    Create a backup file of the open channels, and download it to ~/.rln
    """
    a = arrow.now()
    backup_name = f"channels.{a.format('YYYY-MM-DD.HH:mm:ss')}.backup"
    backup_path = "/home/ubuntu/channel_backups/%s" % (backup_name)
    c.run("mkdir -p ~/channel_backups")
    c.run(f"lncli exportchanbackup --all --output_file={backup_path}")
    c.get(backup_path, os.path.join(config_node_dir(node_name), backup_name))


@task
def get_graph(c):
    """
    Run a describe graph and download as ./graph.json
    """
    print("describing graph")
    c.run("lncli describegraph > /tmp/graph.json")
    print("downloading graph")
    c.get("/tmp/graph.json", "graph.json")

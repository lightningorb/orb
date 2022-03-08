import json
import os
import arrow
from time import time

from invoke import task
from textwrap import dedent
from .utils import get_conf_file_path


@task(
    help={
        "upgrade": "Whether to upgrade all the packages to their latest version. This can be time-consuming.",
        "mainnet": "If False, then an alias for lncli --testnet is created.",
    }
)
def setup(c, upgrade=True, mainnet=True):
    """
    Basic host setup, i.e updating packages, install vim and nmon (for system monitoring),
    setup PATHS and aliases properly at the top of .bashrc for non-login shells
    """
    c.sudo("apt update")
    c.sudo("apt install -y vim nmon jq")
    if upgrade:
        c.sudo("apt upgrade -y")
    if c.run("test -d .run-lnd-env.sh", warn=True, hide=True).failed:
        src_conf = (".rln-env-testnet.sh", ".run-lnd-env.sh")[mainnet]
        c.put(get_conf_file_path(src_conf), ".run-lnd-env.sh")
    if ".run-lnd-env.sh" not in c.run("cat ~/.bashrc", hide=True).stdout:
        c.run("""sed -i '1isource ~/.run-lnd-env.sh\n' ~/.bashrc""", hide=True)
    c.run("touch ~/.hushlogin")


@task
def fd(c):
    """
    Up the maximum number of files open simultaniously to
    half a million (512000). Does not require a system reboot.
    """
    if "512000" not in c.sudo("sysctl fs.file-max").stdout:
        c.sudo("echo 'fs.file-max=512000' | sudo tee -a /etc/sysctl.conf")
    c.sudo("sysctl -p")
    assert "512000" in c.sudo("sysctl fs.file-max").stdout
    print("max files opened are 512000")


@task
def ufw(c):
    """
    Block all ports, apart from OpenSSH, 10009 (standard GRPC) and 9735 (standard P2P) and
    9911 (watchtower).
    """
    c.sudo("apt-get install ufw -y", warn=True)
    c.sudo("ufw allow OpenSSH", warn=True)
    c.sudo("ufw allow 10009", warn=True)
    c.sudo("ufw allow 9911", warn=True)
    c.sudo("ufw allow 9735", warn=True)
    c.sudo("ufw logging on", warn=True)
    c.sudo("ufw --force enable", warn=True)
    c.sudo("ufw status", warn=True)


@task
def flood_protection(c):
    """
    Protect the network interface from being flooded with packets.
    """
    c.sudo("iptables -N syn_flood", warn=True)
    c.sudo("iptables -A INPUT -p tcp --syn -j syn_flood", warn=True)
    c.sudo(
        "iptables -A syn_flood -m limit --limit 1/s --limit-burst 3 -j RETURN",
        warn=True,
    )
    c.sudo("iptables -A syn_flood -j DROP", warn=True)
    c.sudo(
        "iptables -A INPUT -p icmp -m limit --limit 1/s --limit-burst 1 -j ACCEPT",
        warn=True,
    )
    c.sudo(
        "iptables -A INPUT -p icmp -m limit --limit 1/s --limit-burst 1 -j LOG --log-prefix PING-DROP:",
        warn=True,
    )
    c.sudo("iptables -A INPUT -p icmp -j DROP", warn=True)
    c.sudo("iptables -A OUTPUT -p icmp -j ACCEPT", warn=True)


@task
def shutdown(c):
    """
    Shut the system down. Make sure you first stop bitcoind, as it needs
    to write its dbcache to disk first.
    """
    c.sudo("shutdown")


@task
def reboot(c):
    """
    Reboot the system. Make sure you first stop bitcoind, as it needs
    to write its dbcache to disk first.
    """
    c.sudo("reboot")

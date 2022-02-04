# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-02-05 05:46:07
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-05 07:00:32

"""
Everything related to recieving and processing licence payments on
the LND node.

./build.py katching.deploy-katching

"""

import os
from fabric import Connection
from invoke import task


@task
def deploy_katching_service(c):
    """
    The Katching Service scans for SETTLED invoices on the
    LND node, and dispatches them as jobs on RabbitMQ.
    """
    with c.cd("orb"):
        c.run("git stash")
        c.run("git pull")
        c.put("build_system/katching.conf", "/tmp/")
    c.sudo("mv /tmp/katching.conf /etc/supervisor/conf.d/")
    c.sudo("supervisorctl update")


@task
def deploy_lnd_invoice_service(c):
    """
    The LND Invoice Service runs on the node, and generates
    invoices by handling messages dispatched via RabbitMQ.
    """
    with c.cd("orb"):
        c.run("git stash")
        c.run("git pull")
        c.put("build_system/katching.conf", "/tmp/")
    c.sudo("mv /tmp/katching.conf /etc/supervisor/conf.d/")
    c.sudo("supervisorctl update")


@task
def deploy_katching(c, env=os.environ):
    """
    'Katching' is a python program that runs on the LND node
    and sends messages to the Katching Service when SETTLED
    invoices are detected.
    """
    with Connection(
        env["LND_NODE_IP"],
        connect_kwargs={"key_filename": env["LND_NODE_SSH_CERT"]},
        user="ubuntu",
    ) as con:
        with con.cd("orb"):
            con.run("git stash")
            con.run("git pull")
            con.put("build_system/katching.conf", "/tmp/")
        con.sudo("mv /tmp/katching.conf /etc/supervisor/conf.d/")
        con.sudo("supervisorctl update")

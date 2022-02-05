# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-02-05 05:46:07
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-05 08:11:00

"""
Everything related to recieving and processing licence payments on
the LND node.

./build.py katching.deploy-katching
./build.py katching.deploy-katching-service
./build.py katching.deploy-lnd-invoice-service

"""

import os
from fabric import Connection
from invoke import task


@task
def deploy_lnd_invoice_service(c, env=os.environ):
    """
    The LND Invoice Service runs on the node, and generates
    invoices by handling messages dispatched via RabbitMQ.
    """
    with Connection(
        env["LND_NODE_IP"],
        connect_kwargs={"key_filename": env["LND_NODE_SSH_CERT"]},
        user="ubuntu",
    ) as con:
        with con.cd("orb"):
            con.run("git stash")
            con.run("git pull")
            con.put("build_system/lnd_invoice_service.conf", "/tmp/")
        con.sudo("mv /tmp/lnd_invoice_service.conf /etc/supervisor/conf.d/")
        con.sudo("supervisorctl update")


@task
def deploy_katching_service(c, env=os.environ):
    """
    The Katching Service gets settled invoices from RabbitMQ
    and updates the database.
    """
    with Connection(
        env["SERVER_HOSTNAME"],
        connect_kwargs={"key_filename": env["SERVER_SSH_CERT"]},
        user="ubuntu",
    ) as con:
        with con.cd("orb"):
            con.run("git stash")
            con.run("git pull")
            con.put("build_system/katching_service.conf", "/tmp/")
        con.sudo("mv /tmp/katching_service.conf /etc/supervisor/conf.d/")
        con.sudo("supervisorctl update")


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
        con.sudo("supervisorctl restart")

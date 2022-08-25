# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-21 12:39:49
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-22 12:05:51

from unittest import TestCase
from fabric import Connection
from invoke.context import Context

from build_system.monkey_patch import fix_annotations
from orb.ln import factory

fix_annotations()
from orb.cli import node


class TestSSHWizard(TestCase):
    def test_cli_cln_ssh_wizard(self):
        self.c = Context(Connection("localhost").config)
        node.ssh_wizard(
            self.c,
            hostname="regtest.cln.lnorb.com",
            node_type="cln",
            ssh_cert_path="lnorb_com.cer",
            rest_port="3001",
            protocol="rest",
            ln_cert_path="/home/ubuntu/dev/regtest-workbench/certificate.pem",
            ln_macaroon_path="/home/ubuntu/dev/regtest-workbench/access.macaroon",
        )
        pk = "02d74e4ffe22c95d78bea7d629907a631e0b0231376c7c674377bf4efaa1e2290e"
        ln = factory(pk)
        info = ln.get_info()
        self.assertTrue(info.alias == "regtest.cln.lnorb.com")
        node.delete(self.c, pubkey=pk)

    def test_cli_lnd_rest_ssh_wizard(self):
        self.c = Context(Connection("localhost").config)
        node.ssh_wizard(
            self.c,
            hostname="signet.lnd.lnorb.com",
            node_type="lnd",
            ssh_cert_path="lnorb_com.cer",
            rest_port="8080",
            protocol="rest",
            ln_cert_path="/home/ubuntu/dev/plebnet-playground-docker/volumes/lnd_datadir/tls.cert",
            ln_macaroon_path="/home/ubuntu/dev/plebnet-playground-docker/admin.macaroon",
        )
        pk = "0227750e13a6134c1f1e510542a88e3f922107df8ef948fc3ff2a296fca4a12e47"
        ln = factory(pk)
        info = ln.get_info()
        self.assertTrue(info.alias in ["signet.lnd.lnorb.conf", "signet.lnd.lnorb.com"])
        node.delete(self.c, pubkey=pk)

    def test_cli_lnd_grpc_ssh_wizard(self):
        self.c = Context(Connection("localhost").config)
        node.ssh_wizard(
            self.c,
            hostname="signet.lnd.lnorb.com",
            node_type="lnd",
            ssh_cert_path="lnorb_com.cer",
            rest_port="10009",
            protocol="grpc",
            ln_cert_path="/home/ubuntu/dev/plebnet-playground-docker/volumes/lnd_datadir/tls.cert",
            ln_macaroon_path="/home/ubuntu/dev/plebnet-playground-docker/admin.macaroon",
        )
        pk = "0227750e13a6134c1f1e510542a88e3f922107df8ef948fc3ff2a296fca4a12e47"
        ln = factory(pk)
        info = ln.get_info()
        self.assertTrue(info.alias in ["signet.lnd.lnorb.conf", "signet.lnd.lnorb.com"])
        node.delete(self.c, pubkey=pk)

# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-21 12:39:49
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-25 09:59:28

from unittest import TestCase
import unittest
from fabric import Connection
from invoke.context import Context

from build_system.monkey_patch import fix_annotations
from orb.ln import factory

fix_annotations()
from orb.cli import node
from orb.cli.utils import get_default_id


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
            use_node=True,
        )
        pk = get_default_id()
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
            use_node=True,
        )
        pk = get_default_id()
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
        pk = get_default_id()
        ln = factory(pk)
        info = ln.get_info()
        self.assertTrue(info.alias in ["signet.lnd.lnorb.conf", "signet.lnd.lnorb.com"])
        node.delete(self.c, pubkey=pk)


if __name__ == "__main__":
    unittest.main()

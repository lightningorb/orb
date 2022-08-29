# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-29 08:13:12
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-29 12:54:43


from .cli_test_case import CLITestCase
from orb.ln import factory
from orb.cli.utils import get_default_id
from random import shuffle
from orb.app import App


def pytest_generate_tests(metafunc):
    if "pubkey" in metafunc.fixturenames:
        metafunc.parametrize(
            "pubkey", [("cln", "rest"), ("lnd", "rest"), ("lnd", "grpc")], indirect=True
        )


class TestOrbApp(CLITestCase):
    def test_orb_app_channels(self, pubkey):
        App().run(pubkey=pubkey)
        ln = factory(pubkey)
        App().build(ln)
        app = App.get_running_app()
        assert app
        assert app.channels
        app.stop()

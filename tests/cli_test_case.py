# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-12 08:27:51
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-23 05:51:19

import unittest
from fabric import Connection
from invoke.context import Context
from io import StringIO
import sys
import os
from build_system.monkey_patch import fix_annotations

fix_annotations()


old_stdout = sys.stdout

from pathlib import Path
import sys

parent_dir = Path(__file__).parent.parent
for p in (parent_dir / Path("third_party")).glob("*"):
    sys.path.append(p.as_posix())

names = ("name", "protocol", "impl")


def get_params(target: str = "all"):
    import os

    vals = []

    if target in ["lnd", "lnd_rest", "rest", "all"]:
        vals.append(("lnd_rest", "rest", "lnd"))
    if target in ["lnd", "lnd_grpc", "grpc", "all"]:
        vals.append(("lnd_grpc", "grpc", "lnd"))
    if target in ["cln", "cln_rest", "rest", "all"]:
        vals.append(("cln_rest", "rest", "cln"))
    # if target in ["cln", "cln_grpc", "grpc"]:
    #   vals.append(("cln_grpc", "grpc", "cln"))

    return [names, vals]


class CLITestCase(unittest.TestCase):
    def setUp(self):
        os.environ["ORB_CLI_NO_COLOR"] = "1"
        os.environ["ORB_INTEGRATION_TESTS"] = "1"
        self.c = Context(Connection("localhost").config)
        self.c.run(
            f"./main.py node.create-orb-public --protocol {self.protocol} --node-type {self.impl}"
        )
        self.start_capture()

    def tearDown(self):
        del os.environ["ORB_CLI_NO_COLOR"]
        del os.environ["ORB_INTEGRATION_TESTS"]
        self.c.run(f"./main.py node.delete")
        del self.c
        self.stop_capture()

    def start_capture(self):
        self._stdout = StringIO()
        sys.stdout = self._stdout

    def stop_capture(self):
        sys.stdout = old_stdout

    @property
    def stdout(self):
        return self._stdout.getvalue()

    def clear_stdout():
        self._stdout = StringIO()

    def get_stdout(self, flush=False):
        stdout = self.stdout
        if flush:
            self.start_capture()
        return stdout

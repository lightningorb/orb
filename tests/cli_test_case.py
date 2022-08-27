# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-12 08:27:51
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-27 09:25:40

import pytest
import sys
from orb.misc.monkey_patch import fix_annotations


fix_annotations()

from pathlib import Path

parent_dir = Path(__file__).parent.parent
for p in (parent_dir / Path("third_party")).glob("*"):
    sys.path.append(p.as_posix())

# def get_params(target: str = "all"):
#     import os

#     vals = []

#     if target in ["lnd", "lnd_rest", "rest", "all"]:
#         vals.append(("lnd_rest", "rest", "lnd"))
#     if target in ["lnd", "lnd_grpc", "grpc", "all"]:
#         vals.append(("lnd_grpc", "grpc", "lnd"))
#     if target in ["cln", "cln_rest", "rest", "all"]:
#         vals.append(("cln_rest", "rest", "cln"))
#     # if target in ["cln", "cln_grpc", "grpc"]:
#     #   vals.append(("cln_grpc", "grpc", "cln"))

#     return [names, vals]


class CLITestCase:
    @pytest.fixture
    def c(self, request):
        from orb.cli import node
        import os
        from fabric import Connection
        from invoke.context import Context

        os.environ["ORB_CLI_NO_COLOR"] = "1"
        os.environ["ORB_INTEGRATION_TESTS"] = "1"
        c = Context(Connection("localhost").config)
        node.create_orb_public(c, *request.param)
        self.prot, self.impl = request.param
        yield c
        del os.environ["ORB_CLI_NO_COLOR"]
        del os.environ["ORB_INTEGRATION_TESTS"]
        node.delete(c)

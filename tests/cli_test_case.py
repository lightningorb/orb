# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-12 08:27:51
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-28 06:18:20

import sys
from pathlib import Path

import pytest

from orb.cli.utils import get_default_id

parent_dir = Path(__file__).parent.parent
for p in (parent_dir / Path("third_party")).glob("*"):
    sys.path.append(p.as_posix())


class CLITestCase:
    @pytest.fixture
    def pubkey(self, request):
        from orb.cli import node
        import os

        os.environ["ORB_CLI_NO_COLOR"] = "1"
        os.environ["ORB_INTEGRATION_TESTS"] = "1"
        node.create_orb_public(*request.param)
        self.impl, self.prot = request.param
        yield get_default_id()
        del os.environ["ORB_CLI_NO_COLOR"]
        del os.environ["ORB_INTEGRATION_TESTS"]
        node.delete()

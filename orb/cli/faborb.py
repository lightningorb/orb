# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-08 14:04:25
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-27 07:10:27

import sys

sys.argv = [sys.argv[0]]
from pathlib import Path

from orb.misc.monkey_patch import fix_annotations

fix_annotations()

from orb.cli import chain
from orb.cli import node
from orb.cli import invoice
from orb.cli import pay
from orb.cli import rebalance
from orb.cli import channel
from orb.cli import peer
from orb.cli import test

from invoke import Collection

parent_dir = Path(__file__).parent
for p in (parent_dir / Path("third_party")).glob("*"):
    sys.path.append(p.as_posix())


namespace = Collection(chain, node, invoice, pay, rebalance, channel, peer, test)

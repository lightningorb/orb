#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-07-14 18:22:27
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-05 14:15:01

import os
import sys
from pathlib import Path

os.environ["KIVY_NO_ARGS"] = "1"

parent_dir = Path(__file__).parent
for p in (parent_dir / Path("third_party")).glob("*"):
    sys.path.append(p.as_posix())

if len(sys.argv) == 1:
    import kivy

    kivy.require("2.1.0")

    from orb.orb_main import main
    from orb.core_ui.hidden_imports import *

    main()
elif len(sys.argv) == 2 and sys.argv[-1].endswith(".py"):
    from importlib import __import__

    __import__(sys.argv[-1].split(".")[0])

else:

    import typer

    from orb.cli import node
    from orb.cli import invoice
    from orb.cli import peer
    from orb.cli import pay
    from orb.cli import channel
    from orb.cli import test
    from orb.cli import chain
    from orb.cli import web
    from orb.cli import network

    app = typer.Typer()
    app.add_typer(node.app, name="node")
    app.add_typer(invoice.app, name="invoice")
    app.add_typer(pay.app, name="pay")
    app.add_typer(channel.app, name="channel")
    app.add_typer(test.app, name="test")
    app.add_typer(peer.app, name="peer")
    app.add_typer(chain.app, name="chain")
    app.add_typer(web.app, name="web")
    app.add_typer(network.app, name="network")

    if __name__ == "__main__":
        app()

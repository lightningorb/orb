#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-07-14 18:22:27
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-26 15:25:13

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
else:

    from fabric.main import program

    if len(sys.argv) == 2:
        if sys.argv[1] in ["-h", "--help"]:
            sys.argv[1] = "-l"

    sys.argv.insert(1, "-c")
    sys.argv.insert(2, "orb/cli/faborb")

    sys.exit(program.run())

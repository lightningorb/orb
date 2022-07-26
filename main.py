# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-07-14 18:22:27
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-21 15:14:45

import sys
from pathlib import Path

print("appending paths to include lnd and third party modules")
parent_dir = Path(__file__).parent
# for p in (parent_dir / Path("third_party")).glob("*"):
#     sys.path.append(p.as_posix())
sys.path.append((parent_dir / Path("third_party/contextmenu")).as_posix())
sys.path.append((parent_dir / Path("third_party/arrow")).as_posix())
sys.path.append((parent_dir / Path("third_party/python-qrcode/")).as_posix())
sys.path.append((parent_dir / Path("third_party/forex-python/")).as_posix())
sys.path.append((parent_dir / Path("third_party/bezier/src/python/")).as_posix())
sys.path.append((parent_dir / Path("third_party/colour/")).as_posix())
sys.path.append((parent_dir / Path("third_party/currency-symbols/")).as_posix())
sys.path.append((parent_dir / Path("third_party/lnurl/")).as_posix())

from orb.orb_main import main
from orb.core_ui.hidden_imports import *
from orb.core.orb_logging import get_logger

main()

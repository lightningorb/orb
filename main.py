# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-07-14 18:22:27
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-14 22:45:39

import sys
from pathlib import Path

if __name__ == "__main__":
    print("appending paths to include lnd and third party modules")
    print(Path(__file__).as_posix())
    print(Path(__file__).parent.as_posix())
    parent_dir = Path(__file__).parent
    sys.path.append((parent_dir / Path("orb/lnd")).as_posix())
    sys.path.append((parent_dir / Path("orb/lnd/grpc_generated")).as_posix())
    sys.path.append((parent_dir / Path("third_party/contextmenu")).as_posix())
    sys.path.append((parent_dir / Path("third_party/arrow")).as_posix())
    sys.path.append((parent_dir / Path("third_party/python-qrcode/")).as_posix())
    sys.path.append((parent_dir / Path("third_party/forex-python/")).as_posix())
    sys.path.append((parent_dir / Path("third_party/bezier/src/python/")).as_posix())
    sys.path.append((parent_dir / Path("third_party/colour/")).as_posix())
    sys.path.append((parent_dir / Path("third_party/currency-symbols/")).as_posix())
    from orb.orb_main import main

    main()

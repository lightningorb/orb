# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-08 19:08:11
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-07 06:00:01

import os
from pathlib import Path
from configparser import ConfigParser

from orb.misc.utils_no_kivy import _get_user_data_dir_static


def get_default_id():
    conf_path = Path(_get_user_data_dir_static()) / f"orbconnector/orbconnector.ini"
    if conf_path.exists():
        conf = ConfigParser()
        conf.read(conf_path.as_posix())
        try:
            return conf.get("ln", "identity_pubkey")
        except:
            pass
    return ""


def pprint_from_ansi(*args, end="\n"):
    if os.environ.get("ORB_CLI_NO_COLOR"):
        import sys

        sys.stdout.write(" ".join(str(x) for x in args))
        sys.stdout.write("\n")
        sys.stdout.flush()
    else:
        from rich.pretty import pprint
        from rich.text import Text
        from rich.console import Console

        Console().print(Text.from_ansi(args[0]))


def pprint(*args, end="\n"):
    if os.environ.get("ORB_CLI_NO_COLOR"):
        import sys

        sys.stdout.write(" ".join(str(x) for x in args))
    else:
        from rich.pretty import pprint

        pprint(args[0], expand_all=True)

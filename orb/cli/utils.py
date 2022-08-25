# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-08 19:08:11
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-21 06:51:42

from orb.misc.utils_no_kivy import _get_user_data_dir_static
from configparser import ConfigParser
from pathlib import Path


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

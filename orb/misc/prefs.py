# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 13:24:06
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-16 13:18:20

from orb.misc.utils import *
from pathlib import Path
from orb.misc.utils import pref


def is_mock():
    return pref("lnd.protocol") == "mock"


def is_rest():
    return pref("lnd.protocol") == "rest"


def is_grpc():
    return pref("lnd.protocol") == "grpc"


def hostname():
    app = App.get_running_app()
    return app.config["lnd"]["hostname"]


def grpc_port():
    app = App.get_running_app()
    return app.config["lnd"]["grpc_port"]


def macaroon():
    app = App.get_running_app()
    return app.config["lnd"]["macaroon_admin"]


def cert():
    app = App.get_running_app()
    return app.config["lnd"]["tls_certificate"].encode()


def cert_path():
    app = App.get_running_app()
    return (Path(app.user_data_dir) / pref("path.cert") / "tls.cert").as_posix()


def inverted_channels():
    return bool(pref("display.inverted_channels"))

# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 13:24:06
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-06 14:58:39

from orb.misc.utils import *
from pathlib import Path
import tempfile
from orb.misc.utils import pref
from orb.misc.utils import desktop


def is_mock():
    return pref("ln.protocol") == "mock"


def is_rest():
    return pref("ln.protocol") == "rest"


def is_grpc():
    return pref("ln.protocol") == "grpc"


def hostname():
    app = App.get_running_app()
    return app.config["ln"]["hostname"]


def grpc_port():
    app = App.get_running_app()
    return app.config["ln"]["grpc_port"]


def macaroon():
    app = App.get_running_app()
    return app.config["ln"]["macaroon_admin"]


def cert():
    app = App.get_running_app()
    return app.config["ln"]["tls_certificate"].encode()


# @lru_cache(maxsize=None)
def cert_path(use_tmp=False, node_type="lnd"):
    """
    Get the path to the temp TLS cert file.
    On mobile we store it in the temp diretory, since it's only accessible by the
    app, while on desktop we keep the cert in the user's app data dir.
    """
    if use_tmp:
        return Path(tempfile.gettempdir()) / f"{node_type}_f66d6b24ccfb"
    if desktop:
        app = App.get_running_app()
        return Path(app.user_data_dir) / pref("path.cert") / f"{node_type}_tls.cert"
    else:
        return Path(tempfile.gettempdir()) / f"{node_type}_f66d6b24ccfb"


def inverted_channels():
    return bool(pref("display.inverted_channels"))

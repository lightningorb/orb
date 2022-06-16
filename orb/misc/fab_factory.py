# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-10 08:15:01
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-10 11:52:25

from orb.misc.utils import pref
from orb.misc.sec_rsa import *


def Connection(
    use_prefs=True,
    host=None,
    port=None,
    auth=None,
    username=None,
    password=None,
    cert_path=None,
):

    if use_prefs:
        host = pref("host.hostname")
        auth = pref("host.auth_type")
        port = int(pref("host.port"))
        username = pref("host.username")
        priv, pub = get_sec_keys()
        password = pref("host.password")
        try:
            password = decrypt(password, priv)
        except Exception as e:
            print(e)
        cert_path = pref("host.certificate")

    from fabric import Connection as Con

    ck = {}
    if auth == "certificate":
        ck["key_filename"] = cert_path
    elif auth == "password":
        ck["password"] = password

    return Con(
        host,
        port=port,
        connect_kwargs=ck,
        user=username,
    )

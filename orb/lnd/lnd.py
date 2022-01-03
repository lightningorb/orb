# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-31 04:51:50
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-03 16:32:54

from orb.misc.utils import pref
from traceback import print_exc

lnd = None


def Lnd():
    """
    Return the appropriate Lnd class based on protocol.
    """

    global lnd

    if lnd is None:
        if pref("lnd.protocol") == "grpc":
            from orb.lnd.lnd_grpc import LndGRPC

            try:
                lnd = LndGRPC(
                    tls_certificate=pref("lnd.tls_certificate"),
                    server=pref("lnd.hostname"),
                    network=pref("lnd.network"),
                    macaroon=pref("lnd.macaroon_admin"),
                )
            except:
                print(print_exc())
                from orb.lnd.lnd_mock import LndMock

                lnd = LndMock()
        elif pref("lnd.protocol") == "rest":
            from orb.lnd.lnd_rest import LndREST
            from kivy.app import App
            import os

            app = App.get_running_app()
            data_dir = app.user_data_dir
            cert_path = os.path.join(data_dir, "tls.cert")
            lnd = LndREST(
                tls_certificate=cert_path,
                server=pref("lnd.hostname"),
                network=pref("lnd.network"),
                macaroon=pref("lnd.macaroon_admin"),
                port=int(pref("lnd.rest_port")),
            )
        elif pref("lnd.protocol") == "mock":
            from orb.lnd.lnd_mock import LndMock

            lnd = LndMock()

    return lnd

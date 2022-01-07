# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-31 04:51:50
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-07 20:00:09

from orb.misc.utils import pref
from traceback import print_exc
from kivy.app import App
import os

lnd = {}


class Protocol:
    rest = "rest"
    mock = "mock"
    grpc = "grpc"


def Lnd():
    """
    Return the appropriate Lnd class based on protocol.
    """

    protocol = pref("lnd.protocol")

    if lnd.get(protocol) is None:
        if protocol == None:
            from orb.lnd.lnd_mock import LndMock

            lnd[protocol] = LndMock()
        if protocol == Protocol.grpc:
            from orb.lnd.lnd_grpc import LndGRPC

            try:
                lnd[protocol] = LndGRPC(
                    tls_certificate=pref("lnd.tls_certificate"),
                    server=pref("lnd.hostname"),
                    network=pref("lnd.network"),
                    macaroon=pref("lnd.macaroon_admin"),
                )
            except:
                print(print_exc())
                from orb.lnd.lnd_mock import LndMock

                lnd[protocol] = LndMock()
        elif pref("lnd.protocol") == Protocol.rest:
            from orb.lnd.lnd_rest import LndREST

            app = App.get_running_app()
            data_dir = app.user_data_dir
            cert_path = os.path.join(data_dir, "tls.cert")
            lnd[protocol] = LndREST(
                tls_certificate=cert_path,
                server=pref("lnd.hostname"),
                network=pref("lnd.network"),
                macaroon=pref("lnd.macaroon_admin"),
                port=int(pref("lnd.rest_port")),
            )
        elif pref("lnd.protocol") == Protocol.mock:
            from orb.lnd.lnd_mock import LndMock

            lnd[protocol] = LndMock()

    return lnd[protocol]

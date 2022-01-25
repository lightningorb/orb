# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-31 04:51:50
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-26 03:00:23

from orb.misc.utils import pref
from traceback import print_exc
from kivy.app import App
import os

from orb.misc.certificate_secure import CertificateSecure
from orb.misc.macaroon_secure import MacaroonSecure
from orb.misc.prefs import cert_path

lnd = {}


class Protocol:
    rest = "rest"
    mock = "mock"
    grpc = "grpc"


mac = None


def Lnd():
    """
    Return the appropriate Lnd class based on protocol.
    """
    global mac

    protocol = pref("lnd.protocol")

    if not mac:
        mac_secure = MacaroonSecure.init_from_encrypted(
            pref("lnd.macaroon_admin").encode()
        )
        mac = mac_secure.as_plain_macaroon().macaroon.decode()
        print(mac)

    if lnd.get(protocol) is None:
        if protocol == None:
            from orb.lnd.lnd_mock import LndMock

            lnd[protocol] = LndMock()
        if protocol == Protocol.grpc:
            from orb.lnd.lnd_grpc import LndGRPC

            try:
                cert_secure = CertificateSecure.init_from_encrypted(
                    pref("lnd.tls_certificate").encode()
                )
                cert = cert_secure.as_plain_certificate()
                lnd[protocol] = LndGRPC(
                    tls_certificate=cert.reformat(),
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
            lnd[protocol] = LndREST(
                tls_certificate=cert_path().as_posix(),
                server=pref("lnd.hostname"),
                network=pref("lnd.network"),
                macaroon=mac,
                port=int(pref("lnd.rest_port")),
            )
        elif pref("lnd.protocol") == Protocol.mock:
            from orb.lnd.lnd_mock import LndMock

            lnd[protocol] = LndMock()

    return lnd[protocol]

# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-31 04:51:50
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-05-27 09:29:53

from traceback import format_exc
from threading import Lock

from orb.misc.certificate_secure import CertificateSecure
from orb.misc.macaroon_secure import MacaroonSecure

lnd = {}

lnd_lock = Lock()


class Protocol:
    rest = "rest"
    mock = "mock"
    grpc = "grpc"


mac = None
mac_invalid = False


def Lnd():
    """
    Return the appropriate Lnd class based on protocol.
    """
    with lnd_lock:
        from orb.misc.utils import pref
        from kivy.app import App
        from orb.misc.prefs import cert_path

        global mac
        global mac_invalid

        protocol = pref("lnd.protocol")

        if not mac and not mac_invalid:
            mac_secure = MacaroonSecure.init_from_encrypted(
                pref("lnd.macaroon_admin").encode()
            )
            mac = mac_secure.as_plain_macaroon().macaroon.decode()
            if not mac:
                print("Macaroon is invalid")
                mac_invalid = True

        if lnd.get(protocol) is None:
            if protocol == Protocol.grpc:
                from orb.lnd.lnd_grpc import LndGRPC

                try:
                    cert_secure = CertificateSecure.init_from_encrypted(
                        pref("lnd.tls_certificate").encode()
                    )
                    cert = cert_secure.as_plain_certificate()
                    if cert.is_well_formed():
                        lnd[protocol] = LndGRPC(
                            tls_certificate=cert.reformat(),
                            server=pref("lnd.hostname"),
                            network=pref("lnd.network"),
                            macaroon=mac,
                        )
                except:
                    print("could not start lnd grpc")
                    print(format_exc())
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

        if not lnd.get(protocol):
            from orb.lnd.lnd_mock import LndMock

            lnd[protocol] = LndMock()

        return lnd[protocol]

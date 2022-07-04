# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-31 04:51:50
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-29 17:43:21

from traceback import format_exc

from orb.misc.certificate_secure import CertificateSecure
from orb.misc.macaroon_secure import MacaroonSecure

lnd = {}


class Protocol:
    rest = "rest"
    mock = "mock"
    grpc = "grpc"


def decode_pref_mac(pref_mac):
    mac_secure = MacaroonSecure.init_from_encrypted(pref_mac.encode())
    mac = mac_secure.as_plain_macaroon().macaroon.decode()
    if not mac:
        print("Macaroon is invalid")
    return mac


def Lnd(
    fallback_to_mock=True,
    cache=True,
    use_prefs=True,
    hostname=None,
    protocol=None,
    mac_secure=None,
    mac=None,
    cert_secure=None,
    cert=None,
    rest_port=None,
    grpc_port=None,
):
    """
    Return the appropriate Lnd class based on protocol.
    """
    if use_prefs:
        from orb.misc.utils import pref

        hostname = pref("host.hostname")
        protocol = pref("lnd.protocol")
        mac_secure = pref("lnd.macaroon_admin")
        cert_secure = pref("lnd.tls_certificate")
        rest_port = int(pref("lnd.rest_port"))
        grpc_port = int(pref("lnd.grpc_port"))

    if lnd.get(protocol) is None or not cache:
        if protocol == Protocol.grpc:
            from orb.lnd.lnd_grpc import LndGRPC

            try:
                if (not mac) and mac_secure:
                    mac = decode_pref_mac(mac_secure)
                if (not cert) and cert_secure:
                    cert_secure_obj = CertificateSecure.init_from_encrypted(
                        cert_secure.encode()
                    )
                    cert = cert_secure_obj.as_plain_certificate()
                    if not cert.is_well_formed():
                        print("certificate badly formed")
                    else:
                        cert = cert.reformat()
                lnd[protocol] = LndGRPC(
                    tls_certificate=cert,
                    server=hostname,
                    port=grpc_port,
                    macaroon=mac,
                )
            except:
                print("could not start lnd grpc")
                print(format_exc())
        elif protocol == Protocol.rest:
            from orb.lnd.lnd_rest import LndREST
            from orb.misc.prefs import cert_path

            if (not mac) and mac_secure:
                mac = decode_pref_mac(mac_secure)
            if (not cert) and cert_secure:
                cert_secure_obj = CertificateSecure.init_from_encrypted(
                    cert_secure.encode()
                )
                cert = cert_secure_obj.as_plain_certificate().cert

            if cert:
                with cert_path(use_tmp=True).open("w") as f:
                    f.write(cert)

            lnd[protocol] = LndREST(
                tls_certificate=(
                    cert_path(use_tmp=True).as_posix()
                    if cert
                    else None
                ),
                server=hostname,
                macaroon=mac,
                port=rest_port,
            )

    success = lnd.get(protocol)

    if protocol == Protocol.mock or ((not success) and fallback_to_mock):
        from orb.lnd.lnd_mock import LndMock

        lnd[protocol] = LndMock()

    if not cache and protocol in lnd:
        ret = lnd[protocol]
        del lnd[protocol]
        return ret
    return lnd[protocol]

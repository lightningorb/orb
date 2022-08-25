# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-31 04:51:50
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-20 10:08:03

from orb.misc.certificate_secure import CertificateSecure
from orb.misc.macaroon_secure import MacaroonSecure

from pathlib import Path
import sys
from traceback import format_exc

cln = {}


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


def Cln(
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
    version=None,
):
    """
    Return the appropriate Cln class based on protocol.
    """
    if use_prefs:
        from orb.misc.utils import pref

        hostname = pref("host.hostname")
        protocol = pref("ln.protocol")
        mac_secure = pref("ln.macaroon_admin")
        cert_secure = pref("ln.tls_certificate")
        rest_port = int(pref("ln.rest_port"))
        grpc_port = int(pref("ln.grpc_port"))
        version = pref("ln.version")

    if cln.get(protocol) is None or not cache:
        if protocol == Protocol.grpc:
            set_cln_grpc_path_for_version(version=version or "v0.11.2")
            from orb.cln.cln_grpc import ClnGRPC

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
                cln[protocol] = ClnGRPC(
                    tls_certificate=cert,
                    server=hostname,
                    port=grpc_port,
                    macaroon=mac,
                )
            except:
                print("could not start cln grpc")
                print(format_exc())
        elif protocol == Protocol.rest:
            from orb.cln.cln_rest import ClnREST
            from orb.misc.utils_no_kivy import cert_path

            if (not mac) and mac_secure:
                mac = decode_pref_mac(mac_secure)
            if (not cert) and cert_secure:
                cert_secure_obj = CertificateSecure.init_from_encrypted(
                    cert_secure.encode()
                )
                cert = cert_secure_obj.as_plain_certificate().cert

            if cert:
                with cert_path(hostname).open("w") as f:
                    f.write(cert)

            cln[protocol] = ClnREST(
                tls_certificate=(cert_path(hostname).as_posix() if cert else None),
                server=hostname,
                macaroon=mac,
                port=rest_port,
            )

    if not cache and protocol in cln:
        ret = cln[protocol]
        del cln[protocol]
        return ret
    return cln[protocol]


def set_cln_grpc_path_for_version(version="v0.11.2"):
    """
    Make sure the path to cln's grpc libraries are in python's path
    """
    version_dir = version.replace(".", "_").replace("-", "_")
    main_dir = Path(sys.argv[0]).parent
    path = (main_dir / Path(f"orb/cln/grpc_generated/{version_dir}")).as_posix()
    if path not in sys.path:
        sys.path.append(path)

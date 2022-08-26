# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-08 19:12:26
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-26 14:58:40

import re
import os
import codecs
from tempfile import TemporaryDirectory
from pathlib import Path
from orb.misc.utils_no_kivy import _get_user_data_dir_static
from orb.cli.utils import get_default_id
from fabric import Connection
from orb.misc.macaroon_secure import MacaroonSecure
from orb.misc.certificate_secure import CertificateSecure
from orb.ln import Ln

from orb.ln import factory
from configparser import ConfigParser
from invoke import task
from .chalk import chalk


@task()
def delete(c, pubkey: str = ""):
    """
    Delete node information.
    """
    if not pubkey:
        pubkey = get_default_id()
    conf_path = Path(_get_user_data_dir_static()) / f"orb_{pubkey}"
    if conf_path.exists():
        from shutil import rmtree

        rmtree(conf_path.as_posix())
        print(chalk().green(f"{conf_path} deleted"))
    else:
        print(chalk().red(f"{conf_path} does not exist"))


@task(help=dict(show_info="If True, then connect and return node information"))
def list(c, show_info=False):
    """
    Get a list of nodes known to Orb.
    """
    data_dir = Path(_get_user_data_dir_static())
    for x in data_dir.glob("orb_*"):
        m = re.match(r"^orb_([a-zA-Z0-9]{66})$", x.name)
        if m and x.is_dir():
            pk = m.group(1)
            if show_info:
                print(f"Showing info for: {chalk().greenBright(pk)}:")
                try:
                    info(c, pk)
                except:
                    print(f"Failed to get info for: {chalk().red(pk)}:")
            else:
                print(chalk().green(pk))


@task(help=dict(pubkey="The Pubkey to use as the default pubkey for all Orb commands"))
def info(c, pubkey: str = ""):
    """
    Get node information.
    """
    if not pubkey:
        pubkey = get_default_id()
    for k, v in factory(pubkey).get_info().__dict__.items():
        print(f"{chalk().greenBright(k)}: {chalk().blueBright(v)}")


@task
def balance(c, pubkey: str = ""):
    """
    Get total balance, for both on-chain and balance in channels.
    """
    if not pubkey:
        pubkey = get_default_id()
    from orb.logic.balance import balance as bal

    print(chalk().green(f"{bal(factory(pubkey)):_}"))


@task(help=dict(pubkey="The Pubkey to use as the default pubkey for all Orb commands"))
def use(c, pubkey: str):
    """
    Use the given node as default.
    """
    conf_dir = Path(_get_user_data_dir_static()) / "orbconnector"
    if not conf_dir.is_dir():
        os.makedirs(conf_dir.as_posix(), exist_ok=True)
    conf_path = conf_dir / "orbconnector.ini"
    conf = ConfigParser()
    conf.filename = conf_path.as_posix()
    conf.add_section("ln")
    conf.set("ln", "identity_pubkey", pubkey)
    conf.write(conf_path.open("w"))
    print(chalk().green(f"Setting {pubkey} as default"))


@task(
    help=dict(
        protocol="rest or grpc",
        node_type="lnd or cln",
        use_node="Set this node as the default.",
    )
)
def create_orb_public(c, protocol: str, node_type: str, use_node: bool = True):
    """
    Create public testnet node.
    """
    from orb.misc.macaroon_secure import MacaroonSecure

    hostname = dict(cln="regtest.cln.lnorb.com", lnd="signet.lnd.lnorb.com")[node_type]
    rest_port = dict(cln="3001", lnd="8080")[node_type]
    grpc_port = dict(cln="10010", lnd="10009")[node_type]
    cert = dict(
        cln="-----BEGIN CERTIFICATE-----\nMIIDpzCCAo+gAwIBAgIUAObOYMfHkbsVkiIJUs3/gkqdNAEwDQYJKoZIhvcNAQEL\nBQAwUjELMAkGA1UEBhMCVVMxDDAKBgNVBAgMA0ZvbzEMMAoGA1UEBwwDQmFyMQww\nCgYDVQQKDANCYXoxGTAXBgNVBAMMEGMtbGlnaHRuaW5nLXJlc3QwHhcNMjIwODIz\nMDEwODIzWhcNMjMwODIzMDEwODIzWjBSMQswCQYDVQQGEwJVUzEMMAoGA1UECAwD\nRm9vMQwwCgYDVQQHDANCYXIxDDAKBgNVBAoMA0JhejEZMBcGA1UEAwwQYy1saWdo\ndG5pbmctcmVzdDCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBANLya1KP\nzljILwk65lYb9qUisO6mEubfs88IXt0M6U1nrVEkeWOkXvoqwjrRDWx416sIF8eX\n1v1Ymxd2NPc7/TQDndCIXJNg98WcvZY1nux02MwfDjNJuNGMbmLqTAZ7mNZRj6uN\nLFh9f3l6j4VJrHjNNtTF03XdJxvjJhGwR4suyttUl0/3PTU3DOTjeexFnbCjRNMV\ny3zG/0rmrDMNBpF6J9b6jg6BuvyKN4ux+mdVsLhAcQf0EWBa/iSjco7DowmJH2XS\nxzity1wHWiUIYYoijBWna9ziGOCLeVirW/ml2mMGiKhxBOh4Hc3o6KfMx+EaxycO\nczmkZ3sYBiTj6N8CAwEAAaN1MHMwHQYDVR0OBBYEFFEnhV78bRE0mhfSr1AWb/ep\nlxbQMB8GA1UdIwQYMBaAFFEnhV78bRE0mhfSr1AWb/eplxbQMA8GA1UdEwEB/wQF\nMAMBAf8wIAYDVR0RBBkwF4IVcmVndGVzdC5jbG4ubG5vcmIuY29tMA0GCSqGSIb3\nDQEBCwUAA4IBAQB+Vf0LoNVrinPW54fgYHH0v+mn71JH5Ungc1Kfi+GMlVFBMIs8\nK4dQ8+X/wlctexLkMr7vrr4hNPMC1sV8MFlknFELZj5z53jExI3sh4IfT2p5Jph7\n4/95dlcbjG0uxjQOFj0NwLxdWQ6WLPhGLE6qh7JwWl0n2nwe++xkObuBfDX9MBi3\nbwzr2Z6Xa184z/kKGYVTlTLGlIMaQ6rUQjIEJUbFEucOTI3ufQt+nicnfsshIAd5\nWkPV9G7D+ctRoLMxYZ15CC5zRGhkwAnYf524EBhbwZaEB0GXKIepMFMswZf7z0lp\nRWAHbwRXCGxHBCwSDDi9KfUEKt9NTw9hhmc1\n-----END CERTIFICATE-----\n",
        lnd="-----BEGIN CERTIFICATE-----\nMIICOjCCAeCgAwIBAgIQE3My2g1g5yRsD35v2/4qfDAKBggqhkjOPQQDAjA4MR8w\nHQYDVQQKExZsbmQgYXV0b2dlbmVyYXRlZCBjZXJ0MRUwEwYDVQQDEww4NjBiYTVj\nNTQ3NzAwHhcNMjIwODIwMjE1MDQ1WhcNMjMxMDE1MjE1MDQ1WjA4MR8wHQYDVQQK\nExZsbmQgYXV0b2dlbmVyYXRlZCBjZXJ0MRUwEwYDVQQDEww4NjBiYTVjNTQ3NzAw\nWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAARRnSKy3uNVVrQXWhxEHoTXzwqCu4YC\ndSRDVqQyrJwR313Op0SChZZanZxigjFBKlapmQvNRy1IhNUxdkN2eTQ4o4HLMIHI\nMA4GA1UdDwEB/wQEAwICpDATBgNVHSUEDDAKBggrBgEFBQcDATAPBgNVHRMBAf8E\nBTADAQH/MB0GA1UdDgQWBBTu4yTg9J01l3rojEzSiDSd3RFwzzBxBgNVHREEajBo\nggw4NjBiYTVjNTQ3NzCCCWxvY2FsaG9zdIIUc2lnbmV0LmxuZC5sbm9yYi5jb22C\nBHVuaXiCCnVuaXhwYWNrZXSCB2J1ZmNvbm6HBH8AAAGHEAAAAAAAAAAAAAAAAAAA\nAAGHBKwWAAQwCgYIKoZIzj0EAwIDSAAwRQIgcwRSvTNqJPrV6xd+SFKZVg8AjIQw\njYcQ6dNQ0P9wTyECIQD4Vj3ac+b+35tVedYRX5sOJ7KWAEdHemwvl5OQS4Eg3w==\n-----END CERTIFICATE-----\n",
    )[node_type]
    mac = dict(
        cln="02010b632d6c696768746e696e67023e5475652041756720323320323032322030313a30383a323320474d542b303030302028436f6f7264696e6174656420556e6976657273616c2054696d652900000620f3760d5a3cc139d75c9f4ef895df847ea436ae94c2cd8ebfa07f2cce505ff5e5",
        lnd="0201036c6e6402f801030a106fb784f1598e0ce2f89c050b98139c8e1201301a160a0761646472657373120472656164120577726974651a130a04696e666f120472656164120577726974651a170a08696e766f69636573120472656164120577726974651a210a086d616361726f6f6e120867656e6572617465120472656164120577726974651a160a076d657373616765120472656164120577726974651a170a086f6666636861696e120472656164120577726974651a160a076f6e636861696e120472656164120577726974651a140a057065657273120472656164120577726974651a180a067369676e6572120867656e6572617465120472656164000006205d186c6864b437cd5d723eef6d064eae85467e7913f876a8b49bfe962028a2e8",
    )[node_type]
    network = dict(cln="regtest", lnd="signet")[node_type]
    create(
        c,
        hostname=hostname,
        mac_hex=mac,
        node_type=node_type,
        protocol=protocol,
        network=network,
        cert_plain=cert,
        rest_port=rest_port,
        grpc_port=grpc_port,
        use_node=use_node,
    )


@task(
    help=dict(
        hostname="IP address or DNS-resovable name for this host",
        mac_hex="Macaroon in hex format",
        node_type="cln or lnd",
        protocol="rest or grpc",
        network="mainnet / testnet / signet / regtest",
        rest_port="REST port (default: 8080)",
        grpc_port="GRPC port (default: 10009)",
        use_node="Set this node as the default (default: True).",
    )
)
def create(
    c,
    hostname: str,
    mac_hex: str,
    node_type: str,
    protocol: str,
    network: str,
    cert_plain: str = None,
    rest_port: int = 8080,
    grpc_port: int = 10009,
    use_node: bool = True,
):
    """
    Create node.
    """

    print(chalk().cyan(f"Encrypting mac"))
    mac_secure = MacaroonSecure.init_from_plain(mac_hex).macaroon_secure.decode()
    print(chalk().cyan(f"Encrypting cert"))
    cert_secure = CertificateSecure.init_from_plain(cert_plain).cert_secure.decode()
    print(chalk().cyan(f"Connecting to: {hostname}"))
    ln = Ln(
        node_type=node_type,
        fallback_to_mock=False,
        cache=False,
        use_prefs=False,
        hostname=hostname,
        protocol=protocol,
        mac_secure=mac_secure,
        cert_secure=cert_secure,
        rest_port=rest_port,
        grpc_port=grpc_port,
    )
    try:
        pubkey = ln.get_info().identity_pubkey
        print(chalk().greenBright(f"Connected to: {pubkey}"))
    except Exception as e:
        print(chalk().red(f"Failed to connect: {e}"))
        return
    conf_dir = Path(_get_user_data_dir_static()) / f"orb_{pubkey}"
    if not conf_dir.is_dir():
        conf_dir.mkdir()
        print(chalk().green(f"{conf_dir} created"))
    conf_path = conf_dir / f"orb_{pubkey}.ini"
    conf = ConfigParser()
    conf.filename = conf_path.as_posix()
    conf.add_section("host")
    conf.set("host", "hostname", hostname)
    conf.set("host", "type", node_type)
    conf.add_section("ln")
    conf.set("ln", "macaroon_admin", mac_secure)
    conf.set("ln", "tls_certificate", cert_secure)
    conf.set("ln", "network", network)
    conf.set("ln", "protocol", protocol)
    conf.set("ln", "rest_port", str(rest_port))
    conf.set("ln", "grpc_port", str(grpc_port))
    conf.set("ln", "identity_pubkey", pubkey)
    conf.write(conf_path.open("w"))
    print(chalk().green(f"{conf_path} created"))
    if use_node:
        use(c, pubkey)


@task(
    help=dict(
        hostname="IP address or DNS-resovable name for this host",
        node_type="cln or lnd",
        protocol="rest or grpc",
        network="mainnet / testnet / signet / regtest",
        rest_port="REST port (default: 8080)",
        grpc_port="GRPC port (default: 10009)",
        use_node="Set this node as the default (default: True).",
    )
)
def create_from_cert_files(
    c,
    hostname: str,
    mac_file_path: str,
    node_type: str,
    protocol: str,
    network: str,
    cert_file_path: str = None,
    rest_port: int = 8080,
    grpc_port: int = 10009,
    use_node: bool = True,
):
    """
    Create node and use certificate files.
    """
    print(chalk().cyan(f"Reading mac: {mac_file_path}"))
    cert_plain, mac_hex = "", ""
    with open(mac_file_path, "rb") as f:
        mac_hex = codecs.encode(f.read(), "hex")
    if cert_file_path:
        print(chalk().cyan(f"Reading cert: {cert_file_path}"))
        with open(cert_file_path, "r") as f:
            cert_plain = f.read()

    create(
        c,
        hostname=hostname,
        mac_hex=mac_hex,
        node_type=node_type,
        protocol=protocol,
        network=network,
        cert_plain=cert_plain,
        rest_port=rest_port,
        grpc_port=grpc_port,
        use_node=use_node,
    )


@task(
    help=dict(
        hostname="IP address or DNS-resovable name for this host",
        node_type="cln or lnd",
        use_node="Set this node as the default (Default: True).",
        network="mainnet / testnet / signet / regtest",
        protocol="Connect via rest or grpc. (Default: rest).",
        rest_port="REST port (default: 8080)",
        grpc_port="GRPC port (default: 10009)",
        ssh_cert_path="SSH session certificate, if not already specified in .ssh/config",
        ssh_password="SSH session password (if not using a pem certificate)",
        ssh_port="SSH session port to use, if not already specified in .ssh/config. (Default: 22).",
        ssh_user="SSH session user, if not already specified in .ssh/config. (Default: 22).",
    )
)
def ssh_wizard(
    c,
    hostname: str,
    node_type: str,
    ssh_cert_path: str,
    ssh_password: str = "",
    ln_cert_path: str = "",
    ln_macaroon_path: str = "",
    network: str = "mainnet",
    protocol: str = "rest",
    rest_port: int = 8080,
    grpc_port: int = 10009,
    ssh_user: str = "ubuntu",
    ssh_port: int = 22,
    use_node: bool = True,
):
    """
    SSH into the node, and figure things out.
    """
    connect_kwargs = {}
    if ssh_cert_path:
        connect_kwargs["key_filename"] = ssh_cert_path
    elif ssh_password:
        connect_kwargs["password"] = ssh_password
    with Connection(
        hostname, connect_kwargs=connect_kwargs, user=ssh_user, port=ssh_port
    ) as con:
        print(chalk().magenta("ssh session connected!"))
        try:
            print(
                chalk().green(f'OS:       {con.run("uname", hide=True).stdout.strip()}')
            )
            print(
                chalk().green(
                    f'Hostname: {con.run("hostname", hide=True).stdout.strip()}'
                )
            )
        except:
            pass

        with TemporaryDirectory() as d:
            d = Path(d)
            tmp_ln_cert_path = d / Path(ln_cert_path).name
            tmp_ln_macaroon_path = d / Path(ln_macaroon_path).name
            print(chalk().cyan(f"Securely copying: {ln_cert_path}"))
            con.get(
                f"{ln_cert_path}",
                tmp_ln_cert_path.as_posix(),
            )
            print(chalk().cyan(f"Securely copying: {ln_macaroon_path}"))
            con.get(
                f"{ln_macaroon_path}",
                tmp_ln_macaroon_path.as_posix(),
            )

            print(chalk().cyan(f"Encrypting: {tmp_ln_cert_path}"))
            print(chalk().cyan(f"Encrypting: {tmp_ln_macaroon_path}"))

            with tmp_ln_macaroon_path.open("rb") as f:
                mac_hex = codecs.encode(f.read(), "hex")
            with tmp_ln_cert_path.open("r") as f:
                cert_plain = f.read()
            from orb.ln import Ln

            create(
                c,
                hostname=hostname,
                mac_hex=mac_hex,
                node_type=node_type,
                protocol=protocol,
                network=network,
                cert_plain=cert_plain,
                rest_port=rest_port,
                grpc_port=grpc_port,
                use_node=use_node,
            )

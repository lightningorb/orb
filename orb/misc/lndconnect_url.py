# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-15 10:47:00
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-18 15:25:16

from urllib.parse import urlparse
from urllib.parse import parse_qs
import base64


def decode_cert(cert):
    decoded_url = base64.urlsafe_b64decode(cert.strip().encode())
    decoded = base64.b64encode(decoded_url).decode()
    header = "-----BEGIN CERTIFICATE-----"
    footer = "-----END CERTIFICATE-----"
    cert = "\n".join(
        [
            header,
            "\n".join(decoded[i : i + 64] for i in range(0, len(decoded), 64)),
            footer,
        ]
    )

    return cert


def decode_mac(mac):
    decoded_url = base64.urlsafe_b64decode(mac.encode() + b"==")
    return decoded_url
    # return base64.b64encode(decoded_url).decode()


def decode_ln_url(url):
    res = urlparse(url)
    q = parse_qs(res.query)
    host, cert, mac = (
        res.hostname,
        next(iter(q["cert"]), None),
        next(iter(q["macaroon"]), None),
    )

    mac, cert = decode_mac(mac), decode_cert(cert)
    return host, cert, mac

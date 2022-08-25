# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-18 12:10:52
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-24 11:21:25


from bech32 import bech32_decode, convertbits
from typing import List, Set, Tuple
import requests


def _bech32_decode(
    bech32: str, *, allowed_hrp: Set[str] = None
) -> Tuple[str, List[int]]:
    hrp, data = bech32_decode(bech32)

    if not hrp or not data or (allowed_hrp and hrp not in allowed_hrp):
        raise ValueError(f"Invalid data or Human Readable Prefix (HRP): {hrp}.")

    return hrp, data


def _lnurl_clean(lnurl: str) -> str:
    return (
        lnurl.strip().replace("lightning:", "")
        if lnurl.startswith("lightning:")
        else lnurl
    )


def _lnurl_decode(lnurl: str) -> str:
    return bytes(
        convertbits(
            _bech32_decode(_lnurl_clean(lnurl), allowed_hrp={"lnurl"})[1], 5, 8, False
        )
    ).decode("utf-8")


def get_callback_url(amount, url):
    if "@" in url:
        user, domain = url.split("@")
        response = requests.get(f"https://{domain}/.well-known/lnurlp/{user}")
    else:
        lnurl = _lnurl_decode(url)
        response = requests.get(lnurl)
    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        raise Exception("Something bad")
    req = response.json()
    return f"{req['callback']}?amount={amount*1000}"


def get_invoice(lnurl, amount):
    rurl = get_callback_url(amount, url=lnurl)
    req = requests.get(rurl)
    if req.status_code == 200:
        resp = req.json()
        if "pr" in resp:
            line = resp["pr"]
            return line
        else:
            print(resp)
    else:
        print(req.text)

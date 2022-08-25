# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-23 09:57:46
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-23 10:07:41

from unittest import TestCase, main
from orb.ln.types import HTLC
from orb.misc.auto_obj import dict2obj

f1 = {
    "forward_event": {
        "payment_hash": "10afbb3b440068bfa3e2b0c5f3bdd42f2b913c736789e21d979328b2367110c7",
        "in_channel": "749662x1463x3",
        "out_channel": "749669x2018x8",
        "in_msatoshi": 689554963,
        "in_msat": "689554963msat",
        "out_msatoshi": 689547068,
        "out_msat": "689547068msat",
        "fee": 7895,
        "fee_msat": "7895msat",
        "status": "offered",
        "style": "tlv",
        "received_time": 1661218921.231,
    }
}
f2 = {
    "forward_event": {
        "payment_hash": "10afbb3b440068bfa3e2b0c5f3bdd42f2b913c736789e21d979328b2367110c7",
        "in_channel": "749662x1463x3",
        "out_channel": "749669x2018x8",
        "in_msatoshi": 689554963,
        "in_msat": "689554963msat",
        "out_msatoshi": 689547068,
        "out_msat": "689547068msat",
        "fee": 7895,
        "fee_msat": "7895msat",
        "status": "failed",
        "style": "tlv",
        "received_time": 1661218921.231,
        "resolved_time": 1661218924.423,
    }
}


class TestHTLC(TestCase):
    def test_htlc(self):
        h1 = HTLC("cln", dict2obj(f1))
        print(h1)
        # h2 = HTLC("cln", dict2obj(f2))


if __name__ == "__main__":
    main()

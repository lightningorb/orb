# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-02-20 10:19:07
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-20 11:56:29


import unittest
from orb.misc.auto_obj import *


class TestAutoObj(unittest.TestCase):
    def test_autoobj(self):
        self.maxDiff = 1000000
        gobj = to_num(sort_dict(grpc))
        robj = to_num(sort_dict(rest))
        self.assertDictEqual(gobj, robj)


grpc = {
    "creation_date": "1631710649",
    "creation_time_ns": "1631710649545190528",
    "failure_reason": "FAILURE_REASON_NONE",
    "fee": "0",
    "fee_msat": "0",
    "fee_sat": "0",
    "htlcs": [
        {
            "attempt_id": "1",
            "attempt_time_ns": "1631710649568966914",
            "preimage": "zaHMy1N53OMQmPhQ/lX/4fP3vTpoe7ZGIpV6wm88vwM=",
            "resolve_time_ns": "1631710650879874955",
            "route": {
                "hops": [
                    {
                        "amt_to_forward": "1000000",
                        "amt_to_forward_msat": "1000000000",
                        "chan_capacity": "10000000",
                        "chan_id": "770369523584794633",
                        "custom_records": {},
                        "expiry": 700698,
                        "fee": "0",
                        "fee_msat": "0",
                        "mpp_record": {
                            "payment_addr": "DiqL70lVKCBy8NaipBGVJ6wQzeWBjA/8TZ93hkQVt+k=",
                            "total_amt_msat": "1000000000",
                        },
                        "pub_key": "035e4ff418fc8b5554c5d9eea66396c227bd429a3251c8cbc711002ba215bfc226",
                        "tlv_payload": True,
                    }
                ],
                "total_amt": "1000000",
                "total_amt_msat": "1000000000",
                "total_fees": "0",
                "total_fees_msat": "0",
                "total_time_lock": 700698,
            },
            "status": "SUCCEEDED",
        }
    ],
    "payment_hash": "fdbda30b6454169ea3bdeee1341be193432b40886e52b2350b7c404bcca304e2",
    "payment_index": "1",
    "payment_preimage": "cda1cccb5379dce31098f850fe55ffe1f3f7bd3a687bb64622957ac26f3cbf03",
    "payment_request": "",
    "status": "SUCCEEDED",
    "value": "1000000",
    "value_msat": "1000000000",
    "value_sat": "1000000",
}


rest = {
    "creation_date": 1631710649,
    "creation_time_ns": 1631710649545190528,
    "failure_reason": "FAILURE_REASON_NONE",
    "fee": 0,
    "fee_msat": 0,
    "fee_sat": 0,
    "htlcs": [
        {
            "attempt_id": 1,
            "attempt_time_ns": 1631710649568966914,
            # "failure": None,
            "preimage": "zaHMy1N53OMQmPhQ/lX/4fP3vTpoe7ZGIpV6wm88vwM=",
            "resolve_time_ns": 1631710650879874955,
            "route": {
                "hops": [
                    {
                        # "amp_record": None,
                        "amt_to_forward": 1000000,
                        "amt_to_forward_msat": 1000000000,
                        "chan_capacity": 10000000,
                        "chan_id": 770369523584794633,
                        "custom_records": {},
                        "expiry": 700698,
                        "fee": 0,
                        "fee_msat": 0,
                        "mpp_record": {
                            "payment_addr": "DiqL70lVKCBy8NaipBGVJ6wQzeWBjA/8TZ93hkQVt+k=",
                            "total_amt_msat": 1000000000,
                        },
                        "pub_key": "035e4ff418fc8b5554c5d9eea66396c227bd429a3251c8cbc711002ba215bfc226",
                        "tlv_payload": True,
                    }
                ],
                "total_amt": 1000000,
                "total_amt_msat": 1000000000,
                "total_fees": 0,
                "total_fees_msat": 0,
                "total_time_lock": 700698,
            },
            "status": "SUCCEEDED",
        }
    ],
    "payment_hash": "fdbda30b6454169ea3bdeee1341be193432b40886e52b2350b7c404bcca304e2",
    "payment_index": 1,
    "payment_preimage": "cda1cccb5379dce31098f850fe55ffe1f3f7bd3a687bb64622957ac26f3cbf03",
    "payment_request": "",
    "status": "SUCCEEDED",
    "value": 1000000,
    "value_msat": 1000000000,
    "value_sat": 1000000,
}


if __name__ == "__main__":
    unittest.main()

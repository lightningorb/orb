# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-08 10:18:11
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-24 10:55:06

import unittest
import requests
from orb.logic.lnurl import get_callback_url


class TestLNURL(unittest.TestCase):
    def test_lnurl(self):
        lnurl = get_callback_url(
            amount=1,
            # url="user@domain.com", # this works too
            url="LNURL1DP68GURN8GHJ7AMPD3KX2AR0VEEKZAR0WD5XJTNRDAKJ7TNHV4KXCTTTDEHHWM30D3H82UNVWQHHVCTVD9J8QCTJV4H8GV3CMHGV0A",
        )
        req = requests.get(lnurl).json()
        self.assertTrue("lnbc" in req["pr"])


if __name__ == "__main__":
    unittest.main()

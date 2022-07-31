# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-08 10:18:11
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-31 10:43:23

import unittest
import requests
from lnurl import Lnurl, LnurlResponse


class TestLNURL(unittest.TestCase):
    def test_lnurl(self):
        lnurl = Lnurl("")
        req = requests.get(lnurl.url).json()
        res = LnurlResponse.from_dict(req)
        rurl = f"{res.callback}?amount={1000*1000}"
        req = requests.get(rurl)
        self.assertTrue("lnbc", req.json()["pr"])


if __name__ == "__main__":
    unittest.main()

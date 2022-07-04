# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-08 10:18:11
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-29 07:21:20

import unittest
from orb.misc.lndconnect_url import decode_ln_url

rest_local = "lndconnect://umbrel.local:8080}?cert=MIICJDCCAcqgAwIBAgIQUQt7h7UKVmGwTTA6JzPZejAKBggqhkjOPQQDAjA4MR8wHQYDVQQKExZsbmQgYXV0b2dlbmVyYXRlZCBjZXJ0MRUwEwYDVQQDEwx1bWJyZWwubG9jYWwwHhcNMjIwNjE3MDMwODA0WhcNMjMwODEyMDMwODA0WjA4MR8wHQYDVQQKExZsbmQgYXV0b2dlbmVyYXRlZCBjZXJ0MRUwEwYDVQQDEwx1bWJyZWwubG9jYWwwWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAASxLTJ7jdcrWRG4vsvdIwJ4YTEa5haBV_FNEAq4wYvOMAmIhhfQn5JXeUTvwjUM_9RH7SXFLuJ_FqxV_yfG1lOLo4G1MIGyMA4GA1UdDwEB_wQEAwICpDATBgNVHSUEDDAKBggrBgEFBQcDATAPBgNVHRMBAf8EBTADAQH_MB0GA1UdDgQWBBRlPQnCuoD9AkCQhGWPzzwsFZo00DBbBgNVHREEVDBSgglsb2NhbGhvc3SCDHVtYnJlbC5sb2NhbIIEdW5peIIKdW5peHBhY2tldIIHYnVmY29ubocEfwAAAYcQAAAAAAAAAAAAAAAAAAAAAYcEChUVCTAKBggqhkjOPQQDAgNIADBFAiB89XN7WZ04thOCihGIf_RlaHnVVwZIcojI-kfFQ6fRNgIhAIV9V4Zap7UoPCb0KTcmIUMgqidDNHEMBy0HgEY5Gap-&macaroon=AgEDbG5kAvgBAwoQ3Sem4wrE-gyrYbeBpGtD1xIBMBoWCgdhZGRyZXNzEgRyZWFkEgV3cml0ZRoTCgRpbmZvEgRyZWFkEgV3cml0ZRoXCghpbnZvaWNlcxIEcmVhZBIFd3JpdGUaIQoIbWFjYXJvb24SCGdlbmVyYXRlEgRyZWFkEgV3cml0ZRoWCgdtZXNzYWdlEgRyZWFkEgV3cml0ZRoXCghvZmZjaGFpbhIEcmVhZBIFd3JpdGUaFgoHb25jaGFpbhIEcmVhZBIFd3JpdGUaFAoFcGVlcnMSBHJlYWQSBXdyaXRlGhgKBnNpZ25lchIIZ2VuZXJhdGUSBHJlYWQAAAYguVd_y7eoBzLgOsnr-GwDZQHccap8WSkKHc3keli7ngo"
_cert = """-----BEGIN CERTIFICATE-----
MIICJDCCAcqgAwIBAgIQUQt7h7UKVmGwTTA6JzPZejAKBggqhkjOPQQDAjA4MR8w
HQYDVQQKExZsbmQgYXV0b2dlbmVyYXRlZCBjZXJ0MRUwEwYDVQQDEwx1bWJyZWwu
bG9jYWwwHhcNMjIwNjE3MDMwODA0WhcNMjMwODEyMDMwODA0WjA4MR8wHQYDVQQK
ExZsbmQgYXV0b2dlbmVyYXRlZCBjZXJ0MRUwEwYDVQQDEwx1bWJyZWwubG9jYWww
WTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAASxLTJ7jdcrWRG4vsvdIwJ4YTEa5haB
V/FNEAq4wYvOMAmIhhfQn5JXeUTvwjUM/9RH7SXFLuJ/FqxV/yfG1lOLo4G1MIGy
MA4GA1UdDwEB/wQEAwICpDATBgNVHSUEDDAKBggrBgEFBQcDATAPBgNVHRMBAf8E
BTADAQH/MB0GA1UdDgQWBBRlPQnCuoD9AkCQhGWPzzwsFZo00DBbBgNVHREEVDBS
gglsb2NhbGhvc3SCDHVtYnJlbC5sb2NhbIIEdW5peIIKdW5peHBhY2tldIIHYnVm
Y29ubocEfwAAAYcQAAAAAAAAAAAAAAAAAAAAAYcEChUVCTAKBggqhkjOPQQDAgNI
ADBFAiB89XN7WZ04thOCihGIf/RlaHnVVwZIcojI+kfFQ6fRNgIhAIV9V4Zap7Uo
PCb0KTcmIUMgqidDNHEMBy0HgEY5Gap+
-----END CERTIFICATE-----"""

_mac = b"\x02\x01\x03lnd\x02\xf8\x01\x03\n\x10\xdd'\xa6\xe3\n\xc4\xfa\x0c\xaba\xb7\x81\xa4kC\xd7\x12\x010\x1a\x16\n\x07address\x12\x04read\x12\x05write\x1a\x13\n\x04info\x12\x04read\x12\x05write\x1a\x17\n\x08invoices\x12\x04read\x12\x05write\x1a!\n\x08macaroon\x12\x08generate\x12\x04read\x12\x05write\x1a\x16\n\x07message\x12\x04read\x12\x05write\x1a\x17\n\x08offchain\x12\x04read\x12\x05write\x1a\x16\n\x07onchain\x12\x04read\x12\x05write\x1a\x14\n\x05peers\x12\x04read\x12\x05write\x1a\x18\n\x06signer\x12\x08generate\x12\x04read\x00\x00\x06 \xb9W\x7f\xcb\xb7\xa8\x072\xe0:\xc9\xeb\xf8l\x03e\x01\xdcq\xaa|Y)\n\x1d\xcd\xe4zX\xbb\x9e\n"


class TestLNDConnectURL(unittest.TestCase):
    def test_lndconnect_url(self):
        host, port, cert, mac = decode_ln_url(rest_local)
        self.assertEqual(host, "umbrel.local")
        self.assertEqual(port, 8080)
        self.assertEqual(cert, _cert)
        self.assertEqual(mac, _mac)


if __name__ == "__main__":
    unittest.main()

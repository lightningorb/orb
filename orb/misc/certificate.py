# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-09 08:41:00
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-09 10:41:51

import re
import base64


class Certificate:
    def __init__(self):
        self.cert = ""
        self.first_line = "-----BEGIN CERTIFICATE-----"
        self.last_line = "-----END CERTIFICATE-----"

    @staticmethod
    def init_from_str(text):
        cert = Certificate()
        cert.cert = text
        return cert

    @staticmethod
    def init_from_not_sure(text):
        if Certificate.is_base64_cert_str(text):
            return Certificate.init_from_base64(text)
        else:
            cert = Certificate()
            cert.cert = text
            return cert

    @staticmethod
    def init_from_base64(text):
        b64 = base64.b64decode(text.strip().encode()).decode()
        return Certificate.init_from_str(b64)

    @staticmethod
    def is_base64_cert_str(text):
        try:
            b64 = base64.b64decode(text.strip().encode()).decode()
            cert = Certificate.init_from_str(b64)
            return cert.is_well_formed()
        except:
            return False

    def is_well_formed(self):
        return self.debug() == "Certificate correctly formatted"

    def reformat(self):
        if not self.is_well_formed():
            raise Exception("Certificate is badly formatted")
        lines = [x.strip() for x in self.cert.split("\n") if x]
        formatted = [self.first_line] + lines[1:13] + [self.last_line]
        self.cert = "\n".join(formatted)
        return self.cert

    def debug(self):
        cert = self.cert
        lines = [x.strip() for x in cert.split("\n") if x]
        if len(lines) != 14:
            return f"Certificate length is {len(lines)}. It should be 14 lines long"
        if not re.search(self.first_line, lines[0]):
            return f"First line should be {self.first_line}"
        if not re.search(self.last_line, lines[13]):
            return f"Last line should be {self.last_line}"
        for i, line in enumerate(lines[1:12], 1):
            if len(line) != 64:
                return f"line {i} length is {len(line)}. Needs to be 64 characters long"
        line = lines[12]
        if len(line) != 8:
            return f"line 12 length is {len(line)}. Needs to be 8 characters long"
        return "Certificate correctly formatted"

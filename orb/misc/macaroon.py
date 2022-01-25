# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-09 08:41:00
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-25 16:43:54

import re
import base64
import codecs


class Macaroon:
    def __init__(self):
        self.macaroon = ""

    @staticmethod
    def init_from_plain(text):
        macaroon = Macaroon()
        macaroon.macaroon = text
        return macaroon

    @staticmethod
    def init_from_str(text):
        macaroon = Macaroon()
        macaroon.macaroon = text.strip()
        return macaroon

    @staticmethod
    def init_from_not_sure(text):
        if Macaroon.is_base64_macaroon_str(text):
            return Macaroon.init_from_base64(text)
        else:
            macaroon = Macaroon()
            macaroon.macaroon = text
            return macaroon

    @staticmethod
    def init_from_base64(text):
        b64 = base64.b64decode(text.strip().encode()).decode()
        return Macaroon.init_from_str(b64)

    @staticmethod
    def is_base64_macaroon_str(text):
        try:
            b64 = base64.b64decode(text.strip().encode()).decode()
            macaroon = Macaroon.init_from_str(b64)
            return macaroon.is_well_formed()
        except:
            return False

    def is_well_formed(self):
        if type(self.macaroon) is str:
            return bool(re.match(r"^([a-z]|[A-Z]|[0-9])+$", self.macaroon))
        else:
            return bool(re.match(r"^([a-z]|[A-Z]|[0-9])+$", self.macaroon.decode()))

    def debug(self):
        return (
            "Macaroon correctly formatted"
            if self.is_well_formed()
            else "Macaroon looks invalid"
        )

    def as_base64(self):
        return codecs.encode(self.macaroon, "hex").decode()

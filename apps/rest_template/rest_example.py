# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 20:28:57
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-20 10:08:10

from pathlib import Path
from orb.misc.utils import pref as p
from orb.misc.prefs import cert_path
import base64, codecs, json, requests
import os
import json

from orb.misc.plugin import Plugin


class RestExample(Plugin):
    def main(self):
        url = f"https://{p('host.hostname')}:{p('ln.rest_port')}/v1/channels"
        headers = {"Grpc-Metadata-macaroon": p("ln.macaroon_admin").encode()}
        r = requests.get(url, headers=headers, verify=cert_path())
        print(json.dumps(r.json(), indent=4))

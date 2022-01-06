# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 20:28:57
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-06 20:29:06

import base64, codecs, json, requests
from kivy.app import App
import os
import json


def main():
    app = App.get_running_app()
    data_dir = app.user_data_dir
    cert_path = os.path.join(data_dir, "tls.cert")
    hostname = app.config["lnd"]["hostname"]
    rest_port = app.config["lnd"]["rest_port"]
    macaroon = app.config["lnd"]["macaroon_admin"]
    url = f"https://{hostname}:{rest_port}/v1/channels"
    headers = {"Grpc-Metadata-macaroon": macaroon.encode()}
    r = requests.get(url, headers=headers, verify=cert_path)
    print(json.dumps(r.json(), indent=4))

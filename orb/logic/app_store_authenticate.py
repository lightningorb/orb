# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-19 03:47:33
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-21 07:58:28

import requests
import json
from orb.misc import data_manager
from orb.lnd import Lnd


def get_creds():
    return data_manager.data_man.store.get("auth", {})


def set_creds(creds):
    return data_manager.data_man.store.put("auth", **creds)


def authenticate():
    creds = get_creds()
    lnd = Lnd()
    print("getting identity")
    username = lnd.get_info().identity_pubkey
    print("signing password")
    password = lnd.sign_message("orb_password")
    # if we have creds then return
    if False:
        return creds
    else:
        # first try logging in
        r = requests.post(
            "https://lnappstore.com/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=f"grant_type=&username={username}&password={password}&scope=&client_id=&client_secret=",
        )
        resp = r.json()
        if r.status_code == 200 and "access_token" in resp:
            set_creds(
                {
                    "username": resp["username"],
                    "access_token": resp["access_token"],
                    "user_id": resp["user_id"],
                }
            )
            print("login successful")
        if r.status_code == 401 and resp.get("detail") == "User does not exist":
            print("user does not exist - creating")
            resp = requests.post(
                "https://lnappstore.com/api/auth/users/register/",
                data=json.dumps({"username": username, "password": password}),
            ).json()
            print("storing auth token")
            set_creds(
                {
                    "username": resp["username"],
                    "access_token": resp["access_token"],
                    "user_id": resp["user_id"],
                }
            )
            print("registration successful")

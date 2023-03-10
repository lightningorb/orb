# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-19 03:47:33
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-07 14:01:57

import requests
import json

from kivy.app import App


from orb.ln import Ln
from orb.misc.utils import pref


def get_creds():
    return App.get_running_app().store.get("auth", {})


def set_creds(resp):
    return App.get_running_app().store.put(
        "auth",
        **{
            "username": resp["username"],
            "access_token": resp["access_token"],
            "user_id": resp["user_id"],
        },
    )


def clear_creds(creds):
    return App.get_running_app().store.put("auth", {})


def register(username, password):
    print("user does not exist - creating")
    resp = requests.post(
        f"{pref('url.appstore')}/api/auth/users/register/",
        data=json.dumps({"username": username, "password": password}),
    ).json()
    print("registration response:")
    print(resp)
    if "detail" in resp:
        print("Already registerd!")
    else:
        print("storing auth token")
        set_creds(resp)
        print("registration successful")
        return resp


def login(username, password):
    r = requests.post(
        f"{pref('url.appstore')}/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=f"grant_type=&username={username}&password={password}&scope=&client_id=&client_secret=",
    )
    resp = r.json()
    print("Login request response:")
    print(resp)
    set_creds(resp)
    return resp


def get_password():
    return Ln().sign_message("orb_password")

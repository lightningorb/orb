# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-19 14:20:57
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-22 13:21:59

import re
import requests

from orb.logic.app_store_authenticate import get_creds
from orb.misc.auto_obj import dict2obj
from orb.misc.utils import pref_path, pref


class API:
    def __init__(self):
        self.fqdn = pref("url.appstore")

    @property
    def __headers(self):
        creds = get_creds()
        if not creds.get("access_token"):
            print("no access token available")
            return {}
        else:
            return {
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(creds.get("access_token")),
            }

    def download(self, uuid):
        r = requests.get(f"{self.fqdn}/api/app/?uuid={uuid}", headers=self.__headers)
        d = r.headers["content-disposition"]
        fname = re.findall('filename="(.+)"', d)[0]
        path = pref_path("download") / fname
        with open(path.as_posix(), "wb") as f:
            f.write(r.content)
            return path

    def list_apps(self):
        return dict2obj({"apps": self.__get(f"/api/app/list", auto_obj=False)})

    def delete_from_store(self, uuid):
        ret = self.__post(f"/api/app/delete/?uuid={uuid}")
        print(ret)

    def upload(self, file_path):
        headers = self.__headers
        del headers["Content-Type"]
        r = requests.post(
            f"{self.fqdn}/api/app/",
            files={"file": open(file_path, "rb")},
            headers=headers,
        )
        if r.status_code == 200:
            return dict2obj(r.json())

    def get_icon_path(self, uuid):
        return f"{pref('url.appstore')}/api/app/icon?uuid={uuid}"

    def __get(self, url, auto_obj=True):
        r = requests.get(f"{self.fqdn}{url}", headers=self.__headers)
        if auto_obj:
            return dict2obj(r.json())
        else:
            return r.json()

    def __post(self, url, data=None):
        r = requests.post(f"{self.fqdn}{url}", data=data, headers=self.__headers)
        return dict2obj(r.json())

    def __delete(self, url, data):
        r = requests.delete(f"{self.fqdn}{url}", data=data, headers=self.__headers)
        return dict2obj(r.json())

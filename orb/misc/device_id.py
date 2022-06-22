# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-23 03:05:02
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-23 03:06:45

import plyer
import uuid

from orb.misc.utils import pref


def device_id():
    try:
        if pref("system.identifier") == "uuid":
            uid = uuid.getnode()
        elif pref("system.identifier") == "plyer":
            uid = plyer.uniqueid.id
        else:
            uid = 0
    except Exception as e:
        print(e)
        print("WARNING: plyer.uniqueid.id failed - setting uid to 0")
        uid = 0
    return uid

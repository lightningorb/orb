# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-23 03:05:02
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-30 18:56:58

import plyer
import uuid


def device_id():
    try:
        uid = plyer.uniqueid.id
    except Exception as e:
        print(e)
        print("WARNING: plyer.uniqueid.id failed - setting uid to 0")
        uid = 0
    if type(uid) is str:
        uid = uid.encode()
    return uid

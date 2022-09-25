# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-23 03:05:02
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-25 13:03:08

import plyer
import uuid
import os


def device_id():
    try:
        uid = plyer.uniqueid.id
    except Exception as e:
        if not (
            os.environ.get("ORB_INTEGRATION_TESTS")
            or os.environ.get("ORB_NO_DEVICE_ID_WARNING")
        ):
            print(e)
            print("WARNING: plyer.uniqueid.id failed - setting uid to 0")
        uid = b"0"
    if type(uid) is str:
        uid = uid.encode()
    return uid

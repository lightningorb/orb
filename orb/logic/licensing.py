# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-02-15 13:04:42
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-15 15:52:09

import arrow


def get_code():
    try:
        from pytransform import get_license_info
    except:
        return "satoshi"
    return get_license_info()["CODE"]


get_days_left = lambda: (
    arrow.get(get_license_info()["EXPIRED"], "MMM DD HH:mm:ss YYYY") - arrow.utcnow()
).days
is_valid = lambda: get_days_left() > 0
is_registered = lambda: False  # TODO
is_trial = lambda: "eval" in get_code()
is_satoshi = lambda: "satoshi" in get_code()
is_digital_gold = lambda: get_code() == "digital-gold"
get_edition = lambda: "satoshi" if is_satoshi() else "digital-gold"

# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-24 08:28:49
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-31 05:44:24

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.decorators import guarded
from orb.lnd import Lnd


class ConnectScreen(PopupDropShadow):
    @guarded
    def connect(self, address):
        res = Lnd().connect(address)
        print(res)

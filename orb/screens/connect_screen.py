# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-24 08:28:49
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-17 07:23:59

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.decorators import guarded
from orb.lnd import Lnd


class ConnectScreen(PopupDropShadow):
    @guarded
    def connect(self, address):
        """
        Lnd().connect(address) gives an error in REST.. strangely
        it connects successfully, and the error can be ignored.
        """
        return Lnd().connect(address)

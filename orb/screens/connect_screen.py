# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-24 08:28:49
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-08 10:44:28

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.decorators import guarded
from orb.ln import Ln


class ConnectScreen(PopupDropShadow):
    @guarded
    def connect(self, address):
        """
        Lnd().connect(address) gives an error in REST.. strangely
        it connects successfully, and the error can be ignored.
        """
        ret = Ln().connect(address)
        print(ret)

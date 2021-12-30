# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-31 05:43:03

from kivy.uix.popup import Popup

from orb.misc.decorators import guarded
from orb.lnd import Lnd


class CloseChannel(Popup):
    @guarded
    def close_channel(self, channel_point, sats_per_vbyte):
        result = Lnd().close_channel(
            channel_point=channel_point, force=False, sat_per_vbyte=int(sats_per_vbyte)
        )
        print(result)

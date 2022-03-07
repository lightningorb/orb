# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-03-05 12:17:44

from threading import Thread
from orb.core.stoppable_thread import StoppableThread

from kivy.uix.popup import Popup

from orb.misc.decorators import guarded
from orb.lnd import Lnd


class CloseChannel(Popup):
    @guarded
    def close_channel(self, channel_point, sats_per_vbyte):
        def func():
            print(f"Closing: {channel_point}")
            result = Lnd().close_channel(
                channel_point=channel_point,
                force=self.ids.force.active,
                sat_per_vbyte=int(sats_per_vbyte),
            )
            for response in result:
                print(response)

        StoppableThread(target=func).start()

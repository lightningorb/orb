# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-08 08:12:28

from threading import Thread
from orb.core.stoppable_thread import StoppableThread

from kivy.uix.popup import Popup

from orb.misc.decorators import guarded
from orb.misc.utils import pref
from orb.ln import Ln


class CloseChannel:
    def __init__(self):
        self.impl = dict(cln=CLNCloseChannel, lnd=LNDCloseChannel)[pref("host.type")]()

    def open(self):
        self.impl.open()


class CLNCloseChannel(Popup):
    @guarded
    def close_channel(self, id: str, unilateral_timeout: str, dest: str):
        def func():
            print(f"Closing: {id}")
            result = Ln().close_channel(
                id=id,
                unilateral_timeout=int(unilateral_timeout),
                dest=dest,
            )
            print(result)
            print("done")

        StoppableThread(target=func).start()


class LNDCloseChannel(Popup):
    @guarded
    def close_channel(self, channel_point: str, sats_per_vbyte: str):
        def func():
            print(
                f"Closing: {channel_point}, force: {self.ids.force.active}, sats v/b: {int(sats_per_vbyte)}"
            )
            result = Ln().close_channel(
                channel_point=channel_point,
                force=self.ids.force.active,
                sat_per_vbyte=int(sats_per_vbyte),
            )
            for response in result:
                print(response)

        StoppableThread(target=func).start()

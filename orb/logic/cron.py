# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-02 13:04:10


from orb.misc.utils_no_kivy import pref
from orb.core.stoppable_thread import StoppableThread

import time


class Cron:
    def __init__(self, *_, **__):
        from kivy.clock import Clock

        from orb.logic.forwarding_history import DownloadFowardingHistory
        DownloadFowardingHistory().start()

        from orb.logic.payment_history import DownloadPaymentHistory
        DownloadPaymentHistory().start()

        if Clock:

            def udpate_channels(*_):
                from orb.app import App

                app = App.get_running_app()
                if app:
                    cs = app.main_layout.ids.sm.get_screen("channels")
                    if cs:
                        cw = cs.channels_widget
                        if cw:
                            cw.update()

            Clock.schedule_interval(
                udpate_channels,
                10,
            )

        # TODO: needs tying up

        if pref("host.type") == "cln":

            class UpdateChannels(StoppableThread):
                def run(self):
                    while not self.stopped():
                        from orb.app import App

                        def do_update():
                            app = App.get_running_app()
                            if app.channels:
                                app.channels.get()
                                app.channels.compute_balanced_ratios()
                                if hasattr(app, "update_channels_widget"):
                                    app.update_channels_widget += 1

                        do_update()

                        timer = 10
                        while timer and not self.stopped():
                            timer -= 1
                            time.sleep(1)

            UpdateChannels().start()

            return

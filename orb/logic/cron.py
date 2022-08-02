# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-01 19:05:46

from orb.logic.forwarding_history import download_forwarding_history
from orb.logic.payment_history import download_payment_history
from orb.logic.licensing import is_registered

from kivy.clock import Clock
from kivy.app import App


class Cron:
    def __init__(self, *args, **kwargs):
        if Clock:
            Clock.schedule_once(download_forwarding_history, 30)
            Clock.schedule_interval(download_forwarding_history, 60)
            Clock.schedule_once(download_payment_history, 5)
            Clock.schedule_interval(download_payment_history, 60)
            Clock.schedule_interval(
                lambda _: App.get_running_app()
                .main_layout.ids.sm.get_screen("channels")
                .channels_widget.update(),
                10,
            )
            # Clock.schedule_once(is_registered, 80)
            # Clock.schedule_interval(is_registered, 3600)

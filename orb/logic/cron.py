# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-05 05:26:39

from kivy.clock import Clock

from orb.dialogs.forwarding_history import download_forwarding_history


class Cron:
    def __init__(self, *args, **kwargs):
        if Clock:
            Clock.schedule_once(download_forwarding_history, 30)
            Clock.schedule_interval(download_forwarding_history, 10 * 60)


cron = Cron()

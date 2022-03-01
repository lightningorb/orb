# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-03-01 10:06:55

from kivy.clock import Clock

from orb.logic.forwarding_history import download_forwarding_history
from orb.logic.payment_history import download_payment_history

from orb.logic.licensing import is_registered


class Cron:
    def __init__(self, *args, **kwargs):
        if Clock:
            Clock.schedule_once(download_forwarding_history, 30)
            Clock.schedule_interval(download_forwarding_history, 60)
            Clock.schedule_once(download_payment_history, 5)
            Clock.schedule_interval(download_payment_history, 60)
            Clock.schedule_once(is_registered, 80)
            Clock.schedule_interval(is_registered, 3600)


cron = Cron()

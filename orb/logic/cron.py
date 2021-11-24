from kivy.clock import Clock

from orb.dialogs.forwarding_history import download_forwarding_history


class Cron:
    def __init__(self, *args, **kwargs):
        Clock.schedule_once(download_forwarding_history, 30)
        Clock.schedule_interval(download_forwarding_history, 10 * 60)


cron = Cron()

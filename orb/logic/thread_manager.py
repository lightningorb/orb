# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-05 09:06:41

from kivy.clock import Clock
from kivy.properties import ListProperty
from kivy.event import EventDispatcher

from threading import Thread


class ThreadManager(EventDispatcher):
    """
    The ThreadManager is used to register Threads, and regularly check
    on whether they're still running.

    Use this class if you want your threads to be visible, and manageable
    from within the UI. Make sure to use the stoppable thread pattern.

    :py:module:`MyModule.constants`
    """

    threads = ListProperty([])

    def __init__(self, *args):
        if Clock:
            Clock.schedule_interval(
                lambda _: Thread(target=self.check_alive).start(), 1
            )

    def stop_threads(self):
        for t in self.threads:
            t.stop()
        self.threads.clear()

    def check_alive(self, *args):
        to_remove = []
        for t in self.threads:
            if t.stopped():
                to_remove.append(t)
        for t in to_remove:
            self.threads.remove(t)

    def add_thread(self, thread):
        self.threads.append(thread)


thread_manager = ThreadManager()

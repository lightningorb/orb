# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-27 11:42:51

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
        Clock.schedule_interval(lambda _: Thread(target=self.check_alive).start(), 1)

    def check_alive(self, *args):
        for t in self.threads:
            if t.stopped():
                self.threads.remove(t)
                return

    def add_thread(self, thread):
        self.threads.append(thread)


thread_manager = ThreadManager()

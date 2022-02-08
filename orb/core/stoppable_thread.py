# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:27:21
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-08 17:34:56

from threading import Thread, Event
from orb.logic.thread_manager import thread_manager
from abc import ABCMeta, abstractmethod


class StoppableThread(Thread):
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = Event()
        self.name = self.__class__.__name__
        thread_manager.add_thread(self)

    def run(self, *args):
        super(StoppableThread, self).run(*args)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:27:21
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-29 13:33:18

from threading import Thread, Event


class StoppableThread(Thread):
    def __init__(self, visible=True, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = Event()
        self.name = self.__class__.__name__
        self.visible = visible
        from orb.app import App, AppMode

        app = App.get_running_app()
        if app.mode == AppMode.ui:
            from orb.logic.thread_manager import thread_manager

            thread_manager.add_thread(self)
        elif app.mode == AppMode.cli:
            from orb.logic.cli_thread_manager import cli_thread_manager

            cli_thread_manager.add_thread(self)

    def run(self, *args):

        super(StoppableThread, self).run(*args)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class StoppableThreadHidden(StoppableThread):
    def __init__(self, *args, **kwargs):
        super(StoppableThreadHidden, self).__init__(visible=False, *args, **kwargs)

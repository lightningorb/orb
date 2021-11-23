from kivy.clock import Clock
from kivy.properties import ListProperty
from kivy.event import EventDispatcher

from threading import Thread


class ThreadManager(EventDispatcher):
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

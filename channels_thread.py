import threading
from time import sleep
from traceback import print_exc

import data_manager


class ChannelsThread(threading.Thread):
    def __init__(self, inst, *args, **kwargs):
        super(ChannelsThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.inst = inst

    def run(self):
        while not self.stopped():
            try:
                lnd = data_manager.data_man.lnd
                it = lnd.get_channel_events()
                if it:
                    for e in it:
                        if self.stopped():
                            return
                        print(e)
                        if e.open_channel:
                            self.inst.channels.append(e.open_channel)
            except:
                print("Exception getting Channels - let's sleep")
                print_exc()
                sleep(10)
            sleep(10)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

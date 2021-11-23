import threading
from time import sleep

import data_manager
from orb.logic.thread_manager import thread_manager


class ChannelsThread(threading.Thread):
    def __init__(self, inst, name, *args, **kwargs):
        super(ChannelsThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.inst = inst
        self.name = name
        thread_manager.add_thread(self)

    def run(self):
        try:
            self.__run()
        except:
            self.stop()

    def __run(self):
        while not self.stopped():
            try:
                lnd = data_manager.data_man.lnd
                it = lnd.get_channel_events()
                if it:
                    for e in it:
                        if self.stopped():
                            return
                        print(e)
                        # console_output(str(e))
                        if e.open_channel.chan_id:
                            self.inst.add_channel(e.open_channel)
                        if e.closed_channel.chan_id:
                            self.inst.remove_channel(e.open_channel)
            except:
                print("Exception getting Channels - let's sleep")
                # print_exc()
                sleep(10)
            sleep(10)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

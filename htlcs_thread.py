import threading
from time import sleep
from traceback import print_exc

import data_manager
from htlc import Htlc


class HTLCsThread(threading.Thread):
    def __init__(self, inst, *args, **kwargs):
        super(HTLCsThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.inst = inst

    def run(self):
        while not self.stopped():
            try:
                lnd = data_manager.data_man.lnd
                for e in lnd.get_htlc_events():
                    if self.stopped():
                        return
                    self.inst.update_rect()
                    for cid in self.inst.cn:
                        if self.inst.cn[cid].l.channel.chan_id in [
                            e.outgoing_channel_id,
                            e.incoming_channel_id,
                        ]:
                            self.inst.cn[cid].l.anim_htlc(Htlc(lnd, e))
            except:
                print("Exception getting HTLCs - let's sleep")
                print_exc()
                sleep(10)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

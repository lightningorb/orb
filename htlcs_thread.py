from munch import Munch
import json
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
                print("Getting HTLC events")
                it = lnd.get_htlc_events()
                # print("events it", it)
                # e = b'{"result":{"incoming_channel_id":"771459139617882112","outgoing_channel_id":"775187583469486081","incoming_htlc_id":"1443","outgoing_htlc_id":"45","timestamp_ns":"1634262356778094095","event_type":"FORWARD","forward_event":{"info":{"incoming_timelock":705279,"outgoing_timelock":705239,"incoming_amt_msat":"255398649","outgoing_amt_msat":"255142507"}}}}'
                # e = Munch.fromDict(json.loads(e)).result
                # h = Htlc(lnd, e)
                # print(h.__dict__)
                for e in it.iter_lines():
                    if self.stopped():
                        return
                    self.inst.update_rect()
                    e = json.loads(e)["result"]
                    print(e)
                    e = Munch.fromDict(e)
                    for cid in self.inst.cn:
                        chans = [
                            e.get("outgoing_channel_id"),
                            e.get("incoming_channel_id"),
                        ]
                        print(chans)
                        if self.inst.cn[cid].l.channel.chan_id in chans:
                            print("DOING ANIM")
                            self.inst.cn[cid].l.anim_htlc(Htlc(lnd, e))
            except:
                print("Exception getting HTLCs - let's sleep")
                print_exc()
                sleep(10)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

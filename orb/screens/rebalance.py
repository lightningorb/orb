from traceback import print_exc
import threading

from kivy.clock import mainthread

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.output import *
from orb.logic.pay_logic import pay_thread, PaymentStatus
from orb.logic.channel_selector import get_low_inbound_channel
from orb.logic.thread_manager import thread_manager
from orb.logic.channel_selector import get_low_outbound_channel
import data_manager


class Rebalance(PopupDropShadow):
    def __init__(self, **kwargs):
        PopupDropShadow.__init__(self, **kwargs)
        self.output = Output(None)
        self.output.lnd = data_manager.data_man.lnd
        self.lnd = data_manager.data_man.lnd
        self.chan_id = None
        self.last_hop_pubkey = None
        self.alias_to_pk = {}

        @mainthread
        def delayed():
            channels = data_manager.data_man.channels
            for c in channels:
                self.ids.spinner_out_id.values.append(
                    f"{c.chan_id}: {self.lnd.get_node_alias(c.remote_pubkey)}"
                )
                self.ids.spinner_in_id.values.append(
                    f"{self.lnd.get_node_alias(c.remote_pubkey)}"
                )
                self.alias_to_pk[
                    self.lnd.get_node_alias(c.remote_pubkey)
                ] = c.remote_pubkey

        delayed()

    def first_hop_spinner_click(self, chan):
        self.chan_id = int(chan.split(":")[0])

    def last_hop_spinner_click(self, alias):
        self.last_hop_pubkey = self.alias_to_pk[alias]
        print(f"Settting last hop pubkey to: {self.last_hop_pubkey}")

    def rebalance(self):
        class RebalanceThread(threading.Thread):
            def __init__(self, inst, name, thread_n, *args, **kwargs):
                super(RebalanceThread, self).__init__(*args, **kwargs)
                self._stop_event = threading.Event()
                self.name = name
                self.inst = inst
                self.thread_n = thread_n
                thread_manager.add_thread(self)

            def run(self):
                try:
                    self.__run()
                except:
                    print_exc()
                finally:
                    self.stop()

            def __run(self):
                amount = int(self.inst.ids.amount.text)

                if not self.inst.chan_id:
                    self.inst.chan_id = get_low_inbound_channel(
                        lnd=self.inst.lnd,
                        pk_ignore=[],
                        chan_ignore=[],
                        num_sats=amount,
                    )

                if self.inst.last_hop_pubkey:
                    print(f"Last hop pubkey is: {self.inst.last_hop_pubkey}")
                if not self.inst.last_hop_pubkey:
                    _, self.inst.last_hop_pubkey = get_low_outbound_channel(
                        lnd=self.inst.lnd,
                        pk_ignore=[],
                        chan_ignore=[],
                        num_sats=amount,
                    )
                    print(
                        f"Last hop pubkey not set, so selected one: {self.inst.last_hop_pubkey}"
                    )

                raw, payment_request = data_manager.data_man.lnd.generate_invoice(
                    memo="rebalance", amount=amount
                )
                status = pay_thread(
                    inst=self.inst,
                    stopped=self.stopped,
                    thread_n=0,
                    fee_rate=int(self.inst.ids.fee_rate.text),
                    payment_request=payment_request,
                    payment_request_raw=raw,
                    outgoing_chan_id=self.inst.chan_id,
                    last_hop_pubkey=self.inst.last_hop_pubkey,
                    max_paths=int(self.inst.ids.max_paths.text),
                )

                if not status == PaymentStatus.success:
                    try:
                        data_manager.data_man.lnd.cancel_invoice(
                            payment_request.payment_hash
                        )
                    except:
                        print("Exception while cancelling invoice")

            def stop(self):
                self._stop_event.set()

            def stopped(self):
                return self._stop_event.is_set()

        self.thread = RebalanceThread(inst=self, name="RebalanceThread", thread_n=0)
        self.thread.daemon = True
        self.thread.start()

    def kill(self):
        self.thread.stop()

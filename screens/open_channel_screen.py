from kivy.uix.screenmanager import Screen
import data_manager
from ui_actions import console_output
from traceback import format_exc


class OpenChannelScreen(Screen):
    def open_channel(self, pk, sats, sats_per_vbyte):
        try:
            result = data_manager.data_man.lnd.open_channel(
                node_pubkey_string=pk,
                sat_per_vbyte=int(sats_per_vbyte),
                amount_sat=int(sats),
            )
            console_output(result)
        except:
            console_output(format_exc())

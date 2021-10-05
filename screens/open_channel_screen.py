from kivy.uix.screenmanager import Screen
from data_manager import data_man


class OpenChannelScreen(Screen):
    def open_channel(self, pk, sats, sats_per_vbyte):
        result = data_man.lnd.open_channel(
            node_pubkey_string=pk,
            sat_per_vbyte=int(sats_per_vbyte),
            amount_sat=int(sats),
        )
        print(result)

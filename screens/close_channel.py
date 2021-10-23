from kivy.uix.popup import Popup
import data_manager
from ui_actions import console_output
from decorators import guarded

class CloseChannel(Popup):
    @guarded
    def close_channel(self, pk, sats, sats_per_vbyte):
        result = data_manager.data_man.lnd.close_channel(self, channel_point, force, sat_per_vbyte)
        console_output(result)

from kivy.uix.popup import Popup
import data_manager
from orb.misc.ui_actions import console_output
from orb.misc.decorators import guarded


class CloseChannel(Popup):
    @guarded
    def close_channel(self, channel_point, sats_per_vbyte):
        result = data_manager.data_man.lnd.close_channel(
            channel_point=channel_point, force=False, sat_per_vbyte=int(sats_per_vbyte)
        )
        console_output(result)

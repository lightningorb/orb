from popup_drop_shadow import PopupDropShadow
import data_manager
from ui_actions import console_output
from traceback import format_exc
from decorators import guarded

class OpenChannelScreen(PopupDropShadow):
    @guarded
    def open_channel(self, pk, sats, sats_per_vbyte):
        result = data_manager.data_man.lnd.open_channel(
            node_pubkey_string=pk,
            sat_per_vbyte=int(sats_per_vbyte),
            amount_sat=int(sats),
        )
        console_output(result)

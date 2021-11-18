from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.ui_actions import console_output
from orb.misc.decorators import guarded

import data_manager


class OpenChannelScreen(PopupDropShadow):
    @guarded
    def open_channel(self, pk, sats, sats_per_vbyte):
        result = data_manager.data_man.lnd.open_channel(
            node_pubkey_string=pk,
            sat_per_vbyte=int(sats_per_vbyte),
            amount_sat=int(sats),
        )
        console_output(result)

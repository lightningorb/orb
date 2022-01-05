# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-24 08:30:20
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-05 19:26:48

from kivy.config import Config
from kivy.core.window import Window
import sys
import os

sys.path.append(os.path.join("orb", "lnd"))
sys.path.append(os.path.join("orb", "lnd", "grpc_generated"))
sys.path.append(os.path.join("user", "scripts"))

Config.set("graphics", "window_state", "maximized")
Config.set("graphics", "fullscreen", "auto")

Window.maximize()

# Window.fullscreen = True

from orb.core_ui.orb_app import OrbApp

from orb.channels.channels_widget import ChannelsWidget
from orb.screens.close_channel import CloseChannel
from orb.screens.rebalance import Rebalance
from orb.screens.channels_screen import ChannelsScreen
from orb.screens.pay_screen import PayScreen
from orb.screens.mail_screen import MailScreen
from orb.screens.open_channel_screen import OpenChannelScreen
from orb.screens.connect_screen import ConnectScreen
from orb.screens.ingest_invoices_screen import IngestInvoicesScreen
from orb.screens.console.console_screen import ConsoleScreen
from orb.screens.player_screen import PlayerScreen
from orb.screens.send_coins import SendCoins
from orb.screens.about import About
from orb.screens.rankings import Rankings
from orb.widgets.HUD import HUD
from orb.dialogs.fee_spy import FeeSpy
from orb.attribute_editor.AE_fees import AEFees
from orb.lnd import Lnd

from orb.core_ui.main_layout import MainLayout
from orb.status_line.status_line import StatusLine
from orb.core_ui.top_menu import TopMenu
from orb.logic.cron import cron

keep = lambda _: _

keep(Lnd)
keep(ChannelsWidget)
keep(Rebalance)
keep(CloseChannel)
keep(Rebalance)
keep(ChannelsScreen)
keep(PayScreen)
keep(OpenChannelScreen)
keep(ConnectScreen)
keep(IngestInvoicesScreen)
keep(ConsoleScreen)
keep(PlayerScreen)
keep(SendCoins)
keep(About)
keep(Rankings)
keep(FeeSpy)
keep(MainLayout)
keep(StatusLine)
keep(TopMenu)
keep(HUD)
keep(MailScreen)
keep(AEFees)
keep(cron)

if __name__ == "__main__":
    OrbApp().run()

# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-24 08:30:20
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-28 06:49:13

from kivy.config import Config
import sys
import os

sys.path.append(os.path.join("orb", "lnd"))
sys.path.append(os.path.join("orb", "lnd", "grpc_generated"))
sys.path.append(os.path.join("user", "scripts"))

Config.set("graphics", "window_state", "maximized")

from orb.core_ui.orb_app import OrbApp

from orb.attribute_editor.attribute_editor import AttributeEditor
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
from orb.screens.send_coins import SendCoins
from orb.screens.about import About
from orb.screens.rankings import Rankings
from orb.widgets.HUD import HUD
from orb.dialogs.fee_spy import FeeSpy
from orb.attribute_editor.AE_fees import AEFees

from orb.core_ui.main_layout import MainLayout
from orb.status_line.status_line import StatusLine
from orb.core_ui.top_menu import TopMenu
from orb.logic.cron import cron

keep = lambda _: _

keep(AttributeEditor)
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

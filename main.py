# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-24 08:30:20
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-12 07:49:37

from kivy.config import Config
from kivy.core.window import Window
import sys
import os

sys.path.append(os.path.join("orb", "lnd"))
sys.path.append(os.path.join("orb", "lnd", "grpc_generated"))

Config.set("graphics", "window_state", "maximized")
Config.set("graphics", "fullscreen", "auto")

Window.maximize()

from orb.core_ui.orb_app import OrbApp

from orb.attribute_editor.attribute_editor import AttributeEditor
from orb.channels.channels_widget import ChannelsWidget
from orb.screens.close_channel import CloseChannel
from orb.screens.rebalance import Rebalance
from orb.screens.channels_screen import ChannelsScreen
from orb.screens.pay_screen import PayScreen
from orb.dialogs.mail_dialog import MailDialog
from orb.screens.open_channel_screen import OpenChannelScreen
from orb.screens.connect_screen import ConnectScreen
from orb.screens.ingest_invoices_screen import IngestInvoicesScreen
from orb.screens.console.console_screen import ConsoleScreen
from orb.dialogs.player_dialog import PlayerDialog
from orb.screens.send_coins import SendCoins
from orb.screens.about import About
from orb.screens.rankings import Rankings
from orb.dialogs.connection_settings import ConnectionSettings
from orb.lnd import Lnd
from orb.widgets.hud.HUD import HUD
from orb.widgets.hud import HUDS

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
keep(PlayerDialog)
keep(SendCoins)
keep(About)
keep(Rankings)
keep(MainLayout)
keep(StatusLine)
keep(TopMenu)
keep(MailDialog)
keep(cron)
keep(AttributeEditor)
keep(HUD)
keep(HUDS)
keep(ConnectionSettings)

if __name__ == "__main__":
    OrbApp().run()

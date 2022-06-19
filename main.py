# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-24 08:30:20
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-19 17:15:31

print("importing system modules")

import sys
import os
from pathlib import Path

print("importing logger")

from orb.core.logging import get_logger

main_logger = get_logger(__name__)
debug = main_logger.debug

debug("importing kivy")

from kivy.config import Config
from kivy.utils import platform

# from hanging_threads import start_monitoring

# monitoring_thread = start_monitoring(seconds_frozen=600, test_interval=100)

if platform == "win":
    debug("windows detected, setting graphics multisampling to 0")
    Config.set("graphics", "multisamples", "0")

# os.environ["KIVY_AUDIO"] = "ffpyplayer"
# os.environ["KIVY_VIDEO"] = "ffpyplayer"

if platform == "macosx":
    os.environ["KIVY_DPI"] = "240"
    os.environ["KIVY_METRICS_DENSITY"] = "1.5"
    # import fabric
    # import pandas
    # import numpy
    # import matplotlib

debug("appending paths to include lnd and third party modules")
parent_dir = Path(__file__).parent
sys.path.append((parent_dir / Path("orb/lnd")).as_posix())
sys.path.append((parent_dir / Path("orb/lnd/grpc_generated")).as_posix())
sys.path.append((parent_dir / Path("third_party/contextmenu")).as_posix())
sys.path.append((parent_dir / Path("third_party/arrow")).as_posix())
sys.path.append((parent_dir / Path("third_party/python-qrcode/")).as_posix())
sys.path.append((parent_dir / Path("third_party/forex-python/")).as_posix())
sys.path.append((parent_dir / Path("third_party/bezier/src/python/")).as_posix())
sys.path.append((parent_dir / Path("third_party/colour/")).as_posix())
sys.path.append((parent_dir / Path("third_party/currency-symbols/")).as_posix())

debug("importing orb modules")

from orb.attribute_editor.attribute_editor import AttributeEditor
from orb.channels.channels_widget import ChannelsWidget
from orb.screens.close_channel import CloseChannel
from orb.screens.rebalance import Rebalance
from orb.screens.channels_screen import ChannelsScreen
from orb.screens.pay_screen import PayScreen
from orb.screens.open_channel_screen import OpenChannelScreen
from orb.screens.connect_screen import ConnectScreen
from orb.dialogs.ingest_invoices.ingest_invoices import IngestInvoices
from orb.screens.console.console_screen import ConsoleScreen
from orb.dialogs.player_dialog import PlayerDialog
from orb.screens.send_coins import SendCoins
from orb.screens.rankings import Rankings
from orb.dialogs.connection_settings import ConnectionSettings
from orb.lnd import Lnd
from orb.widgets.hud.HUD import HUD
from orb.widgets.hud import HUDS
from orb.dialogs.app_store import TipDialog
from orb.dialogs.mail_dialog import MailDialog
from orb.core_ui.main_layout import MainLayout
from orb.status_line.status_line import StatusLine
from orb.dialogs import forwarding_history

from orb.core_ui.top_menu import TopMenu
from orb.logic.cron import cron
from orb.screens.new_address_screen import NewAddress
from orb.screens.batch_open_screen import BatchOpenScreen
from orb.dialogs.fee_distribution import FeeDistribution
from orb.dialogs.help_dialog.about.about import About
from orb.dialogs.upload_app import UploadAppDialog
from orb.dialogs.highlighter_dialog.highlighter_dialog import HighlighterDialog
from orb.dialogs.connection_wizard.connection_wizard import ConnectionWizard
from orb.dialogs.umbrel_node.umbrel_node import UmbrelNode
from orb.dialogs.voltage_node.voltage_node import VoltageNode
import colour
from kivymd.effects.stiffscroll import StiffScrollEffect

from orb.core_ui.orb_app import OrbApp

debug("keeping import modules in main")

keep = lambda _: _

keep(VoltageNode)
keep(UmbrelNode)
keep(ConnectionWizard)
keep(Lnd)
keep(ChannelsWidget)
keep(Rebalance)
keep(CloseChannel)
keep(Rebalance)
keep(ChannelsScreen)
keep(PayScreen)
keep(OpenChannelScreen)
keep(ConnectScreen)
keep(IngestInvoices)
keep(ConsoleScreen)
keep(PlayerDialog)
keep(SendCoins)
keep(Rankings)
keep(MainLayout)
keep(StatusLine)
keep(TopMenu)
keep(cron)
keep(AttributeEditor)
keep(HUD)
keep(HUDS)
keep(ConnectionSettings)
keep(StiffScrollEffect)
keep(colour)
keep(TipDialog)
keep(MailDialog)
keep(NewAddress)
keep(BatchOpenScreen)
keep(FeeDistribution)
keep(About)
keep(UploadAppDialog)
keep(forwarding_history)
keep(HighlighterDialog)

if __name__ == "__main__":
    debug("in __main__")
    debug("launching main Orb App")
    OrbApp().run()

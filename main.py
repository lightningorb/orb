# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-24 08:30:20
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-03-04 03:14:19

import sys
import os
from pathlib import Path
from kivy.config import Config
from kivy.utils import platform

if platform == "win":
    Config.set("graphics", "multisamples", "0")

# os.environ["KIVY_AUDIO"] = "ffpyplayer"
# os.environ["KIVY_VIDEO"] = "ffpyplayer"

from kivy.utils import platform

if platform == "macosx":
    os.environ["KIVY_DPI"] = "240"
    os.environ["KIVY_METRICS_DENSITY"] = "1.5"
    # import fabric
    # import pandas
    # import numpy
    # import matplotlib

sys.path.append(Path("orb/lnd").as_posix())
sys.path.append(Path("orb/lnd/grpc_generated").as_posix())
sys.path.append(Path("third_party/contextmenu").as_posix())
sys.path.append(Path("third_party/arrow").as_posix())
sys.path.append(Path("third_party/python-qrcode/").as_posix())
sys.path.append(Path("third_party/forex-python/").as_posix())
sys.path.append(Path("third_party/bezier/src/python/").as_posix())
sys.path.append(Path("third_party/colour/").as_posix())
sys.path.append(Path("third_party/currency-symbols/").as_posix())

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

import colour
from kivymd.effects.stiffscroll import StiffScrollEffect

from orb.core_ui.orb_app import OrbApp

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
    # import unittest

    # print("TESTING CERTIFICATE")
    # from tests.test_certificate import TestCertificate

    # print("TESTING MACAROON")
    # from tests.test_macaroon import TestMacaroon

    # print("TESTING RSA")
    # from tests.test_sec_rsa import TestSec

    # print("TESTING MACAROON RSA")
    # from tests.test_macaroon_secure import TestMacaroonSecure

    # print("TESTING CERTIFICATE RSA")
    # from tests.test_certificate_secure import TestCertificateSecure

    # unittest.main(exit=False)

    OrbApp().run()

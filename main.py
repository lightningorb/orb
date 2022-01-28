# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-24 08:30:20
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-28 13:35:20

import sys
import os
from pathlib import Path

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

from kivy.config import Config
from kivy.core.window import Window

sys.path.append(str(Path("orb/lnd")))
sys.path.append(str(Path("orb/lnd/grpc_generated")))
sys.path.append(str(Path("third_party/contextmenu")))
sys.path.append(str(Path("third_party/arrow")))
sys.path.append(str(Path("third_party/python-qrcode/")))
sys.path.append(str(Path("third_party/forex-python/")))
sys.path.append(str(Path("third_party/bezier/src/python/")))
sys.path.append(str(Path("third_party/colour/")))
sys.path.append(str(Path("third_party/currency-symbols/")))

Config.set("graphics", "window_state", "maximized")
Config.set("graphics", "fullscreen", "auto")

Window.maximize()

from orb.attribute_editor.attribute_editor import AttributeEditor
from orb.channels.channels_widget import ChannelsWidget
from orb.screens.close_channel import CloseChannel
from orb.screens.rebalance import Rebalance
from orb.screens.channels_screen import ChannelsScreen
from orb.screens.pay_screen import PayScreen
from orb.screens.open_channel_screen import OpenChannelScreen
from orb.screens.connect_screen import ConnectScreen
from orb.screens.ingest_invoices_screen import IngestInvoicesScreen
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

from orb.core_ui.top_menu import TopMenu
from orb.logic.cron import cron
from orb.screens.new_address_screen import NewAddress
from orb.screens.batch_open_screen import BatchOpenScreen
from orb.dialogs.fee_distribution import FeeDistribution
from orb.dialogs.help_dialog.about.about import About
from orb.dialogs.upload_app import UploadAppDialog

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
keep(IngestInvoicesScreen)
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

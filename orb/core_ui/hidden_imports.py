# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-28 15:44:18
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-29 10:22:06

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
from orb.logic.cron import Cron
from orb.screens.new_address_screen import NewAddress
from orb.screens.batch_open_screen import BatchOpenScreen
from orb.dialogs.fee_distribution import FeeDistribution
from orb.dialogs.help_dialog.about.about import About
from orb.dialogs.upload_app import UploadAppDialog
from orb.dialogs.highlighter_dialog.highlighter_dialog import HighlighterDialog
from orb.dialogs.connection_wizard.connection_wizard import ConnectionWizard
from orb.dialogs.umbrel_node.umbrel_node import UmbrelNode
from orb.dialogs.voltage_node.voltage_node import VoltageNode
from orb.misc.device_id import device_id
import colour
from kivymd.effects.stiffscroll import StiffScrollEffect

from orb.core_ui.orb_app import OrbApp

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
keep(SendCoins)
keep(Rankings)
keep(MainLayout)
keep(StatusLine)
keep(TopMenu)
keep(Cron)
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
keep(device_id)

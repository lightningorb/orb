from kivy.config import Config

Config.set('graphics', 'window_state', 'maximized')

from orb_app import OrbApp

from autobalance import Autobalance
from attribute_editor.attribute_editor import AttributeEditor
from channels.channels_widget import ChannelsWidget
from screens.close_channel import CloseChannel
from screens.rebalance import Rebalance
from screens.channels_screen import ChannelsScreen
from screens.pay_screen import PayScreen
from screens.mail_screen import MailScreen
from screens.open_channel_screen import OpenChannelScreen
from screens.connect_screen import ConnectScreen
from screens.ingest_invoices_screen import IngestInvoicesScreen
from screens.console_screen import ConsoleScreen
from screens.send_coins import SendCoins
from screens.about import About
from screens.rankings import Rankings
from HUD import HUD
from fee_spy import FeeSpy

from main_layout import MainLayout
from status_line.status_line import StatusLine
from top_menu import TopMenu

keep = lambda _: _

keep(AttributeEditor)
keep(Autobalance)
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

if __name__ == "__main__":
    OrbApp().run()

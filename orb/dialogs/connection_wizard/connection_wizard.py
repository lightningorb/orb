# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-30 13:16:45


from kivy.app import App
from kivymd.uix.screen import MDScreen

from orb.dialogs.connection_wizard.lnd_conf import LNDConf
from orb.dialogs.connection_wizard.copy_keys import CopyKeys
from orb.dialogs.connection_wizard.restart_lnd import RestartLND
from orb.dialogs.connection_wizard.nodes_and_files import NodeAndFiles
from orb.dialogs.connection_wizard.ssh_credentials import SSHCredentials

keep = lambda _: _
keep(SSHCredentials)
keep(NodeAndFiles)
keep(LNDConf)
keep(RestartLND)
keep(CopyKeys)


class ConnectionWizard(MDScreen):
    def on_enter(self, *args):
        self.config = App.get_running_app().config
        super(ConnectionWizard, self).on_enter(self, *args)
        self.ids.ssh_credentials.cert_or_pass()

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        if tab_text == "Restart LND":
            self.ids.restart_lnd.stream_log()

# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-10 06:36:55
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-17 09:40:12

from threading import Thread

from kivy.clock import mainthread
from kivy.app import App

from orb.misc.decorators import guarded
from orb.dialogs.connection_wizard.tab import Tab
from orb.misc.utils import pref
from orb.misc.fab_factory import Connection


def system_ctl_service_enabled(c, service):
    out = c.run(
        "systemctl list-unit-files | grep enabled | awk '{ print $1 }'",
        warn=True,
        hide=True,
    ).stdout
    return f"{service}.service" in out.split("\n")


class NodeAndFiles(Tab):
    def save(self):
        self.set_and_save("host.type", self.ids.node_type.text)
        self.set_and_save("lnd.path", self.ids.lnd_directory.text)
        self.set_and_save("lnd.conf_path", self.ids.conf_path.text)
        self.set_and_save("lnd.log_path", self.ids.log_path.text)
        self.set_and_save("lnd.channel_db_path", self.ids.channel_db_path.text)
        self.set_and_save("lnd.macaroon_admin_path", self.ids.admin_macaroon_path.text)
        self.set_and_save(
            "lnd.tls_certificate_path", self.ids.tls_certificate_path.text
        )
        self.set_and_save("lnd.network", self.ids.network.text)
        self.set_and_save("lnd.stop_cmd", self.ids.lnd_stop_cmd.text)
        self.set_and_save("lnd.start_cmd", self.ids.lnd_start_cmd.text)

    def set_and_save(self, key, val):
        self.config = App.get_running_app().config
        section, name = key.split(".")
        print(f"Setting: {section}, {name}")
        self.config.set(section, name, val)
        self.config.write()

    @guarded
    def detect_node_type(self):
        self.ids.node_type.text = ""
        self.ids.lnd_directory.text = ""
        self.ids.conf_path.text = ""
        self.ids.log_path.text = ""
        self.ids.channel_db_path.text = ""
        self.ids.admin_macaroon_path.text = ""
        self.ids.tls_certificate_path.text = ""
        self.ids.network.text = ""
        self.ids.lnd_stop_cmd.text = ""
        self.ids.lnd_start_cmd.text = ""

        def func():

            with Connection() as c:
                test_file = lambda x: c.run(f"test -f {x}", warn=True).ok
                test_dir = lambda x: c.run(f"test -d {x}", warn=True).ok

                if test_dir("~/umbrel"):
                    self.ids.node_type.text = "umbrel"
                else:
                    self.ids.node_type.text = "default"

                node_type = self.ids.node_type.text

                if test_dir("~/.lnd"):
                    self.ids.lnd_directory.text = "~/.lnd"
                elif test_dir("~/umbrel/lnd"):
                    self.ids.lnd_directory.text = "~/umbrel/lnd"
                else:
                    print("Could not find lnd directory")
                    return

                lnd_dir = self.ids.lnd_directory.text

                for network in ["mainnet", "testnet", "signet"]:
                    if test_dir(f"{lnd_dir}/data/graph/{network}"):
                        self.ids.network.text = network
                        break
                else:
                    print("Could not detect network type.")
                    return

                network = self.ids.network.text

                if lnd_dir:

                    if test_file(f"{lnd_dir}/lnd.conf"):
                        self.ids.conf_path.text = f"{lnd_dir}/lnd.conf"

                    if test_file(f"{lnd_dir}/tls.cert"):
                        self.ids.tls_certificate_path.text = f"{lnd_dir}/tls.cert"

                    if test_file(
                        f"{lnd_dir}/data/chain/bitcoin/{network}/admin.macaroon"
                    ):
                        self.ids.admin_macaroon_path.text = (
                            f"{lnd_dir}/data/chain/bitcoin/{network}/admin.macaroon"
                        )

                    if test_file(f"{lnd_dir}/logs/bitcoin/{network}/lnd.log"):
                        self.ids.log_path.text = (
                            f"{lnd_dir}/logs/bitcoin/{network}/lnd.log"
                        )

                    if test_file(f"{lnd_dir}/data/graph/{network}/channel.db"):
                        self.ids.channel_db_path.text = (
                            f"{lnd_dir}/data/graph/{network}/channel.db"
                        )

                if node_type == "umbrel":
                    if system_ctl_service_enabled(c, "docker"):
                        self.ids.lnd_stop_cmd.text = "docker stop lnd"
                        self.ids.lnd_start_cmd.text = "docker start lnd"
                    else:
                        print(
                            "could not find an enabled docker.service file in systemctl service files"
                        )
                else:
                    if system_ctl_service_enabled(c, "lnd"):
                        self.ids.lnd_stop_cmd.text = "systemctl stop lnd"
                        self.ids.lnd_start_cmd.text = "systemctl start lnd"
                    else:
                        print(
                            "could not find an enabled lnd.service file in systemctl service files"
                        )

        Thread(target=func).start()

# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-10 06:36:55
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-30 08:52:23

from threading import Thread

from kivy.clock import mainthread
from kivy.app import App

from orb.misc.decorators import guarded
from orb.dialogs.connection_wizard.tab import Tab
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
        app = App.get_running_app()
        app.node_settings["host.type"] = self.ids.node_type.text
        app.node_settings["lnd.path"] = self.ids.lnd_directory.text
        app.node_settings["lnd.conf_path"] = self.ids.conf_path.text
        app.node_settings["lnd.log_path"] = self.ids.log_path.text
        app.node_settings["lnd.channel_db_path"] = self.ids.channel_db_path.text
        app.node_settings["lnd.macaroon_admin_path"] = self.ids.admin_macaroon_path.text
        app.node_settings[
            "lnd.tls_certificate_path"
        ] = self.ids.tls_certificate_path.text
        app.node_settings["lnd.network"] = self.ids.network.text
        app.node_settings["lnd.stop_cmd"] = self.ids.lnd_stop_cmd.text
        app.node_settings["lnd.start_cmd"] = self.ids.lnd_start_cmd.text
        print("SAVE")
        print(app.node_settings)

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
            app = App.get_running_app()
            with Connection(
                use_prefs=False,
                host=app.node_settings.get("host.hostname"),
                port=app.node_settings.get("host.port"),
                auth=app.node_settings.get("host.auth_type"),
                username=app.node_settings.get("host.username"),
                password=app.node_settings.get("host.password"),
                cert_path=app.node_settings.get("host.certificate"),
            ) as c:
                test_file = lambda x: c.run(f"test -f {x}", warn=True).ok
                test_dir = lambda x: c.run(f"test -d {x}", warn=True).ok

                home = c.run("echo $HOME").stdout.strip()

                if test_dir("~/umbrel"):
                    self.ids.node_type.text = "umbrel"
                else:
                    self.ids.node_type.text = "default"

                node_type = self.ids.node_type.text

                if test_dir("~/.lnd"):
                    self.ids.lnd_directory.text = f"{home}/.lnd"
                elif test_dir("~/umbrel/lnd"):
                    self.ids.lnd_directory.text = f"{home}/umbrel/lnd"
                elif test_dir("~/umbrel/app-data/lightning/data/lnd"):
                    self.ids.lnd_directory.text = (
                        f"{home}/umbrel/app-data/lightning/data/lnd"
                    )
                else:
                    print("Could not find lnd directory")
                    return

                lnd_dir = self.ids.lnd_directory.text

                for network in ["mainnet", "testnet", "signet"]:
                    print(f"{lnd_dir}/data/graph/{network}")
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

                if node_type == "default":
                    if system_ctl_service_enabled(c, "lnd"):
                        self.ids.lnd_stop_cmd.text = "systemctl stop lnd"
                        self.ids.lnd_start_cmd.text = "systemctl start lnd"
                    else:
                        print(
                            "could not find an enabled lnd.service file in systemctl service files"
                        )
                elif node_type == "umbrel":
                    self.ids.lnd_stop_cmd.text = f"{home}/umbrel/scripts/stop"
                    self.ids.lnd_start_cmd.text = f"{home}/umbrel/scripts/start"

                self.save()

        Thread(target=func).start()

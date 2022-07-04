# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-17 08:34:57
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-30 09:33:33

import os
import re
import time
import hashlib
from pathlib import Path
from threading import Thread
from tempfile import gettempdir

from kivy.app import App
from kivy.uix.textinput import TextInput

from orb.misc.decorators import guarded
from orb.misc.fab_factory import Connection
from orb.dialogs.connection_wizard.tab import Tab
from orb.lnd.lnd_conf import LNDConf as LNDConfParser


def md5checksum(fname):
    md5 = hashlib.md5()
    f = open(fname, "r")
    while chunk := f.read(4096):
        md5.update(chunk.encode())
    return md5.hexdigest()


class FocusTextInput(TextInput):
    def on_touch_down(self, touch):
        from orb.misc import data_manager

        if self.collide_point(*touch.pos):
            if data_manager.data_man.menu_visible:
                return False
        return super(FocusTextInput, self).on_touch_down(touch)


class LNDConf(Tab):
    @guarded
    def check_lnd_conf(self):
        def update(changes):
            self.ids.input.text = self.config.to_string()
            self.ids.report.text = "\n".join(
                changes if changes else ["no changes required"]
            )

        def func():
            app = App.get_running_app()
            print("Analyzing lnd.conf")
            if not app.node_settings.get("lnd.conf_path"):
                print("lnd.conf_path not set - quitting")
                return
            with Connection(
                use_prefs=False,
                host=app.node_settings.get("host.hostname"),
                port=app.node_settings.get("host.port"),
                auth=app.node_settings.get("host.auth_type"),
                username=app.node_settings.get("host.username"),
                password=app.node_settings.get("host.password"),
                cert_path=app.node_settings.get("host.certificate"),
            ) as c:
                print(f'Checking {app.node_settings.get("lnd.conf_path")}')
                lnd_conf = c.run(
                    f'cat {app.node_settings.get("lnd.conf_path")}', hide=True
                ).stdout
                self.config = LNDConfParser()
                self.config.read_string(lnd_conf)
                app_options = self.config.get_section("[Application Options]")
                tlsextraips = app_options.get("tlsextraip")
                tlsextradomains = app_options.get("tlsextradomain")
                hostname = app.node_settings.get("host.hostname")
                changes = []
                is_ip = re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", hostname)
                if is_ip:
                    if hostname not in tlsextraips:
                        app_options.add("tlsextraip", hostname)
                        changes.append("tlsextraip needs modifying")
                else:
                    if hostname not in tlsextradomains:
                        app_options.add("tlsextradomain", hostname)
                        changes.append("tlsextradomain needs modifying")
                if "true" not in app_options.get("tlsautorefresh"):
                    changes.append("tlsautorefresh needs modifying")
                    app_options.set("tlsautorefresh", "true")
                if "0.0.0.0:10009" not in app_options.get("rpclisten"):
                    changes.append("rpclisten needs modifying")
                    app_options.set("rpclisten", "0.0.0.0:10009")
                if "0.0.0.0:8080" not in app_options.get("restlisten"):
                    changes.append("restlisten needs modifying")
                    app_options.set("restlisten", "0.0.0.0:8080")

                update(changes)

        Thread(target=func).start()

    @guarded
    def back_up_lnd_conf(self, *args):
        app = App.get_running_app()
        backup = Path(app._get_user_data_dir()) / "lnd.conf"
        print(f"Creating lnd.conf backup {backup}")

        def func():
            with Connection(
                use_prefs=False,
                host=app.node_settings.get("host.hostname"),
                port=app.node_settings.get("host.port"),
                auth=app.node_settings.get("host.auth_type"),
                username=app.node_settings.get("host.username"),
                password=app.node_settings.get("host.password"),
                cert_path=app.node_settings.get("host.certificate"),
            ) as c:
                conf_path = Path(app.node_settings.get("lnd.conf_path"))
                print(f"copying {conf_path} to {backup}")
                lnd_conf = c.run(f"cat {conf_path.as_posix()}", hide=True).stdout
                if backup.exists():
                    print(
                        f"{backup} already exists - refusing to overwrite this backup"
                    )
                    return
                with backup.open("w") as f:
                    f.write(lnd_conf)
                if backup.exists():
                    print(f"Back-up created: {backup}")
                else:
                    print(f"failed to create backup {backup}")

        Thread(target=func).start()

    @guarded
    def restore_backup(self, *args):
        app = App.get_running_app()
        backup = os.path.expanduser(
            (Path(app._get_user_data_dir()) / "lnd.conf").as_posix()
        )
        print(f"Restoring lnd.conf backup {backup}")

        def func():
            with Connection(
                use_prefs=False,
                host=app.node_settings.get("host.hostname"),
                port=app.node_settings.get("host.port"),
                auth=app.node_settings.get("host.auth_type"),
                username=app.node_settings.get("host.username"),
                password=app.node_settings.get("host.password"),
                cert_path=app.node_settings.get("host.certificate"),
            ) as c:
                conf_path = Path(app.node_settings.get("lnd.conf_path")).as_posix()
                print(f"copying {backup} to {conf_path}")
                result = md5checksum(backup)
                md5sum = (
                    c.run(f"md5sum {conf_path}", hide=True).stdout.split()[0].strip()
                )
                if result == md5sum:
                    print("lnd.conf and backup are identical - skipping")
                else:
                    c.put(backup, conf_path)

        Thread(target=func).start()

    @guarded
    def modify_lnd_conf(self):
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
            if self.ids.input.text:
                path = Path(f"{gettempdir()}") / "lnd.conf"
                print(f"Saving conf to: {path}")
                with path.open("w") as f:
                    f.write(self.ids.input.text)
                print(f"copying {path} to {app.node_settings.get('lnd.conf_path')}")
                c.put(path, app.node_settings.get("lnd.conf_path"))

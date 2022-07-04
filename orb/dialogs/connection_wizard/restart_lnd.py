# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-10 09:17:49
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-30 09:41:55

from threading import Thread

from kivy.app import App
from kivy.clock import mainthread
from kivy.uix.textinput import TextInput

from orb.misc.decorators import guarded
from orb.misc.fab_factory import Connection
from orb.dialogs.connection_wizard.tab import Tab


class FocusTextInput(TextInput):
    def on_touch_down(self, touch):
        from orb.misc import data_manager

        if self.collide_point(*touch.pos):
            if data_manager.data_man.menu_visible:
                return False
        return super(FocusTextInput, self).on_touch_down(touch)


class RestartLND(Tab):
    def __init__(self, *args, **kwargs):
        super(RestartLND, self).__init__(*args, **kwargs)
        self.log_proc = None

    def stream_log(self):
        def func():
            class Out:
                @mainthread
                def write(_, b):
                    if b and b != "\n":
                        lines = self.ids.input.text.split("\n") + [
                            x for x in b.split("\n") if x != "\n"
                        ]
                        self.ids.input.text = "\n".join(lines[len(lines) - 30 :])

                def flush(self):
                    pass

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
                if not self.log_proc or (
                    self.log_proc and not self.log_proc.ok or self.log_proc.exited
                ):
                    self.log_proc = c.run(
                        f"tail -f {app.node_settings.get('lnd.log_path')}",
                        hide=True,
                        out_stream=Out(),
                        asynchronous=True,
                    )
                    self.log_proc.exited = False
                    self.log_proc.join()

        Thread(target=func).start()

    @guarded
    def restart_lnd(self):
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
            c.sudo(app.node_settings.get("lnd.stop_cmd"))
            c.sudo(app.node_settings.get("lnd.start_cmd"))

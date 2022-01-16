# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-17 03:11:15
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-17 03:13:07

import uuid
from traceback import print_exc

from pygments.lexers import CythonLexer

from kivy import platform
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.codeinput import CodeInput
from kivy.uix.popup import Popup

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc import data_manager
from orb.store.scripts import load_scripts, Script, save_scripts

ios = platform == "ios"


class ConsoleFileChooser(PopupDropShadow):

    selected_path = StringProperty("")


class InstallScript(Popup):
    pass


class ConsoleInput(CodeInput):

    output = StringProperty("")

    def __init__(self, *args, **kwargs):
        super(ConsoleInput, self).__init__(
            style_name="monokai", lexer=CythonLexer(), *args, **kwargs
        )

    def on_touch_down(self, touch):

        if self.collide_point(*touch.pos):
            if data_manager.data_man.menu_visible:
                return False
        return super(ConsoleInput, self).on_touch_down(touch)

    def exec(self, text):
        try:
            exec(text)
        except:
            print_exc()

    def run(self, *_):
        self.exec(self.text)

    def open_file(self, *_):
        dialog = ConsoleFileChooser()
        dialog.open()

        def do_open(widget, path):
            print(f"opening {path}")
            self.text = open(path).read()

        dialog.bind(selected_path=do_open)

    def install(self, *_):
        inst = InstallScript()
        inst.open()

        def do_install(_, *__):
            script_name = ">".join(
                x.strip() for x in inst.ids.script_name.text.split(">")
            )
            code = self.text
            scripts = load_scripts()
            existing = next(
                iter([x for x in scripts if scripts[x].menu == script_name]), None
            )
            if existing:
                scripts[existing.uuid].code = code
            else:

                uid = str(uuid.uuid4())
                scripts[uid] = Script(code=code, menu=script_name, uuid=uid)

            save_scripts()
            app = App.get_running_app()
            app.root.ids.app_menu.populate_scripts()
            inst.dismiss()

        inst.ids.install.bind(on_release=do_install)
        app = App.get_running_app()
        app.root.ids.app_menu.close_all()

    def delete(self, *_):
        inst = LoadScript()

        try:
            sc = data_manager.data_man.store.get("scripts")
        except:
            pass

        def do_delete(button, *args):
            sc = data_manager.data_man.store.get("scripts", {})
            del sc[button.text]
            data_manager.data_man.store.put("scripts", **sc)
            app = App.get_running_app()
            app.root.ids.app_menu.populate_scripts()
            inst.dismiss()

        for name in sc:
            button = Button(text=name, size_hint=(None, None), size=(480, 40))
            button.bind(on_release=do_delete)
            inst.ids.grid.add_widget(button)

        inst.open()
        app = App.get_running_app()
        app.root.ids.app_menu.close_all()

    def clear_input(self, *_):
        self.text = ""

    def clear_output(self, *_):
        self.output = ""

    def reset_split_size(self, *_):

        data_manager.data_man.store.put(
            "console", input_height=None, output_height=None
        )

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        meta = "meta" in modifiers
        direction = (
            keycode[1]
            if keycode and keycode[1] in ("left", "right", "up", "down")
            else False
        )
        if meta and direction:
            if direction == "left":
                line = self.text.split("\n")[self.cursor_row]
                for i, c in enumerate(line, 1):
                    if c not in (" ", "\t"):
                        self._cursor = (i, self._cursor[1])
                        break
            elif direction == "right":
                line = self.text.split("\n")[self.cursor_row]
                self._cursor = (len(line) - 1, self._cursor[1])

        if text != "\u0135":
            to_save = self.text + (text or "")
            do_eval = keycode[1] == "enter" and self.selection_text

            data_manager.data_man.store.put("console_input", text=to_save)
            if do_eval:
                self.exec(self.selection_text)
                return True
        return super(ConsoleInput, self).keyboard_on_key_down(
            window, keycode, text, modifiers
        )

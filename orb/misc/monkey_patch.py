# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-26 15:26:40


def fix_annotations():
    """
    Pyinvoke doesnt accept annotations by default, this fix that
    Based on: https://github.com/pyinvoke/invoke/pull/606
    """

    from unittest.mock import patch
    from inspect import getfullargspec, ArgSpec

    import invoke

    def patched_inspect_getargspec(func):
        spec = getfullargspec(func)
        return ArgSpec(*spec[0:4])

    org_task_argspec = invoke.tasks.Task.argspec

    def patched_task_argspec(*args, **kwargs):
        with patch(target="inspect.getargspec", new=patched_inspect_getargspec):
            return org_task_argspec(*args, **kwargs)

    invoke.tasks.Task.argspec = patched_task_argspec


def patch_datatables():
    """
    KivyMD's datatables seems to be very buggy.
    This monkey patch attempts to alleviate some of these
    bugs & crashes.
    """
    from kivymd.uix.datatables import TableData

    def select_all(self, state):
        """Sets the checkboxes of all rows to the active/inactive position."""

        for i in range(0, len(self.recycle_data), self.total_col_headings):
            cell_row_obj = cell_row_obj = self.view_adapter.get_visible_view(i)
            self.cell_row_obj_dict[i] = cell_row_obj
            self.on_mouse_select(cell_row_obj)
            if cell_row_obj:
                cell_row_obj.ids.check.state = state

        if state == "down":
            # select all checks on all pages
            rows_num = self.rows_num
            columns = self.total_col_headings
            full_pages = len(self.row_data) // self.rows_num
            left_over_rows = len(self.row_data) % self.rows_num

            new_checks = {}
            for page in range(full_pages):
                new_checks[page] = list(range(0, rows_num * columns, columns))

            if left_over_rows:
                new_checks[full_pages] = list(
                    range(0, left_over_rows * columns, columns)
                )

            self.current_selection_check = new_checks
            return

        # resets all checks on all pages
        self.current_selection_check = {}

    def on_mouse_select(self, instance):
        """Called on the ``on_enter`` event of the :class:`~CellRow` class."""

        if not self.pagination_menu_open:
            if instance and self.ids.row_controller.selected_row != instance.index:
                self.ids.row_controller.selected_row = instance.index
                self.ids.row_controller.select_current(self)

    TableData.on_mouse_select = on_mouse_select

    def check_all(self, state):
        """Checks if checkboxes of all rows are in the same state"""

        tmp = []
        for i in range(0, len(self.recycle_data), self.total_col_headings):
            if self.cell_row_obj_dict.get(i, None):
                cell_row_obj = self.cell_row_obj_dict[i]
            else:
                cell_row_obj = self.view_adapter.get_visible_view(i)
                if cell_row_obj:
                    self.cell_row_obj_dict[i] = cell_row_obj
            if cell_row_obj:
                tmp.append(cell_row_obj.ids.check.state == state)
        return all(tmp)

    TableData.select_all = select_all


def patch_settings():
    """
    Kivy's settings deal very badly with large inputs.
    This monkey patch resolves this issue.
    """

    from kivy.uix.settings import SettingItem
    from kivy.uix.label import Label

    def add_widget(self, *largs):
        largs = [*largs]
        if largs and type(largs[0]) is Label:
            if self.key in ["tls_certificate", "macaroon_admin"]:
                value = self.panel.get_value(self.section, self.key)[:20]
                largs[0] = Label(text=value)
        if self.content is None:
            return super(SettingItem, self).add_widget(*largs)
        return self.content.add_widget(*largs)

    SettingItem.add_widget = add_widget


def patch_store():
    """
    Make Kivy's JsonStore behave more like a regular
    python dictionary.
    """
    from kivy.storage.jsonstore import JsonStore

    def get(self, key, default=None):
        try:
            return self.orig_get(key)
        except:
            return default

    JsonStore.orig_get = JsonStore.get
    JsonStore.get = get


def patch_kv_settings():
    """
    Kivy hides the app settings if settings are provided.
    Make sure the app settings are also included in the UI.
    """
    from kivy.uix.settings import Settings

    def add_kivy_panel(self):
        from kivy import kivy_data_dir
        from kivy.config import Config
        from os.path import join

        self.add_json_panel(
            "App Settings", Config, join(kivy_data_dir, "settings_kivy.json")
        )

    Settings.add_kivy_panel = add_kivy_panel


def patch_text_input():
    """
    Disable keyboard shortcuts when a TextInput is focussed.
    """
    from kivy.uix.textinput import TextInput
    from kivy.app import App

    app = App.get_running_app()

    def on_focus(_, inst, value):
        if hasattr(app, "disable_shortcuts"):
            if value:
                app.disable_shortcuts = True
            else:
                app.disable_shortcuts = False

    TextInput.on_focus = on_focus

    TextInput._orig_draw_selection = TextInput._draw_selection

    def draw_selection(self, *largs):
        try:
            self._orig_draw_selection(*largs)
        except:
            pass

    TextInput._draw_selection = draw_selection


def patch_thread():
    from threading import Thread
    from traceback import format_exc

    orig_run = Thread.run

    def run(self, *args, **kwargs):
        try:
            orig_run(self, *args, **kwargs)
        except Exception as e:
            print(format_exc())
            print(e)

    Thread.run = run


def do_monkey_patching():
    patch_store()
    patch_settings()
    patch_kv_settings()
    patch_datatables()
    patch_text_input()
    patch_thread()

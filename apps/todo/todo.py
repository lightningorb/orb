# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 17:51:07
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-19 09:35:11

from functools import lru_cache
import os
from pathlib import Path

from peewee import Model, SqliteDatabase, CharField, BooleanField

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

from orb.misc.plugin import Plugin
from orb.store.db_meta import get_db


class Todo(Model):
    """
    Our 'Todo' model which contains the contents of the todo
    and whether it's been completed or not.
    """

    content = CharField()
    done = BooleanField()

    class Meta:
        database = get_db("todo")


class TodoItem(BoxLayout):
    """
    The individual todo entries in the UI.
    """

    content = StringProperty("")


class TodoView(Popup):
    def insert_todo(self, content):
        """
        The callback that is triggered when the user presses
        enter after entering the text for a new todo item.
        """
        todo = Todo(content=content, done=False)
        todo.save()
        self.display_todo(todo)
        self.ids.todo_input.text = ""
        self.ids.todo_input.focus = True

    def display_todo(self, todo):
        """
        Adds the todo to the UI, and registers its callbacks for when
        the done and delete buttons are pressed.
        """
        todo_item = TodoItem(content=todo.content)
        todo_item.ids.delete.on_release = lambda: self.delete_todo(todo_item, todo)
        todo_item.ids.done.on_release = lambda: self.done_todo(todo_item, todo)
        self.ids.todos.add_widget(todo_item)

    def delete_todo(self, todo_item, todo):
        """
        Callback for when the delete button is pressed.
        """
        self.ids.todos.remove_widget(todo_item)
        todo.delete_instance()

    def done_todo(self, todo_item, todo):
        """
        Callback for when the done button is pressed.
        """
        self.ids.todos.remove_widget(todo_item)
        todo.done = True
        todo.save()

    def open(self, *args, **kwargs):
        """
        This gets called when the popup is first opened.
        """
        super(TodoView, self).open(*args, **kwargs)
        for todo in Todo().select().where(Todo.done == False):
            self.display_todo(todo)


class TodoPlugin(Plugin):
    def main(self):
        """
        Main function. The caller must call this.
        """
        db = get_db("todo")
        try:
            # this throws if already connected
            db.connect()
        except:
            pass
        with db:
            db.create_tables([Todo])
        kv_path = (Path(__file__).parent / "todo.kv").as_posix()
        Builder.unload_file(kv_path)
        Builder.load_file(kv_path)
        TodoView().open()

import os
from functools import lru_cache

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

from peewee import Model, SqliteDatabase, CharField, BooleanField


@lru_cache(None)
def get_db(name):
    """
    Create the db file, and return the db object
    in a cached function.
    """
    user_data_dir = App.get_running_app().user_data_dir
    path = os.path.join(user_data_dir, f"{name}.db")
    db = SqliteDatabase(path)
    return db


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


def main():
    """
    Main function. The caller must call this.
    """
    db = get_db("todo")
    db.connect()
    with db:
        db.create_tables([Todo])
    Builder.unload_file("user/scripts/todo.kv")
    Builder.load_file("user/scripts/todo.kv")
    TodoView().open()

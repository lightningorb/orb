Extending Functionality
=======================

One of the core motivations behind Orb is to:

- make it easy for users to extend functionality by writing their own scripts
- make it easy for users to share scripts amongst themselves
- blur the line between users and developers

This entirely removes the dependency upon Orb's core development team, and follows the old adage of 'teaching someone how to fish'. Another good side-effect is the core development team can focus on delivering a high quality, stable core product while technical users can solve their own problems, and scratch their own itch.

User Paths
----------

File-system paths can be added to Orb's runtime environment. This leads to the ability to import python modules and packages into Orb.

The default user scripts path is in the current working directory, followed by ``user/scripts``.

.. note::

    In a future version of Orb, users will have the ability to add their own user script paths.

``user_setup.py``
-------------

If a user path contains a file named ``user_setup.py`` then the file is automatically imported when Orb has finished loading.


Examples
--------

A Todo List
~~~~~~~~~~~

.. code:: python

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


.. code:: python

    #: import dp kivy.metrics.dp

    <TodoView>:
        title: 'Todo'
        size_hint: None, None
        size: dp(600), dp(600)
        background_color: .6, .6, .8, .9
        overlay_color: 0, 0, 0, 0
        BoxLayout:
            orientation: 'vertical'
            ScrollView:
                size_hint: 1, 1
                pos_hint: {'center_x': .5, 'center_y': .5}
                GridLayout:
                    id: todos
                    cols: 1
                    padding: 10
                    spacing: 10
                    size_hint: 1, None
                    height: self.minimum_height
                    do_scroll_x: False
            MDTextField:
                id: todo_input
                text: ''
                helper_text: 'Todo content'
                helper_text_mode: "persistent"
                on_text_validate: root.insert_todo(self.text)

    <TodoItem@BoxLayout>:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(30)
        Label:
            text: root.content
        MDIconButton:
            id: done
            icon: "check"
            pos_hint: {"center_x": .5, "center_y": .5}
        MDIconButton:
            id: delete
            icon: "delete-forever"
            pos_hint: {"center_x": .5, "center_y": .5}
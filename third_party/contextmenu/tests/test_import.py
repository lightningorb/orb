import pytest


def test_context_menu_instantiation():
    from kivy_garden.contextmenu import ContextMenu
    context_menu = ContextMenu()
    assert context_menu.visible == False

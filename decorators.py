from ui_actions import console_output
from traceback import format_exc


def guarded(func):
    def wrapper(*args):
        try:
            func(*args)
        except:
            console_output(format_exc())

    return wrapper

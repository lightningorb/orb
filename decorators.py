import functools
from ui_actions import console_output
from traceback import format_exc


def guarded(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            console_output(format_exc())

    return wrapper_decorator


def silent(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            pass

    return wrapper_decorator

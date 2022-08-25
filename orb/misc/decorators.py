# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-26 18:25:08
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-10 09:28:58

import functools
import threading
from traceback import format_exc
from collections import defaultdict

from orb.ln import Ln
from orb.store.db_meta import get_db

locks = defaultdict(threading.Lock)


def guarded(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            print(format_exc())

    return wrapper_decorator


def silent(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            pass

    return wrapper_decorator


def public_restrict(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        if Ln().get_info().alias.lower() == "orb-public":
            raise Exception("Operation not permitted on public node")

    return wrapper_decorator


def db_connect(name: str, lock: bool = False):
    def decorator(function):
        def wrapper(*args, **kwargs):
            def run():
                db = get_db(name)
                try:
                    db.connect()
                except:
                    pass
                result = function(*args, **kwargs)
                try:
                    db.close()
                except:
                    pass
                return result

            if lock:
                with locks[name]:
                    return run()
            else:
                return run()

        return wrapper

    return decorator

# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-26 18:25:08
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-24 01:57:28

import functools
import threading
from traceback import format_exc
from collections import defaultdict

from orb.lnd import Lnd
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
        if Lnd().get_info().alias.lower() == "orb-public":
            raise Exception("Operation not permitted on public node")

    return wrapper_decorator


def db_connect(name):
    def decorator(function):
        def wrapper(*args, **kwargs):
            with locks[name]:
                db = get_db(name)
                db.connect()
                result = function(*args, **kwargs)
                db.close()
            return result

        return wrapper

    return decorator

# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 17:51:07
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-10 15:14:22

from traceback import format_exc
from threading import Lock
import functools
import string

from orb.store.db_meta import *

printable = set(string.printable)
to_ascii = lambda s: "".join(filter(lambda x: x in printable, s))


lock = Lock()
cache = {}


def aliases_cache(func):
    """
    Cache decorator for getting node aliases. This leads to
    a significant speedup as there can be many peers.
    """

    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        """
        functools.wraps things. Seriously what does this do again?
        """
        pk = args[1]

        # hack alert:
        # loading the model
        from orb.app import App

        if App.get_running_app().title != "Orb":
            return to_ascii(func(*args, **kwargs))

        from orb.store import model

        if pk in cache:
            return cache[pk]
        try:
            with lock:
                db = get_db(aliases_db_name)
                db.connect()
                alias = model.Alias().select().where(model.Alias.pk == pk)
                if alias:
                    cache[pk] = to_ascii(alias.get().alias)
                    db.close()
                    return cache[pk]
                alias = to_ascii(func(*args, **kwargs))
                model.Alias(pk=pk, alias=alias).save()
                cache[pk] = alias
                db.close()
        except:
            print(format_exc())
            alias = to_ascii(func(*args, **kwargs))
            cache[pk] = alias

        return cache[pk]

    return wrapper_decorator

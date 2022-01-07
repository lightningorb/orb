# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 17:51:07
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-08 07:29:35

import functools
from threading import Lock
from orb.store import model
from functools import lru_cache

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

        if pk in cache:
            return cache[pk]
        with lock:
            alias = model.Alias().select().where(model.Alias.pk == pk)
            if alias:
                cache[pk] = alias.get().alias
                return cache[pk]
            alias = func(*args, **kwargs)
            model.Alias(pk=pk, alias=alias).save()
            cache[pk] = alias
        return cache[pk]

    return wrapper_decorator

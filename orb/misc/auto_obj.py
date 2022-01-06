# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-04 06:12:08
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-06 07:20:44

import json


def string_to_num(data):
    """
    Convert the given data to float or int: whichever one
    fits best.

    >>> string_to_num('1')
    1
    >>> string_to_num('1.0')
    1.0
    """
    try:
        f = float(data)
        i = int(data)
        if f == i:
            return i
        else:
            if i - f == 0:
                return i
            else:
                return f
    except:
        pass
    try:
        return float(data)
    except:
        pass
    try:
        return int(data)
    except:
        pass
    return data


def to_num(data):
    """
    Recursively convert any data type to float or int
    if and when appropriate to do so.

    >>> to_num(dict(a='1', b=dict(c='1.0')))['b']['c']
    1.0
    """
    if type(data) is list:
        for i, v in enumerate(data):
            data[i] = to_num(v)
    elif type(data) is dict:
        for k, v in data.items():
            data[k] = to_num(v)
    elif type(data) is str:
        return string_to_num(data)
    return data


class AutoObj(object):
    """
    Recursively convert given data to objects.

    >>> AutoObj(dict(a='1')).a
    '1'
    """

    def __init__(self, dict1):
        self.__dict__.update(dict1)

    def __str__(self):
        return self.toJSON()

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def dict2obj(dict1):
    """
    Recursively convert any data type to float or int
    if and when appropriate to do so. Also convert the
    an object.

    >>> dict2obj(dict(a='1')).a
    1
    """
    to_num(dict1)
    return json.loads(json.dumps(dict1), object_hook=AutoObj)


def todict(obj, classkey=None):
    """
    Recursively convert an object to a dict.
    >>> obj = AutoObj(dict(a='1'))
    >>> todict(obj)['a']
    '1'
    """
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v, classkey)
        return data
    elif hasattr(obj, "_ast"):
        return todict(obj._ast())
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict(
            [
                (key, todict(value, classkey))
                for key, value in obj.__dict__.items()
                if not callable(value) and not key.startswith("_")
            ]
        )
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj


if __name__ == "__main__":
    import doctest

    doctest.testmod()

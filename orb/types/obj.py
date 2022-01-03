# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-04 06:12:08
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-04 07:23:30

import json


def convert(data):
    """
    Convert the given data to float or int: whichever one
    fits best.
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


def convert_to_num(data):
    """
    Recursively convert any data type to float or int
    if and when appropriate to do so.
    """
    if type(data) is list:
        for i, v in enumerate(data):
            data[i] = convert_to_num(v)
    elif type(data) is dict:
        for k, v in data.items():
            data[k] = convert_to_num(v)
    elif type(data) is str:
        return convert(data)
    return data


class obj:
    """
    Recursively convert given data to objects.
    """

    def __init__(self, dict1):
        self.__dict__.update(dict1)

    def __str__(self):
        return str(self.__dict__)

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def dict2obj(dict1):
    """
    Recursively convert any data type to float or int
    if and when appropriate to do so. Also convert the
    an object.
    """
    convert_to_num(dict1)
    return json.loads(json.dumps(dict1), object_hook=obj)

# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-10 12:00:02
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-10 19:36:21

"""
Class to parse and manipulate the lnd.conf file
"""

import re

ws = r"[\s \t]*"


def is_comment(line):
    return re.match(rf"{ws}#.*", line)


def is_section(line):
    return re.match(r"\[[a-z A-Z]+\][\s \t]*(#.*)*", line)


def is_value(line):
    return re.match(r"[a-zA-Z\.\-]+=.*", line)


def is_blank_line(line):
    return re.match(r"[\s\t]*", line)


class Section:
    def __init__(self, name):
        self.name = name
        self.content = []

    def add_value(self, line):
        self.content.append(line)

    def add(self, key, value):
        index = len(self.content) - 1
        i = 0
        for v in self.content:
            if type(v) is Value and v.key == key:
                index = i
            i += 1
        self.content.insert(index + 1, Value(f"{key}={value}"))

    def set(self, key, value):
        for v in self.content:
            if type(v) is Value and v.key == key:
                v.value = value
                break
        else:
            self.add(key, value)

    def get(self, key):
        res = []
        for v in self.content:
            if type(v) is Value and v.key == key:
                res.append(v.value)
        return res

    def __str__(self):
        ret = f"{self.name}\n"
        for c in self.content:
            ret += f"{c}\n"
        return ret


class Value:
    def __init__(self, line):
        m = re.match(r"([a-zA-Z\.\-]+)[\s\t]*=[\s\t]*(.*)[\s\t]*", line)
        self.key = m.group(1)
        self.value = m.group(2)

    def __str__(self):
        return f"{self.key}={self.value}\n"


class Comment:
    def __init__(self, line):
        self.line = line

    def __str__(self):
        return self.line


class LNDConf:
    def __init__(self):
        pass

    def read_string(self, st):
        self.content = []
        last_section = None
        for line in st.split("\n"):
            if is_section(line):
                last_section = Section(line)
                self.content.append(last_section)
            elif is_value(line):
                last_section.add_value(Value(line))
            elif is_comment(line):
                if not last_section:
                    self.content.append(line)
                else:
                    last_section.add_value(line)

    def read_file(self, path):
        with open(path) as f:
            self.read_string(f.read())

    def get(self, section, key):
        res = []
        for c in self.content:
            if type(c) is Section and c.name == section:
                for v in c.content:
                    if type(v) is Value and v.key == key:
                        res.append(v.value)
                break
        return res

    def get_section(self, section):
        for c in self.content:
            if type(c) is Section and c.name == section:
                return c

    def to_string(self):
        return "".join(str(x) for x in self.content)

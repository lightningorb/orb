# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 19:26:18
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-12 18:56:07

import yaml
import os

lib = None


class Base:
    def __str__(self):
        return str(self.__dict__)


class Video(Base):
    def __init__(self, name, title):
        self.name = name
        self.title = title


class Collection(Base):
    def __init__(self, name, videos: [Video]):
        self.name = name
        self.videos = videos


class Library(Base):
    def __init__(self, collections):
        self.collections = collections


def get_loader():
    loader = yaml.SafeLoader
    loader.add_constructor("!Video", lambda l, n: Video(**l.construct_mapping(n)))
    loader.add_constructor(
        "!Collection", lambda l, n: Collection(**l.construct_mapping(n))
    )
    loader.add_constructor("!Library", lambda l, n: Library(**l.construct_mapping(n)))
    return loader


def get_dumper():
    safe_dumper = yaml.SafeDumper
    safe_dumper.add_representer(
        Video,
        lambda dumper, inst: dumper.represent_mapping(
            "!Video",
            {"name": inst.name, "title": inst.title},
        ),
    )
    safe_dumper.add_representer(
        Collection,
        lambda dumper, inst: dumper.represent_mapping(
            "!Collection",
            {"name": inst.name},
            {"videos": inst.videos},
        ),
    )
    safe_dumper.add_representer(
        Library,
        lambda dumper, inst: dumper.represent_mapping(
            "!Library",
            {"collections": inst.collections},
        ),
    )
    return safe_dumper


def load_video_library():
    load = (
        lambda x: yaml.load(open(x, "r"), Loader=get_loader())
        if os.path.exists(x)
        else {}
    )
    path = "video_library.yaml"
    if os.path.exists(path):
        return load(path)


def save_video_library():
    with open("video_library.yaml", "w") as stream:
        stream.write(yaml.dump(lib, Dumper=get_dumper()))

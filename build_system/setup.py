# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-07-13 14:59:04
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-17 16:52:43

from setuptools import setup
from Cython.Build import cythonize
from pathlib import Path

paths = [
    x.as_posix()
    for x in Path("orb/").rglob("*.py")
    if "grpc_generated" not in x.as_posix()
    and "__init__" not in x.as_posix()
    and "cli/" not in x.as_posix()
]
for p in paths:
    print(p)
mods = cythonize(paths, annotate=True)
setup(ext_modules=mods)

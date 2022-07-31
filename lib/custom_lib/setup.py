# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-07-31 07:52:43
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-31 07:52:56

"""setup.py needs to be able to work without cython to build on android
"""
from pathlib import Path
from os import getenv
import sys

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

VERSION = "1.0"

FILES = list(Path(".").rglob("*.pyx")) + list(Path(".").rglob("*.pxi"))

INSTALL_REQUIRES = []
SETUP_REQUIRES = []

# detect Python for android
PLATFORM = sys.platform

if getenv("LIBLINK"):
    PLATFORM = "android"

# detect cython
if PLATFORM != "android":
    SETUP_REQUIRES.append("cython")
    INSTALL_REQUIRES.append("cython")
else:
    FILES = [fn.with_suffix(".c") for fn in FILES]

# create the extension
setup(
    name="custom_lib",
    version=VERSION,
    cmdclass={"build_ext": build_ext},
    install_requires=INSTALL_REQUIRES,
    setup_requires=SETUP_REQUIRES,
    ext_modules=[
        Extension(
            "custom_lib",
            [str(fn) for fn in FILES],
        )
    ],
    extras_require={
        "dev": [],
        "ci": [],
    },
)

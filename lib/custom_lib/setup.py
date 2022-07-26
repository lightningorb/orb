# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-07-09 13:50:14
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-26 14:52:27

from pathlib import Path
from os import getenv
import os
import sys
import shutil

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize

print("SETTTTTTUPPPPPP")

VERSION = "1.0"

# shutil.copy("/home/ubuntu/orb/orb/misc/sec_rsa.py", "./sec_rsa_cython.pyx")

FILES = list(Path(".").rglob("*.pyx"))
# FILES = ["orb/misc/sec_rsa.py"]

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

print("DOING THE BUILDDD")
print(FILES)
# create the extension
setup(
    name="custom_lib",
    version=VERSION,
    cmdclass={"build_ext": build_ext},
    install_requires=INSTALL_REQUIRES,
    setup_requires=SETUP_REQUIRES,
    ext_modules=[Extension(x.stem, [x.as_posix()]) for x in FILES],
    extras_require={
        "dev": [],
        "ci": [],
    },
)

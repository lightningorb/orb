# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-07-09 14:17:39
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-09 14:23:09

from pythonforandroid.recipe import CythonRecipe, IncludedFilesBehaviour


class CustomLibRecipe(IncludedFilesBehaviour, CythonRecipe):
    version = "1.0"
    name = "custom_lib"
    depends = [("genericndkbuild", "sdl2"), "setuptools", "cython"]
    site_package_name = "custom_lib"
    url = None
    src_filename = "../../lib/custom_lib"


recipe = CustomLibRecipe()

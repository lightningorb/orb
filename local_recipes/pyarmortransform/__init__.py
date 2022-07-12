# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-07-03 19:57:57
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-09 10:23:07

import sh
import shutil
from pythonforandroid.recipe import PythonRecipe
from pythonforandroid.util import current_directory
from pythonforandroid.logger import info
import logging


class PyArmorTransformRecipe(PythonRecipe):
    version = ""
    platforms = {"armeabi-v7a": "armv7.0", "arm64-v8a": "aarch64"}
    depends = ["python3", "pyarmor"]
    site_packages_name = "pytransform"

    def build_arch(self, arch):
        super(PyArmorTransformRecipe, self).build_arch(arch)
        info(f"BUILDING PYTRANSFORM FOR ANDROID: '{str(arch)}'")
        # from pyarmor import pyarmor

        # logging.basicConfig(
        #     level=logging.DEBUG,
        #     format="%(levelname)-8s %(message)s",
        # )
        # pyarmor.main("register", "/home/ubuntu/orb/pyarmor-regcode-2364.txt")

        if str(arch) in self.platforms:
            info("getting env")
            env = self.get_recipe_env(arch)
            info("getting build dir for arch")
            build_dir = self.get_build_dir(arch.arch)
            info(f"build_dir: {build_dir}")
            src = f"platforms/android.{self.platforms[str(arch)]}/_pytransform.so"
            info(f"src: {src}")
            dest = self.ctx.get_libs_dir(arch.arch) + "/libpytransform.so"
            info(f"dest: {dest}")
            with current_directory(build_dir):
                info(f"copy: {src} to {dest}")
                shutil.copyfile(src, dest)


recipe = PyArmorTransformRecipe()

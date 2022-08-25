# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-19 14:14:55
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-07 13:17:36

import os
import re
import shutil
from pathlib import Path

from orb.ln import Ln
from orb.logic.app_store_api import API
from orb.misc.utils import pref_path

import os
import zipfile


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(
                os.path.join(root, file),
                os.path.relpath(os.path.join(root, file), path),
            )


class UploadApp:
    def __init__(self, app):
        self.app = app
        self.archive_path = None

    def validate_for_upload(self):
        """
        Check whether this app is valid for upload
        """
        pk = Ln().get_info().identity_pubkey
        if self.app.author != pk:
            return "Not app owner - please change author entry in appinfo.yaml"
        return "ok"

    def get_tags(self):
        tags = []
        for tag in (self.app.directory / ".git/refs/tags/").glob("v*"):
            if re.match("^v[\d]+\.[\d]+\.[\d]+$", str(tag.parts[-1])):
                tags.append(tag)
        return sorted(tags)

    def get_last_tag(self):
        return next(iter(self.get_tags()), None)

    def sign(self):
        """
        Upload the app
        """

    def zip(self):
        """
        Archive the app
        """
        archive_path = pref_path("app_archive") / f"{self.app.uuid}.archive"
        if archive_path.is_file():
            os.unlink(archive_path.as_posix())
        os.makedirs(pref_path("app_archive"), exist_ok=True)
        zipf = zipfile.ZipFile(archive_path.as_posix(), "w", zipfile.ZIP_DEFLATED)
        zipf.setpassword(b"mysuperpassword")
        zipdir(self.app.directory, zipf)
        zipf.close()
        print(f"Archive created: {archive_path.as_posix()}")
        self.archive_path = archive_path
        return self.archive_path.is_file()

    def upload(self):
        return API().upload(self.archive_path.as_posix())

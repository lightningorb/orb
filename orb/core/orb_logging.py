# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-03-18 07:49:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-03 00:05:21
import sys

import logging
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    from orb.misc.utils import android

    if android:
        LOG_FILE = "/data/user/0/com.lnorb.orb/files/orbconnector/orb.log"
    else:
        LOG_FILE = "orb.log"
    file_handler = TimedRotatingFileHandler(LOG_FILE, when="midnight")
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    # logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger

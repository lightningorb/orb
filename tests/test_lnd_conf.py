# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-09 08:44:05
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-10 18:26:47

import unittest
from textwrap import dedent
from pathlib import Path
from orb.lnd.lnd_conf import LNDConf

path = (Path(__file__).parent / "lnd.conf").as_posix()


class TestLNDConf(unittest.TestCase):
    def test_multiple_tlsextraip(self):
        parser = LNDConf()
        parser.read_file(path)
        app_options = parser.get_section("[Application Options]")
        vals = set(app_options.get("tlsextraip"))
        self.assertEqual(vals, set(["10.10.10.10", "20.20.20.20"]))

    def test_add_tlsextraip(self):
        parser = LNDConf()
        parser.read_file(path)
        app_options = parser.get_section("[Application Options]")
        app_options.add("tlsextraip", "30.30.30.30")
        vals = set(app_options.get("tlsextraip"))
        self.assertEqual(vals, set(["10.10.10.10", "20.20.20.20", "30.30.30.30"]))

    def test_set(self):
        parser = LNDConf()
        parser.read_file(path)
        app_options = parser.get_section("[Application Options]")
        app_options.set("tlsautorefresh", "1")
        self.assertEqual(app_options.get("tlsautorefresh")[0], "1")

    def test_to_string(self):
        parser = LNDConf()
        parser.read_file(path)
        print(parser.to_string())


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-10 16:00:00
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-10 16:25:47

import http.server
import socketserver
from threading import Thread
import webbrowser

from orb.misc.plugin import Plugin
from random import randint

PORT = randint(8000, 9000)


class Docs(Plugin):
    def main(self):
        def server(*_):
            Handler = http.server.SimpleHTTPRequestHandler
            with socketserver.TCPServer(("", PORT), Handler) as httpd:
                url = f"http://localhost:{PORT}/docsbuild/"
                print(url)
                webbrowser.open(url)
                httpd.serve_forever()

        self.t = Thread(target=server)
        self.t.daemon = True
        self.t.start()

    @property
    def menu(self):
        return "wip > Docs"

    @property
    def uuid(self):
        return "6cd47d34-1ae8-408b-979f-d7cf82ac3350"

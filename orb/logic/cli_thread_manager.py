# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-29 13:29:02
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-29 13:31:32


class CLIThreadManager:

    threads = []

    def stop_threads(self):
        for t in self.threads:
            t.stop()
        self.threads.clear()

    def add_thread(self, thread):
        self.threads.append(thread)


cli_thread_manager = CLIThreadManager()

# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-05 10:00:19
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-05 10:09:43

import tracemalloc

snapshots = []
started = False


def start():
    global started
    if not started:
        tracemalloc.start(25)
    started = True


def snapshot():
    snapshots.append(tracemalloc.take_snapshot())


def print_stats():
    if not len(snapshots) >= 2:
        print("Need at least 2 snapshots")
        return
    top_stats = snapshots[-1].compare_to(snapshots[0], "lineno")
    print("[ Top 10 differences ]")
    for stat in top_stats[:10]:
        print(stat)

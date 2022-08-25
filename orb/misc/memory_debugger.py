# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-05 10:00:19
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-08 09:35:21

import linecache
import os
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


def pretty():
    display_top(snapshots[-1])


def display_top(snapshot, key_type="lineno", limit=10):
    snapshot = snapshot.filter_traces(
        (
            tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
            tracemalloc.Filter(False, "<unknown>"),
        )
    )
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        print(
            "#%s: %s:%s: %.1f KiB"
            % (index, frame.filename, frame.lineno, stat.size / 1024)
        )
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print("    %s" % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))

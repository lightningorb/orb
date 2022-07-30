# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-07-10 16:35:01
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-23 18:17:20

from kivy.app import App


class BalancedRatioMixin:
    def compute_balanced_ratios(self, *_):
        App.get_running_app().store.get("exclude_from_balanced_ratio", {})
        solution = []
        channels = [x for x in self.channels.values()]
        for c in channels:
            solution.append(
                self.app.store.get("balanced_ratio", {}).get(str(c.chan_id), -1)
            )
        gr = self.global_ratio
        indices = [i for i, x in enumerate(solution) if x == -1]
        capacity = self.capacity
        if capacity == 0:
            return

        def search(solution, indices, global_ratio):
            low, mid, high, n = 0, 0, 1, 0
            while low <= high:
                mid = (high + low) / 2
                for i in indices:
                    solution[i] = mid
                ratio = (
                    sum(
                        [
                            x.capacity * y
                            for x, y in zip([*self.channels.values()], solution)
                        ]
                    )
                    / capacity
                )
                abs_diff = abs(ratio - global_ratio)
                n += 1
                if abs_diff < 1 / 1e5 or n > 100:
                    return ratio
                low, high = (mid, high) if ratio < global_ratio else (low, mid)
            return ratio

        search(solution, indices, gr)
        for i, c in enumerate(channels):
            channels[i].balanced_ratio = solution[i]

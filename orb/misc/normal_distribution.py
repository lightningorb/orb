# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-26 06:52:35
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-27 03:11:29

import math


class NormalDistribution(object):
    def __init__(self):
        self.data = []
        self.probability_distribution = []
        self.total_frequency = 0
        self.total_probability = 0.0
        self.total_normal_probability = 0.0
        self.total_normal_frequency = 0.0

    def calculate_prob_dist(self):
        self.total_frequency = len(self.data)
        data_total = 0
        sum_of_squares = 0
        for item in self.data:
            index = self.__index_of(item, self.probability_distribution)
            if index < 0:
                self.probability_distribution.append(
                    {
                        "value": item,
                        "frequency": 1,
                        "probability": 0,
                        "normal_probability": 0,
                        "normal_frequency": 0,
                    }
                )
            else:
                self.probability_distribution[index]["frequency"] += 1
            data_total += item
            sum_of_squares += item ** 2
        mean = data_total / self.total_frequency
        variance = (
            sum_of_squares - ((data_total ** 2) / self.total_frequency)
        ) / self.total_frequency
        stddev = variance ** 0.5
        for pd in self.probability_distribution:
            pd["probability"] = pd["frequency"] / len(self.data)
            pd["normal_probability"] = (1.0 / (stddev * math.sqrt(2.0 * math.pi))) * (
                pow(
                    math.e, -1.0 * ((pow((pd["value"] - mean), 2.0)) / (variance * 2.0))
                )
            )
            pd["normal_frequency"] = pd["normal_probability"] * len(self.data)
            self.total_probability += pd["probability"]
            self.total_normal_probability += pd["normal_probability"]
            self.total_normal_frequency += pd["normal_frequency"]
        self.probability_distribution.sort(key=lambda k: k["value"])

    @property
    def table(self):
        ret = []
        for item in self.probability_distribution:
            ret.append(
                [
                    f'{item["value"]:5d}',
                    f'{item["probability"]:12.4f}',
                    f'{item["normal_probability"]:12.4f}',
                    f'{item["frequency"]:5d}',
                    f'{item["normal_frequency"]:12.4f}',
                ]
            )
        # ret.append(
        #     "      |{:12.4f} |{:12.6f} |{:5.0f} |{:12.4f}".format(
        #         self.total_probability,
        #         self.total_normal_probability,
        #         self.total_frequency,
        #         self.total_normal_frequency,
        #     )
        # )
        # ret.append("------------------------------------------------------")
        # return "\n".join(ret)
        return ret

    def __index_of(self, n, probdist):
        for i in range(0, len(probdist)):
            if probdist[i]["value"] == n:
                return i
        return -1

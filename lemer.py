from math import sqrt, pi
import matplotlib.pyplot as plt
import numpy as np


class LemerGenerator:
    def __init__(self, m, r0, a):
        self.r0 = r0
        self.last_r = r0
        self.m = m
        self.a = a
        self.r_list = []
        self.v_list = []
        self.aperiodic = None
        self.period = None
        self.mathematical_expectation = None
        self.dispersion = None
        self.root_mean_square_deviation = None

    def __iter__(self):
        return self

    def _reset(self):
        self.r_list = []
        self.dispersion = None
        self.period = None
        self.aperiodic = None
        self.mathematical_expectation = None
        self.root_mean_square_deviation = None
        self.last_r = self.r0

    def _calc_values(self):
        self.aperiodic = len(self.r_list)
        self.period = self.aperiodic - self.r_list[::-1].index(self.last_r)
        self.mathematical_expectation = calc_mathematical_expectation(self.v_list)
        self.dispersion = calc_dispersion(self.v_list, self.mathematical_expectation)
        self.root_mean_square_deviation = calc_root_mean_square_deviation(self.dispersion)

    def __next__(self):
        self.last_r = (self.a * self.last_r) % self.m
        if self.last_r in self.r_list:
            self._calc_values()
            raise StopIteration()

        self.r_list.insert(0, self.last_r)
        next_value = self.last_r / self.m
        self.v_list.append(next_value)
        return next_value

def calc_mathematical_expectation(items):
    return sum(items) / len(items)

def calc_dispersion(items, math_expectation):
    return sum(list(map(lambda x: pow(x - math_expectation, 2), items))) / len(items)

def calc_root_mean_square_deviation(dispersion):
    return sqrt(dispersion)

class HistogramDrawer:
    def __init__(self, sequence, interval_count = 20):
        self.sequence = sequence
        self.interval_count = interval_count
        self.intervals = None
        self._init_intervals()

    def _init_intervals(self):
        maximum = max(self.sequence)
        minimum = min(self.sequence)
        step = (maximum - minimum) / self.interval_count
        self.intervals = [0 for _ in range(self.interval_count)]

        interval_index = 0
        value_index = 0
        self.sequence.sort()
        interval_max_board = minimum + step

        while interval_index < 20 and value_index < len(self.sequence):
            if self.sequence[value_index] <= interval_max_board:
                self.intervals[interval_index] += 1
                value_index += 1
            else:
                interval_index += 1
                interval_max_board += step

    def draw(self):
        _sum = sum(self.intervals)
        plt.bar(np.arange(self.interval_count),
                self.intervals,
                color='yellow',
                edgecolor='black',
                width=0.8
                )
        plt.xticks(np.arange(self.interval_count), np.arange(self.interval_count))
        # plt.show()
        plt.savefig('result_histogram.png')

EPS = 0.001


class UniformityChecker:
    def __init__(self, sequence):
        self.sequence = sequence
        self.is_uniform = None

    def check(self):
        pairs = list(zip(self.sequence[0::2], self.sequence[1::2]))
        true_pairs_count = 0
        for x, y in pairs:
            if pow(x, 2) + pow(y, 2) < 1:
                true_pairs_count += 1

        val = true_pairs_count / len(pairs)
        print("2 * K / N: {}\nPI / 4: {}".format(val, pi / 4))
        if pi / 4 - EPS < val < pi / 4 + EPS:
            self.is_uniform = True
        else:
            self.is_uniform = False
        return self.is_uniform


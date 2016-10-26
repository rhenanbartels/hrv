# coding: utf-8
import unittest

import numpy as np

from hrv.classical import time_domain, frequency_domain
from tests.test_utils import FAKE_RRI, open_rri


class TimeDomainIndexesTestCase(unittest.TestCase):

    def test_correct_response(self):
        response = time_domain(FAKE_RRI)
        expected = {'rmssd': 38.07,
                    'sdnn': 41.93,
                    'nn50': 1,
                    'pnn50': 33.33,
                    'mrri':  793.75,
                    'mhr': 75.67}
        np.testing.assert_almost_equal(sorted(response.values()),
                                       sorted(expected.values()),
                                       decimal=2)
        self.assertEqual(response.keys(),
                         expected.keys())


class FrequencyDomainTestCase(unittest.TestCase):
    def setUp(self):
        self.real_rri = open_rri('tests/test_files/real_rri.txt')

    def test_correct_response(self):
        response = frequency_domain(self.real_rri, interp_freq=4,
                                    method='welch', segment_size=256,
                                    overlap_size=128,
                                    window_function='hanning')
        expected = {'total_power': 0.0,
                    'vlf': 0.0,
                    'lf': 0.0,
                    'hf': 0.0,
                    'lf_hf': 0.0,
                    'lfnu': 0.0,
                    'hfnu': 0.0}
        np.testing.assert_almost_equal(sorted(response.values()),
                                       sorted(expected.values()),
                                       decimal=2)
        self.assertEqual(response.keys(),
                         expected.keys())

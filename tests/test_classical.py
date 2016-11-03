# coding: utf-8
import unittest.mock

import numpy as np

from hrv.classical import time_domain, frequency_domain
from hrv.utils import _interpolate_rri
from tests.test_utils import FAKE_RRI, open_rri


class TimeDomainIndexesTestCase(unittest.TestCase):

    def test_correct_response(self):
        response = time_domain(FAKE_RRI)
        expected = {'rmssd': 38.07,
                    'sdnn': 29.82,
                    'nn50': 1,
                    'pnn50': 33.33,
                    'mrri':  793.75,
                    'mhr': 75.67}
        np.testing.assert_almost_equal(sorted(response.values()),
                                       sorted(expected.values()),
                                       decimal=2)
        self.assertEqual(response.keys(),
                         expected.keys())

    def test_correct_response_with_rri_in_seconds(self):
        response = time_domain(np.array(FAKE_RRI) / 1000)
        expected = {'rmssd': 38.07,
                    'sdnn': 29.82,
                    'nn50': 1,
                    'pnn50': 33.33,
                    'mrri':  793.75,
                    'mhr': 75.67}
        np.testing.assert_almost_equal(sorted(response.values()),
                                       sorted(expected.values()),
                                       decimal=2)


class FrequencyDomainTestCase(unittest.TestCase):
    def setUp(self):
        self.real_rri = open_rri('tests/test_files/real_rri.txt')

    def test_correct_response(self):
        response = frequency_domain(self.real_rri, interp_freq=4,
                                    method='welch', segment_size=256,
                                    overlap_size=128,
                                    window_function='hanning')
        expected = {'total_power':  3602.90,
                    'vlf': 844.5,
                    'lf': 1343.51,
                    'hf': 1414.88,
                    'lf_hf': 0.94,
                    'lfnu': 48.71,
                    'hfnu': 51.28}
        np.testing.assert_almost_equal(sorted(response.values()),
                                       sorted(expected.values()),
                                       decimal=2)
        self.assertEqual(response.keys(),
                         expected.keys())

    def frequency_analysis_with_welch(self):
        interp_freq = 4
        time_interp, rri_interp = interpolate_rri(self.real_rri, interp_freq)
        frequency_domain(self.real_rri)

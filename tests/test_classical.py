# coding: utf-8
import unittest.mock

import numpy as np

from hrv.classical import time_domain, frequency_domain, _auc
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
        response = frequency_domain(self.real_rri, fs=4, method='welch',
                                    nperseg=256, noverlap=128,
                                    window='hanning')
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

    def test_area_under_the_curve(self):
        fxx = np.arange(0, 1, 1 / 1000.0)
        pxx = np.ones(len(fxx))

        results = _auc(fxx, pxx, vlf_band=(0, 0.04), lf_band=(0.04, 0.15),
                       hf_band=(0.15, 0.4))

        np.testing.assert_almost_equal(results['vlf'], 0.04, decimal=2)
        np.testing.assert_almost_equal(results['lf'], 0.11, decimal=2)
        np.testing.assert_almost_equal(results['hf'], 0.25, decimal=2)
        np.testing.assert_almost_equal(results['total_power'], 0.4, decimal=2)
        np.testing.assert_almost_equal(results['lf_hf'], 0.44, decimal=1)
        np.testing.assert_almost_equal(results['lfnu'], 30.5, decimal=0)
        np.testing.assert_almost_equal(results['hfnu'], 69.5, decimal=0)

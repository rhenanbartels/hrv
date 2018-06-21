# coding: utf-8
import unittest.mock

import numpy as np
from spectrum import marple_data

from hrv.classical import (time_domain, frequency_domain, _auc, _poincare,
                           _nn50, _pnn50, _calc_pburg_psd)
from hrv.utils import read_from_text
from tests.test_utils import FAKE_RRI


class TimeDomainIndexesTestCase(unittest.TestCase):

    def test_correct_response(self):
        response = time_domain(FAKE_RRI)
        expected = {'rmssd': 38.07,
                    'sdnn': 29.82,
                    'nn50': 1,
                    'pnn50': 25,
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
                    'pnn50': 25,
                    'mrri':  793.75,
                    'mhr': 75.67}
        np.testing.assert_almost_equal(sorted(response.values()),
                                       sorted(expected.values()),
                                       decimal=2)

    def test_nn50(self):
        nn50 = _nn50(FAKE_RRI)

        expected = 1

        self.assertEqual(nn50, expected)

    def test_pnn50(self):
        pnn50 = _pnn50(FAKE_RRI)

        expected = 25

        self.assertEqual(pnn50, expected)


class FrequencyDomainTestCase(unittest.TestCase):
    def setUp(self):
        self.real_rri = read_from_text('tests/test_files/real_rri.txt')

    def test_frequency_domain_with_welch_method(self):
        time = np.cumsum(self.real_rri) / 1000.0
        time -= time[0]
        response = frequency_domain(self.real_rri, time=time, fs=4,
                                    method='welch', nperseg=256, noverlap=128,
                                    window='hanning')
        expected = {'total_power':  3602.89,
                    'vlf': 844.5,
                    'lf': 1343.50,
                    'hf': 1414.88,
                    'lf_hf': 0.94,
                    'lfnu': 48.70,
                    'hfnu': 51.29}
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

    @unittest.mock.patch('hrv.classical.pburg')
    def test_pburg_method_being_called(self, _pburg):
        _calc_pburg_psd(rri=[1, 2, 3], fs=4.0)
        _pburg.assert_called_once_with(data=[1, 2, 3], NFFT=None, sampling=4.0,
                                       order=16)

    @unittest.mock.patch('hrv.classical._auc')
    @unittest.mock.patch('hrv.classical._interpolate_rri')
    @unittest.mock.patch('hrv.classical._calc_pburg_psd')
    def test_frequency_domain_function_using_pburg(self, _pburg_psd, _irr,
                                                   _auc):
        fake_rri = [1, 2, 3, 4]
        _irr.return_value = fake_rri
        _pburg_psd.return_value = (np.array([1, 2]), np.array([3, 4]))
        frequency_domain(fake_rri, fs=4, method='ar', interp_method='cubic',
                         order=16)

        _pburg_psd.assert_called_once_with(rri=fake_rri, fs=4, order=16)

    def test_calc_pburg_psd_returns_numpy_arrays(self):
        fake_rri = list(range(20))
        fxx, pxx = _calc_pburg_psd(fake_rri, fs=4.0)

        self.assertIsInstance(fxx, np.ndarray)
        self.assertIsInstance(pxx, np.ndarray)

    def test_scale_by_freq_set_to_false(self):
        """
        To certify that scale_by_freq is set to False this test will check
        the average value of the estimated psd of the marple_data.
        It must be approximately equal to 0.40.
        """
        fxx, pxx = _calc_pburg_psd(marple_data, fs=1.0)

        np.testing.assert_almost_equal(np.mean(pxx), 0.400, decimal=2)


class NonLinearTestCase(unittest.TestCase):
    def test_correct_response_from_poincare(self):
        fake_rri = [10, 11, 25, 27]

        expected_sd1 = 5.11
        expected_sd2 = 11.64

        sd1, sd2 = _poincare(fake_rri)

        np.testing.assert_almost_equal(sd1, expected_sd1, decimal=1)
        np.testing.assert_almost_equal(sd2, expected_sd2, decimal=1)

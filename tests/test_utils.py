# conding: utf-8
import unittest

from unittest import mock

import numpy as np

from hrv.classical import frequency_domain
from hrv.rri import RRi
from hrv.utils import (read_from_text, EmptyFileError,
                       _interp_cubic_spline,
                       _interp_linear,
                       _create_interp_time,
                       read_from_hrm)

FAKE_RRI = [800, 810, 815, 750]
# TODO: recreate tests from files with errors


class RRIFileOpeningTestCase(unittest.TestCase):

    def test_open_rri_text_file(self):
        rri_file_name = 'tests/test_files/test_file_1.txt'

        response = read_from_text(rri_file_name)
        expected = np.array(FAKE_RRI)

        self.assertTrue(isinstance(response, RRi))
        np.testing.assert_equal(response.values, expected)

    def test_open_empty_text_file(self):
        rri_file_name = 'tests/test_files/empty.txt'
        self.assertRaises(EmptyFileError, read_from_text, rri_file_name)

    def test_open_hrm_file(self):
        rri_file_name = 'tests/test_files/test_file_2.hrm'

        response = read_from_hrm(rri_file_name)
        expected = np.array(FAKE_RRI)

        self.assertTrue(isinstance(response, RRi))
        np.testing.assert_equal(response.values, expected)

    def test_open_empty_hrm_file(self):
        rri_file_name = 'tests/test_files/test_file_mistake_2.hrm'
        self.assertRaises(EmptyFileError, read_from_hrm, rri_file_name)


class InterpolationTestCase(unittest.TestCase):
    def setUp(self):
        self.real_rri = read_from_text('tests/test_files/real_rri.txt')

    def test_create_interp_time(self):
        time = [0, 1]

        expected = np.array([0, 0.25, 0.5, 0.75, 1.0])
        interp_time = _create_interp_time(time, 4.0)

        np.testing.assert_equal(interp_time, expected)

    def test_interpolate_rri_spline_cubic(self):
        rri = [800, 810, 790, 815]
        time = [0, 1, 2, 3]
        fs = 4.0

        rrix = _interp_cubic_spline(rri, time, fs)
        expected = [
            800., 809.4140625, 813.4375, 813.2421875, 810.,
            804.8828125, 799.0625, 793.7109375, 790., 789.1015625,
            792.1875, 800.4296875, 815.
        ]

        np.testing.assert_array_almost_equal(rrix, expected)

    def test_interpolate_rri_spline_linear(self):
        rri = [800, 810, 790, 815]
        time = [0, 1, 2, 3]
        fs = 4.0

        rrix = _interp_linear(rri, time, fs)
        expected = [
            800., 802.5, 805., 807.5, 810., 805., 800., 795.,  790., 796.25,
            802.5, 808.75, 815.
        ]

        np.testing.assert_array_almost_equal(rrix, expected)

    @mock.patch('hrv.classical._auc')
    @mock.patch('hrv.classical.welch')
    @mock.patch('hrv.utils._transform_rri')
    def test_none_interpolation_method(self, _rri, _welch, _auc):
        random_values = np.random.randn(10)
        _welch.return_value = (random_values, random_values)
        _rri.return_value = self.real_rri

        frequency_domain(self.real_rri, interp_method=None)

        _welch.assert_called_once_with(fs=4.0, x=self.real_rri)

    @mock.patch('hrv.classical.welch')
    @mock.patch('hrv.classical._auc')
    @mock.patch('hrv.utils.np.interp')
    def test_uses_linear_interpolate_method(self, _interp, _auc, _welch):
        _interp.return_value = np.arange(10)
        _welch.return_value = [1, 2]

        frequency_domain(self.real_rri, interp_method='linear')

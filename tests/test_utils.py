# conding: utf-8
import unittest

from unittest import mock

import numpy as np

from hrv.classical import frequency_domain, time_domain
from hrv.rri import RRi
from hrv.utils import (validate_rri, read_from_text, EmptyFileError,
                       _create_time_info,
                       _transform_rri_to_miliseconds,
                       _interp_cubic_spline,
                       _interp_linear,
                       _create_interp_time,
                       read_from_hrm)

FAKE_RRI = [800, 810, 815, 750]
# TODO: recreate tests from files with errors


class RRIValidationTestCase(unittest.TestCase):
    def test_simple_rri_validation(self):
        @validate_rri
        def validate(rri):
            return rri
        response = validate(FAKE_RRI)
        self.assertIsInstance(response, np.ndarray)

    def test_rri_is_different_than_numbers(self):
        string_rri = '100, 300, 400, 500'
        self.assertRaises(ValueError, time_domain, string_rri)

    def test_rri_is_list_numbers(self):
        rri_with_text = FAKE_RRI + ['text']
        self.assertRaises(ValueError, time_domain, rri_with_text)

    def test_transform_rri_to_miliseconds(self):
        expected = FAKE_RRI
        response = _transform_rri_to_miliseconds(np.array(FAKE_RRI) / 1000.0)
        np.testing.assert_equal(response, expected)

    def test_rri_all_zeros(self):
        self.assertRaises(ValueError, time_domain, [0, 0, 0, 0, 0])


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


class FrequencyDomainArgumentsTestCase(unittest.TestCase):
    # @unittest.skip('need further implementation')
    def test_method_arguments(self):
        self.assertRaises(ValueError, frequency_domain,
                          rri=FAKE_RRI, method='other')


class FrequencyDomainAuxiliaryFunctionsTestCase(unittest.TestCase):
    def setUp(self):
        self.real_rri = read_from_text('tests/test_files/real_rri.txt')

    def test_create_time_information(self):
        expected = np.cumsum(FAKE_RRI) / 1000.0
        expected -= expected[0]
        response = _create_time_info(FAKE_RRI)
        np.testing.assert_equal(response, expected)

    def test_create_interp_time(self):
        fake_rri = [0, 1000]

        expected = np.arange(0, 1, 0.25)
        interp_time = _create_interp_time(fake_rri, 4.0)

        np.testing.assert_equal(interp_time, expected)

    def test_interpolate_rri_spline_cubic(self):
        expected_diff = 0.25
        response_time_interp, response_rri_interp = _interp_cubic_spline(
            self.real_rri, fs=4)
        self.assertTrue(all(map(lambda x: x == expected_diff,
                        np.diff(response_time_interp))))
        self.assertEqual(len(response_time_interp), len(response_rri_interp))
        self.assertTrue(len(response_rri_interp) > len(self.real_rri))

    def test_interpolate_rri_spline_linear(self):
        expected_diff = 0.25
        response_time_interp, response_rri_interp = _interp_linear(
            self.real_rri, fs=4)
        self.assertTrue(all(map(lambda x: x == expected_diff,
                        np.diff(response_time_interp))))
        self.assertEqual(len(response_time_interp), len(response_rri_interp))
        self.assertTrue(len(response_rri_interp) > len(self.real_rri))

    @mock.patch('hrv.classical._auc')
    @mock.patch('hrv.classical.welch')
    @mock.patch('hrv.utils._transform_rri')
    def test_none_interpolation_method(self, _rri, _welch, _auc):
        random_values = np.random.randn(10)
        _welch.return_value = (random_values, random_values)
        _rri.return_value = self.real_rri

        frequency_domain(self.real_rri, interp_method=None)

        _welch.assert_called_once_with(fs=4.0, x=self.real_rri)

    # TODO: Refactor tests with mock
    @mock.patch('hrv.classical.welch')
    @mock.patch('hrv.classical._auc')
    @mock.patch('hrv.utils.interpolate.splev')
    @mock.patch('hrv.utils.interpolate.splrep')
    @mock.patch('hrv.utils._create_interp_time')
    def test_uses_cubic_interpolation_method(self, _interp_time, _splrep,
                                             _splev, _auc, _welch):
        fake_values = np.arange(10)
        _interp_time.return_value = fake_values
        _splrep.return_value = fake_values
        _splev.return_value = fake_values
        _welch.return_value = [1, 2]

        frequency_domain(self.real_rri, interp_method='cubic')

        _splev.assert_called_once_with(fake_values, fake_values, der=0)

    @mock.patch('hrv.classical.welch')
    @mock.patch('hrv.classical._auc')
    @mock.patch('hrv.utils.np.interp')
    def test_uses_linear_interpolate_method(self, _interp, _auc, _welch):
        _interp.return_value = np.arange(10)
        _welch.return_value = [1, 2]

        frequency_domain(self.real_rri, interp_method='linear')

# conding: utf-8
import unittest

import numpy as np

from hrv.classical import frequency_domain, time_domain
from hrv.utils import (validate_rri, open_rri, EmptyFileError,
                       _identify_rri_file_type, FileNotSupportedError,
                       _open_rri_from_text, _open_rri_from_hrm,
                       _create_time_info,
                       _transform_rri_to_miliseconds,
                       _interpolate_rri)

FAKE_RRI = [800, 810, 815, 750]


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
        expected = FAKE_RRI
        response = open_rri(rri_file_name)
        np.testing.assert_equal(response, expected)

    def test_open_rri_with_not_supported_extension(self):
        rri_file_name = 'tests/tests_files/test_file_1.bin'
        self.assertRaises(FileNotSupportedError, open_rri, rri_file_name)

    def test_open_empty_text_file(self):
        rri_file_name = 'tests/test_files/empty.txt'
        self.assertRaises(EmptyFileError, open_rri, rri_file_name)

    def test_open_hrm_file(self):
        rri_file_name = 'tests/test_files/test_file_2.hrm'
        response = open_rri(rri_file_name)
        expected = FAKE_RRI
        np.testing.assert_equal(response, expected)

    def test_text_open_funtion(self):
        rri_file_name = 'tests/test_files/test_file_1.txt'
        file_content = open(rri_file_name).read()
        expected = FAKE_RRI
        response = _open_rri_from_text(file_content)
        np.testing.assert_equal(response, expected)

    def test_hrm_open_funtion(self):
        rri_file_name = 'tests/test_files/test_file_2.hrm'
        file_content = open(rri_file_name).read()
        expected = FAKE_RRI
        response = _open_rri_from_hrm(file_content)
        np.testing.assert_equal(response, expected)

    def test_open_hrm_file_with_mistake(self):
        rri_file_name = 'tests/test_files/test_file_mistake_2.hrm'
        self.assertRaises(EmptyFileError, open_rri, rri_file_name)

    def test_identify_file_type(self):
        rri_file_name = 'tests/test_files/test_file_1.txt'
        file_obj = open(rri_file_name, 'r')
        expected = 'text'
        response = _identify_rri_file_type(file_obj.read())
        self.assertEqual(response, expected)

    def test_text_file_not_supported(self):
        rri_file_name = 'tests/test_files/test_file_2.txt'
        file_obj = open(rri_file_name, 'r')
        self.assertRaises(FileNotSupportedError, _identify_rri_file_type,
                          file_obj.read())

    def test_text_file_not_supported_with_words(self):
        rri_file_name = 'tests/test_files/test_file_3.txt'
        file_obj = open(rri_file_name, 'r')
        self.assertRaises(FileNotSupportedError, _identify_rri_file_type,
                          file_obj.read())

    def test_open_rri_from_text_fileobj(self):
        rri_file_name = 'tests/test_files/test_file_1.txt'
        file_obj = open(rri_file_name, 'r')
        expected = FAKE_RRI
        response = open_rri(file_obj)
        np.testing.assert_equal(response, expected)

    def test_open_rri_from_hrm_fileobj(self):
        rri_file_name = 'tests/test_files/test_file_2.hrm'
        file_obj = open(rri_file_name, 'r')
        expected = FAKE_RRI
        response = open_rri(file_obj)
        np.testing.assert_equal(response, expected)

    def test_open_rri_from_notsupported_fileobj(self):
        rri_file_name = 'tests/test_files/test_file_3.txt'
        file_obj = open(rri_file_name, 'r')
        self.assertRaises(FileNotSupportedError, open_rri, file_obj)


class FrequencyDomainArgumentsTestCase(unittest.TestCase):
    #@unittest.skip('need further implementation')
    def test_method_arguments(self):
        self.assertRaises(ValueError, frequency_domain,
                          rri=FAKE_RRI, method='welch', segment_size='258')

        self.assertRaises(ValueError, frequency_domain,
                          rri=FAKE_RRI, method='welch', segment_size=-1)

        self.assertRaises(ValueError, frequency_domain,
                          rri=FAKE_RRI, method='welch', segment_size=256,
                          overlap_size='128')

        self.assertRaises(ValueError, frequency_domain,
                          rri=FAKE_RRI, method='welch', segment_size=256,
                          overlap_size=-1)

        self.assertRaises(ValueError, frequency_domain,
                          rri=FAKE_RRI, method='welch', segment_size=10,
                          overlap_size=1)

class FrequencyDomainAuxiliaryFunctionsTestCase(unittest.TestCase):
    def setUp(self):
        self.real_rri = open_rri('tests/test_files/real_rri.txt')

    def test_create_time_information(self):
        expected = np.cumsum(FAKE_RRI) / 1000.0
        expected -= expected[0]
        response = _create_time_info(FAKE_RRI)
        np.testing.assert_equal(response, expected)

    def test_interpolate_rri(self):
        expexted_diff = 0.25
        response_time_interp, response_rri_interp = _interpolate_rri(
            self.real_rri, interp_freq=4)
        self.assertTrue(all(map(lambda x: x == 0.25,
                                 np.diff(response_time_interp))))
        self.assertEqual(len(response_time_interp), len(response_rri_interp))

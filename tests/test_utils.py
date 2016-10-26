# conding: utf-8
import unittest

import numpy as np

from hrv.utils import (validate_rri, open_rri, EmptyFileError,
                       identify_rri_file_type, FileNotSupportedError,
                       open_rri_from_text, open_rri_from_hrm,
                       _check_frequency_domain_arguments)

FAKE_RRI = [800, 810, 815, 750]


class RRIValidationTestCase(unittest.TestCase):
    def test_simple_rri_validation(self):
        response = validate_rri(FAKE_RRI)
        self.assertIsInstance(response, np.ndarray)

    def test_rri_is_different_than_numbers(self):
        string_rri = '100, 300, 400, 500'
        self.assertRaises(ValueError, validate_rri, string_rri)

    def test_rri_is_list_numbers(self):
        rri_with_text = FAKE_RRI + ['text']
        self.assertRaises(ValueError, validate_rri, rri_with_text)


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
        response = open_rri_from_text(file_content)
        np.testing.assert_equal(response, expected)

    def test_hrm_open_funtion(self):
        rri_file_name = 'tests/test_files/test_file_2.hrm'
        file_content = open(rri_file_name).read()
        expected = FAKE_RRI
        response = open_rri_from_hrm(file_content)
        np.testing.assert_equal(response, expected)

    def test_open_hrm_file_with_mistake(self):
        rri_file_name = 'tests/test_files/test_file_mistake_2.hrm'
        self.assertRaises(EmptyFileError, open_rri, rri_file_name)

    def test_identify_file_type(self):
        rri_file_name = 'tests/test_files/test_file_1.txt'
        file_obj = open(rri_file_name, 'r')
        expected = 'text'
        response = identify_rri_file_type(file_obj.read())
        self.assertEqual(response, expected)

    def test_text_file_not_supported(self):
        rri_file_name = 'tests/test_files/test_file_2.txt'
        file_obj = open(rri_file_name, 'r')
        self.assertRaises(FileNotSupportedError, identify_rri_file_type,
                          file_obj.read())

    def test_text_file_not_supported_with_words(self):
        rri_file_name = 'tests/test_files/test_file_3.txt'
        file_obj = open(rri_file_name, 'r')
        self.assertRaises(FileNotSupportedError, identify_rri_file_type,
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

    def test_method_arguments(self):
        self.assertRaises(ValueError, _check_frequency_domain_arguments,
                          rri=FAKE_RRI, method='method')

        self.assertRaises(ValueError, _check_frequency_domain_arguments,
                          rri=FAKE_RRI, method='welch', segment_size='258')

        self.assertRaises(ValueError, _check_frequency_domain_arguments,
                          rri=FAKE_RRI, method='welch', segment_size=-1)

        self.assertRaises(ValueError, _check_frequency_domain_arguments,
                          rri=FAKE_RRI, method='welch', segment_size=256,
                          overlap_size='128')

        self.assertRaises(ValueError, _check_frequency_domain_arguments,
                          rri=FAKE_RRI, method='welch', segment_size=256,
                          overlap_size=-1)

        self.assertRaises(ValueError, _check_frequency_domain_arguments,
                          rri=FAKE_RRI, method='welch', segment_size=10,
                          overlap_size=1)

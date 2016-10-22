# conding: utf-8
import unittest

import numpy as np

from hrv.utils import (validate_rri, open_rri, EmptyFileError,
                       identify_rri_file_type)

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
        self.assertRaises(IOError, open_rri, rri_file_name)

    def test_open_empty_text_file(self):
        rri_file_name = 'tests/test_files/empty.txt'
        self.assertRaises(EmptyFileError, open_rri, rri_file_name)

    def test_open_hrm_file(self):
        rri_file_name = 'tests/test_files/test_file_2.hrm'
        response = open_rri(rri_file_name)
        expected = FAKE_RRI
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

import unittest

import numpy as np

from hrv.exceptions import EmptyFileError
from hrv.io import read_from_text, read_from_hrm
from hrv.rri import RRi
from tests.test_utils import FAKE_RRI


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

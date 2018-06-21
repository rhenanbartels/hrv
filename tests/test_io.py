import unittest

import numpy as np

from hrv.exceptions import EmptyFileError
from hrv.io import read_from_text, read_from_hrm, read_from_csv
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


class OpenRRiFromCsv(unittest.TestCase):
    def test_open_rri_single_column(self):
        rri = read_from_csv('tests/test_files/rri_1.csv')

        self.assertTrue(isinstance(rri, RRi))
        np.testing.assert_equal(rri.values, np.array([790, 815, 800, 795]))

    def test_open_rri_single_column_with_header(self):
        rri = read_from_csv(
            'tests/test_files/rri_header.csv',
            row_offset=1
        )

        self.assertTrue(isinstance(rri, RRi))
        np.testing.assert_equal(rri.values, np.array([790, 815, 800, 795]))

    def test_open_rri_multiple_columns(self):
        rri = read_from_csv(
            'tests/test_files/rri_multiple_columns.csv',
            rri_col_index=1,
            row_offset=1
        )

        self.assertTrue(isinstance(rri, RRi))
        np.testing.assert_equal(rri.values, np.array([790, 815, 800, 795]))

    def test_open_rri_with_time(self):
        rri = read_from_csv(
            'tests/test_files/rri_multiple_columns.csv',
            rri_col_index=1,
            time_col_index=0,
            row_offset=1
        )

        self.assertTrue(isinstance(rri, RRi))
        np.testing.assert_equal(rri.values, np.array([790, 815, 800, 795]))
        np.testing.assert_equal(rri.time, np.array([1.0, 2.0, 3.0, 4.0]))

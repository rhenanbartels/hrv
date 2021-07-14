import unittest

import pytest
import numpy as np

from hrv.exceptions import EmptyFileError
from hrv.io import read_from_text, read_from_hrm, read_from_csv
from hrv.rri import RRi
from tests.test_utils import FAKE_RRI


class TestRRIFileOpening:
    def test_open_rri_text_file(self):
        rri_file_name = "tests/test_files/test_file_1.txt"

        response = read_from_text(rri_file_name)
        expected = np.array(FAKE_RRI)

        assert isinstance(response, RRi)
        np.testing.assert_equal(response.values, expected)

    def test_open_empty_text_file(self):
        rri_file_name = "tests/test_files/empty.txt"
        with pytest.raises(EmptyFileError):
            read_from_text(rri_file_name)

    def test_open_hrm_file(self):
        rri_file_name = "tests/test_files/test_file_2.hrm"

        response = read_from_hrm(rri_file_name)
        expected = np.array(FAKE_RRI)

        assert isinstance(response, RRi)
        np.testing.assert_equal(response.values, expected)

    def test_open_empty_hrm_file(self):
        rri_file_name = "tests/test_files/test_file_mistake_2.hrm"
        with pytest.raises(EmptyFileError):
            read_from_hrm(rri_file_name)

    def test_open_text_rri_with_floats(self, text_file_with_floats):
        rri = read_from_text(text_file_with_floats.name)
        expected = np.array([570, 1125, 570, 1133])

        np.testing.assert_equal(rri.values, expected)


class TestOpenRRiFromCsv:
    def test_open_rri_single_column(self):
        rri = read_from_csv("tests/test_files/rri_1.csv")

        assert isinstance(rri, RRi)
        np.testing.assert_equal(rri.values, np.array([790, 815, 800, 795]))

    def test_open_rri_single_column_with_header(self):
        rri = read_from_csv("tests/test_files/rri_header.csv", row_offset=1)

        assert isinstance(rri, RRi)
        np.testing.assert_equal(rri.values, np.array([790, 815, 800, 795]))

    def test_open_rri_multiple_columns(self):
        rri = read_from_csv(
            "tests/test_files/rri_multiple_columns.csv", rri_col_index=1, row_offset=1
        )

        assert isinstance(rri, RRi)
        np.testing.assert_equal(rri.values, np.array([790, 815, 800, 795]))

    def test_open_rri_with_time(self):
        rri = read_from_csv(
            "tests/test_files/rri_multiple_columns.csv",
            rri_col_index=1,
            time_col_index=0,
            row_offset=1,
        )

        assert isinstance(rri, RRi)
        np.testing.assert_equal(rri.values, np.array([790, 815, 800, 795]))
        np.testing.assert_equal(rri.time, np.array([1.0, 2.0, 3.0, 4.0]))

    def test_open_rri_separated_with_semicolon(self):
        rri = read_from_csv("tests/test_files/rri_semicolon.csv", row_offset=1,)

        assert isinstance(rri, RRi)
        np.testing.assert_equal(rri.values, [790, 815, 800, 795])

    def test_parse_time_column_in_csv(self):
        rri = read_from_csv(
            "tests/test_files/rri_multiple_columns.csv",
            rri_col_index=1,
            time_col_index=0,
            row_offset=1,
            time_parser=float,
        )

        assert isinstance(rri, RRi)
        np.testing.assert_equal(rri.values, np.array([790, 815, 800, 795]))
        np.testing.assert_equal(rri.time, np.array([1.0, 2.0, 3.0, 4.0]))

    def test_parse_datetime_column_in_csv(self):
        def _time_parser(dt):
            return int(dt.split(":")[-1])

        rri = read_from_csv(
            "tests/test_files/rri_multiple_columns_datetime.csv",
            rri_col_index=1,
            time_col_index=0,
            row_offset=1,
            time_parser=_time_parser,
        )

        assert isinstance(rri, RRi)
        np.testing.assert_equal(rri.values, np.array([790, 815, 800, 795]))
        np.testing.assert_equal(rri.time, np.array([56, 57, 58, 59]))

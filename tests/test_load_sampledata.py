from unittest import TestCase

import numpy as np

from hrv.io import RRi
from hrv.sampledata._load import load_sample_data
from hrv.sampledata import load_rest_rri, load_exercise_rri, load_noisy_rri


class TestLoadSampleData(TestCase):
    def test_load_sample_rest_rri(self):
        sample_rri = load_sample_data('rest_rri.txt')

        self.assertIsInstance(sample_rri, RRi)
        np.testing.assert_almost_equal(
            sample_rri[:3],
            [1114., 1113., 1066.]
        )
        np.testing.assert_almost_equal(
            sample_rri[-3:],
            [956., 1018., 1021]
        )

    def test_load_rest_rri_function(self):
        sample_rri = load_rest_rri()

        self.assertIsInstance(sample_rri, RRi)
        np.testing.assert_almost_equal(
            sample_rri[:3],
            [1114., 1113., 1066.]
        )
        np.testing.assert_almost_equal(
            sample_rri[-3:],
            [956., 1018., 1021]
        )

    def test_load_sample_exercise_rri(self):
        sample_rri = load_sample_data('exercise_rri.hrm')

        self.assertIsInstance(sample_rri, RRi)
        np.testing.assert_almost_equal(
            sample_rri[:3],
            [1589.,  783.,  752.]
        )
        np.testing.assert_almost_equal(
            sample_rri[-3:],
            [562., 555., 557.]
        )

    def test_load_exercise_rri(self):
        sample_rri = load_exercise_rri()

        self.assertIsInstance(sample_rri, RRi)
        np.testing.assert_almost_equal(
            sample_rri[:3],
            [1589.,  783.,  752.]
        )
        np.testing.assert_almost_equal(
            sample_rri[-3:],
            [562., 555., 557.]
        )

    def test_load_sample_noisy_rri(self):
        sample_rri = load_sample_data('noisy_rri.hrm')

        self.assertIsInstance(sample_rri, RRi)
        np.testing.assert_almost_equal(
            sample_rri[:3],
            [904., 913., 937.]
        )
        np.testing.assert_almost_equal(
            sample_rri[-3:],
            [704., 805., 808.]
        )

    def test_load_noisy_rri(self):
        sample_rri = load_noisy_rri()

        self.assertIsInstance(sample_rri, RRi)
        np.testing.assert_almost_equal(
            sample_rri[:3],
            [904., 913., 937.]
        )
        np.testing.assert_almost_equal(
            sample_rri[-3:],
            [704., 805., 808.]
        )

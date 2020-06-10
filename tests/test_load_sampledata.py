from unittest import TestCase

import numpy as np

from hrv.io import RRi
from hrv.sampledata._load import load_sample_data
from hrv.sampledata import load_rest_rri, load_exercise_rri, load_noisy_rri


class TestLoadSampleData(TestCase):
    def test_load_sample_rest_rri(self):
        sample_rri = load_sample_data("rest_rri.txt")

        self.assertIsInstance(sample_rri, RRi)
        np.testing.assert_almost_equal(sample_rri[:3], [1114.0, 1113.0, 1066.0])
        np.testing.assert_almost_equal(sample_rri[-3:], [956.0, 1018.0, 1021])

    def test_load_rest_rri_function(self):
        sample_rri = load_rest_rri()

        self.assertIsInstance(sample_rri, RRi)
        np.testing.assert_almost_equal(sample_rri[:3], [1114.0, 1113.0, 1066.0])
        np.testing.assert_almost_equal(sample_rri[-3:], [956.0, 1018.0, 1021])

    def test_load_sample_exercise_rri(self):
        sample_rri = load_sample_data("exercise_rri.hrm")

        self.assertIsInstance(sample_rri, RRi)
        np.testing.assert_almost_equal(sample_rri[:3], [1589.0, 783.0, 752.0])
        np.testing.assert_almost_equal(sample_rri[-3:], [562.0, 555.0, 557.0])

    def test_load_exercise_rri(self):
        sample_rri = load_exercise_rri()

        self.assertIsInstance(sample_rri, RRi)
        np.testing.assert_almost_equal(sample_rri[:3], [1589.0, 783.0, 752.0])
        np.testing.assert_almost_equal(sample_rri[-3:], [562.0, 555.0, 557.0])

    def test_load_sample_noisy_rri(self):
        sample_rri = load_sample_data("noisy_rri.hrm")

        self.assertIsInstance(sample_rri, RRi)
        np.testing.assert_almost_equal(sample_rri[:3], [904.0, 913.0, 937.0])
        np.testing.assert_almost_equal(sample_rri[-3:], [704.0, 805.0, 808.0])

    def test_load_noisy_rri(self):
        sample_rri = load_noisy_rri()

        self.assertIsInstance(sample_rri, RRi)
        np.testing.assert_almost_equal(sample_rri[:3], [904.0, 913.0, 937.0])
        np.testing.assert_almost_equal(sample_rri[-3:], [704.0, 805.0, 808.0])

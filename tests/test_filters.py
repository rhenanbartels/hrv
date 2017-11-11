from unittest import TestCase

import numpy as np

from hrv.filters import moving_average, moving_median, quotient


class Filter(TestCase):
    def test_moving_average_order_3(self):
        fake_rri = np.array([810, 830, 860, 790, 804])

        rri_filt = moving_average(fake_rri, order=3)

        expected = [810, 833.33, 826.66, 818, 804]
        np.testing.assert_almost_equal(rri_filt, expected, decimal=2)

    def test_moving_average_order_5(self):
        fake_rri = np.array([810, 830, 860, 790, 804, 801, 800])

        rri_filt = moving_average(fake_rri, order=5)

        expected = [810, 830, 818.79, 817.0, 811.0, 801, 800]
        np.testing.assert_almost_equal(rri_filt, expected, decimal=2)

    def test_moving_median_oder_3(self):
        fake_rri = np.array([810, 830, 860, 790, 804])

        rri_filt = moving_median(fake_rri, order=3)

        expected = [810, 830.0, 830.0, 804, 804]
        np.testing.assert_almost_equal(rri_filt, expected, decimal=2)

    def test_moving_median_order_5(self):
        fake_rri = np.array([810, 830, 860, 790, 804, 801, 800])

        rri_filt = moving_median(fake_rri, order=5)

        expected = [810, 830, 810.0, 804.0, 801.0, 801, 800]
        np.testing.assert_almost_equal(rri_filt, expected, decimal=2)

    def test_quotient_filter(self):
        fake_rri = [810, 580, 805, 790]

        rri_filt = quotient(fake_rri)

        expected = [805, 790]
        np.testing.assert_almost_equal(rri_filt, expected, decimal=2)

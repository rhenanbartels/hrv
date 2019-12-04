from unittest import TestCase

import numpy as np

from hrv.detrend import polynomial_detrend
from hrv.rri import RRi, RRiDetrended


class RRiDetrend(TestCase):
    def test_polynomial_detrend(self):
        fake_rri = RRi([810, 830, 860, 790, 804])

        detrended_rri = polynomial_detrend(fake_rri, degree=3)

        expected_rri = [
            4.12877839,
            -16.31947386,
            25.77155567,
            -18.14773522,
            4.56687502
        ]
        np.testing.assert_almost_equal(detrended_rri, expected_rri)
        assert isinstance(detrended_rri, RRiDetrended)
        np.testing.assert_almost_equal(detrended_rri.time, fake_rri.time)
        np.testing.assert_almost_equal(detrended_rri.mean(), 0)

    def test_detrend_with_non_RRi_object(self):
        fake_rri = [810, 830, 860, 790, 804]

        detrended_rri = polynomial_detrend(fake_rri, degree=3)

        expected_rri = [
            4.12877839,
            -16.31947386,
            25.77155567,
            -18.14773522,
            4.56687502
        ]
        expected_time = np.array([0.   , 0.83 , 1.69 , 2.48 , 3.284])

        np.testing.assert_almost_equal(detrended_rri, expected_rri)
        assert isinstance(detrended_rri, RRiDetrended)
        np.testing.assert_almost_equal(detrended_rri.time, expected_time)
        np.testing.assert_almost_equal(detrended_rri.mean(), 0)


from unittest import TestCase

import numpy as np

from hrv.detrend import polynomial_detrend, smoothness_priors, sg_detrend
from hrv.rri import RRi, RRiDetrended


class RRiDetrend(TestCase):
    def test_polynomial_detrend(self):
        fake_rri = RRi([810, 830, 860, 790, 804])

        detrended_rri = polynomial_detrend(fake_rri, degree=3)

        expected_rri = [4.12877839, -16.31947386, 25.77155567, -18.14773522, 4.56687502]
        np.testing.assert_almost_equal(detrended_rri, expected_rri)
        assert isinstance(detrended_rri, RRiDetrended)
        np.testing.assert_almost_equal(detrended_rri.time, fake_rri.time)
        np.testing.assert_almost_equal(detrended_rri.mean(), 0)

    def test_detrend_with_non_RRi_object(self):
        fake_rri = [810, 830, 860, 790, 804]

        detrended_rri = polynomial_detrend(fake_rri, degree=3)

        expected_rri = [4.12877839, -16.31947386, 25.77155567, -18.14773522, 4.56687502]
        expected_time = np.array([0.0, 0.83, 1.69, 2.48, 3.284])

        np.testing.assert_almost_equal(detrended_rri, expected_rri)
        assert isinstance(detrended_rri, RRiDetrended)
        np.testing.assert_almost_equal(detrended_rri.time, expected_time)
        np.testing.assert_almost_equal(detrended_rri.mean(), 0)

    def test_smoothness_priors_detrend(self):
        fake_rri = RRi([810, 830, 860, 790, 804])

        detrended_rri = smoothness_priors(fake_rri, l=500, fs=4.0)

        expected_rri = [
            -26.23170081,
            -29.47559322,
            -20.08889227,
            -3.08519233,
            16.52199257,
            33.71916077,
            43.4927445,
            40.8583971,
            24.76298922,
            2.00160447,
            -19.69858422,
            -32.61041193,
            -29.00663496,
            -1.15987915,
        ]
        np.testing.assert_almost_equal(detrended_rri, expected_rri, 4)
        assert isinstance(detrended_rri, RRiDetrended)
        assert detrended_rri.interpolated
        assert detrended_rri.detrended

    def test_savitzky_golay_detrend(self):
        fake_rri = RRi([810, 830, 860, 790, 804])

        detrended_rri = sg_detrend(fake_rri, window_length=3, polyorder=2)

        expected_rri = [
            2.2737368e-13,
            -3.4106051e-13,
            -3.4106051e-13,
            -3.4106051e-13,
            3.4106051e-13,
        ]
        expected_time = np.array([0.0, 0.83, 1.69, 2.48, 3.284])

        np.testing.assert_almost_equal(detrended_rri, expected_rri)
        assert isinstance(detrended_rri, RRiDetrended)
        np.testing.assert_almost_equal(detrended_rri.time, expected_time)
        np.testing.assert_almost_equal(detrended_rri.mean(), 0)

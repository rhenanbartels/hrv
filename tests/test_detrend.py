from unittest import TestCase

import numpy as np

from hrv.detrend import polynomial_detrend, smoothness_priors
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

    def test_smoothness_priors_detrend(self):
        fake_rri = RRi([810, 830, 860, 790, 804])

        detrended_rri = smoothness_priors(fake_rri, l=500, fs=4.0)

        expected_rri = [
             1.0998221e+01, 9.8113963e+00, 8.6277680e+00, 7.4537082e+00,
             6.2987969e+00, 5.1758828e+00, 4.1011555e+00, 3.0942070e+00,
             2.1780640e+00, 1.3791701e+00, 7.2731375e-01, 2.5552899e-01,
             7.7328588e+02, 7.9830030e+02
        ]
        np.testing.assert_almost_equal(detrended_rri, expected_rri, 4)
        assert isinstance(detrended_rri, RRiDetrended)
        assert detrended_rri.interpolated == True
        assert detrended_rri.detrended == True

from unittest import TestCase

import numpy as np

from hrv.detrend import polynomial_detrend
from hrv.rri import RRi


class RRiDetrend(TestCase):
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

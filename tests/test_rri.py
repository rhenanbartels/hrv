import numpy as np

from hrv.rri import RRi, _validate_rri
from tests.test_utils import FAKE_RRI


def test_transform_rri_to_numpy_array():
    validated_rri = _validate_rri(FAKE_RRI)
    np.testing.assert_array_equal(validated_rri, np.array(FAKE_RRI))


def test_transform_rri_in_seconds_to_miliseconds():
    rri_in_seconds = [0.8, 0.9, 1.2]

    validated_rri = _validate_rri(rri_in_seconds)

    assert isinstance(validated_rri, np.ndarray)
    np.testing.assert_array_equal(
            _validate_rri(rri_in_seconds),
            [800, 900, 1200]
    )


def test_rri_values():
    rri = RRi(FAKE_RRI).values

    assert isinstance(rri, np.ndarray)
    np.testing.assert_array_equal(rri, np.array(FAKE_RRI))

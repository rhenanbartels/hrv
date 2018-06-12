import numpy as np

from hrv.rri import RRi, _validate_rri, _create_time_array
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


def test_create_time_array():
    rri_time = _create_time_array(FAKE_RRI)

    assert isinstance(rri_time, np.ndarray)
    np.testing.assert_array_equal(rri_time, np.cumsum(FAKE_RRI) / 1000)


def test_rri_time_auto_creation():
    rri = RRi(FAKE_RRI)

    np.testing.assert_array_equal(rri.time, np.cumsum(FAKE_RRI) / 1000.0)


def test_rri_time_passed_as_argument():
    rri_time = np.cumsum(FAKE_RRI) / 1000.0
    rri = RRi(FAKE_RRI, rri_time)

    assert isinstance(rri.time, np.ndarray)
    np.testing.assert_array_equal(rri.time, np.cumsum(FAKE_RRI) / 1000.0)

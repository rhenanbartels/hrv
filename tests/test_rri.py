from collections import MutableMapping

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pytest

from hrv.rri import (RRi,
                     _validate_rri,
                     _create_time_array,
                     _validate_time,
                     _prepare_table)
from tests.test_utils import FAKE_RRI


class TestRRiClassArguments:
    def test_transform_rri_to_numpy_array(self):
        validated_rri = _validate_rri(FAKE_RRI)
        np.testing.assert_array_equal(validated_rri, np.array(FAKE_RRI))

    def test_transform_rri_in_seconds_to_miliseconds(self):
        rri_in_seconds = [0.8, 0.9, 1.2]

        validated_rri = _validate_rri(rri_in_seconds)

        assert isinstance(validated_rri, np.ndarray)
        np.testing.assert_array_equal(
                _validate_rri(rri_in_seconds),
                [800, 900, 1200]
        )

    def test_rri_values(self):
        rri = RRi(FAKE_RRI).values

        assert isinstance(rri, np.ndarray)
        np.testing.assert_array_equal(rri, np.array(FAKE_RRI))

    def test_create_time_array(self):
        rri_time = _create_time_array(FAKE_RRI)

        assert isinstance(rri_time, np.ndarray)
        expected = np.cumsum(FAKE_RRI) / 1000
        expected -= expected[0]
        np.testing.assert_array_equal(rri_time, expected)

    def test_rri_time_auto_creation(self):
        rri = RRi(FAKE_RRI)
        expected = np.cumsum(FAKE_RRI) / 1000
        expected -= expected[0]

        np.testing.assert_array_equal(
            rri.time,
            expected
        )

    def test_rri_time_passed_as_argument(self):
        rri_time = [1, 2, 3, 4]
        rri = RRi(FAKE_RRI, rri_time)

        assert isinstance(rri.time, np.ndarray)
        np.testing.assert_array_equal(rri.time, np.array([1, 2, 3, 4]))

    def test_raises_exception_if_rri_and_time_havent_same_length(self):
        with pytest.raises(ValueError) as e:
            _validate_time(FAKE_RRI, [1, 2, 3])

        with pytest.raises(ValueError):
            RRi(FAKE_RRI, [1, 2, 3])

        assert e.value.args[0] == (
                'rri and time series must have the same length')

    def test_rri_and_time_have_same_length_in_class_construction(self):
        rri = RRi(FAKE_RRI, [1, 2, 3, 4])

        np.testing.assert_array_equal(rri.time, np.array([1, 2, 3, 4]))

    def test_time_has_no_zero_value_besides_in_first_position(self):
        with pytest.raises(ValueError) as e:
            _validate_time(FAKE_RRI, [1, 2, 0, 3])

        assert e.value.args[0] == (
                'time series cannot have 0 values after first position')

    def test_time_is_monotonically_increasing(self):
        with pytest.raises(ValueError) as e:
            _validate_time(FAKE_RRI, [0, 1, 4, 3])

        assert e.value.args[0] == (
                'time series must be monotonically increasing'
        )

    def test_time_series_have_no_negative_values(self):
        with pytest.raises(ValueError) as e:
            _validate_time(FAKE_RRI, [-1, 1, 2, 3])

        assert e.value.args[0] == ('time series cannot have negative values')

    def test_rri_series_have_no_negative_values(self):
        with pytest.raises(ValueError) as e:
            _validate_rri([0.0, 1.0, 2.0, 3.0])

        with pytest.raises(ValueError):
            _validate_rri([1.0, 2.0, -3.0, 4.0])

        assert e.value.args[0] == ('rri series can only have positive values')

    def test_rri_class_encapsulation(self):
        rri = RRi(FAKE_RRI)

        with pytest.raises(AttributeError):
            rri.rri = [1, 2, 3, 4]

        with pytest.raises(AttributeError):
            rri.time = [1, 2, 3, 4]

    def test__getitem__method(self):
        rri = RRi(FAKE_RRI)

        rri_slice = rri[:2]
        expected = RRi([800, 810])

        assert isinstance(rri_slice, RRi)
        np.testing.assert_equal(rri_slice.values, expected.values)
        np.testing.assert_equal(rri_slice.time, expected.time)

    def test__getitem_method_integer_position(self):
        # To not break the numpy API (i.e np.sum(rri)) when index is an
        # integer RRi __getitem__ method returns a numpy.float64
        rri = RRi(FAKE_RRI)

        rri_pos_index = rri[0]
        expected = 800

        assert isinstance(rri_pos_index, np.float64)
        np.testing.assert_equal(rri_pos_index, expected)

    def test_class_repr_short_array(self):
        rri = RRi([1, 2, 3, 4])

        assert rri.__repr__() == 'RRi array([1000., 2000., 3000., 4000.])'

    def test_class_repr_long_array(self):
        rri = RRi(range(1, 100000))

        assert rri.__repr__() == (
                'RRi array([1.0000e+00, 2.0000e+00, 3.0000e+00, ..., '
                '9.9997e+04, 9.9998e+04,\n       9.9999e+04])'
        )

    def test__mul__method(self):
        rri = RRi(FAKE_RRI)

        result = rri * 10
        expected = [8000, 8100, 8150, 7500]

        assert isinstance(result, RRi)
        np.testing.assert_equal(result.values, expected)

    def test__add__method(self):
        rri = RRi(FAKE_RRI)

        result = rri + 10
        expected = [810, 820, 825, 760]

        assert isinstance(result, RRi)
        np.testing.assert_equal(result.values, expected)

    def test__sub__method(self):
        rri = RRi(FAKE_RRI)

        result = rri - 10
        expected = [790, 800, 805, 740]

        assert isinstance(result, RRi)
        np.testing.assert_equal(result.values, expected)

    def test__truediv__method(self):
        rri = RRi(FAKE_RRI)

        result = rri / 10
        expected = np.array(FAKE_RRI) / 10

        assert isinstance(result, RRi)
        np.testing.assert_equal(result.values, expected)

    # TODO: make RRi class accept negative values and fix this test
    def test__abs__method(self):
        rri = RRi(FAKE_RRI)

        result = abs(rri)
        expected = np.array(FAKE_RRI)

        assert isinstance(result, RRi)
        np.testing.assert_equal(result.values, expected)

    def test__eq__method(self):
        rri = RRi(FAKE_RRI)

        result = rri == 810

        np.testing.assert_equal(result, rri.values == 810)

    def test__ne__method(self):
        rri = RRi(FAKE_RRI)

        result = rri != 810

        np.testing.assert_equal(result, rri.values != 810)

    def test__gt__method(self):
        rri = RRi(FAKE_RRI)

        result = rri > 810

        np.testing.assert_equal(result, rri.values > 810)

    def test__ge__method(self):
        rri = RRi(FAKE_RRI)

        result = rri >= 810

        np.testing.assert_equal(result, rri.values >= 810)

    def test__lt__method(self):
        rri = RRi(FAKE_RRI)

        result = rri < 810

        np.testing.assert_equal(result, rri.values < 810)

    def test__le__method(self):
        rri = RRi(FAKE_RRI)

        result = rri <= 810

        np.testing.assert_equal(result, rri.values <= 810)

    def test__pow__method(self):
        rri = RRi(FAKE_RRI)

        result = rri ** 2
        expected = [640000., 656100., 664225., 562500.]

        np.testing.assert_equal(result.values, expected)

    def test_operations_with_other_rri_instance(self):
        rri = RRi(FAKE_RRI)
        another_rri = RRi([750, 765, 755, 742])

        mul_result = rri * another_rri
        div_result = rri / another_rri
        add_result = rri + another_rri
        sub_result = rri - another_rri
        pow_result = rri ** another_rri

        results = (mul_result, div_result, add_result, sub_result, pow_result)

        for result in results:
            assert isinstance(result, RRi)


class TestRRiClassMethods:
    def test_rri_statistical_values(self):
        rri = RRi(FAKE_RRI)

        np.testing.assert_array_equal(rri.mean(),  np.mean(FAKE_RRI))
        np.testing.assert_array_equal(rri.var(),  np.var(FAKE_RRI))
        np.testing.assert_array_equal(rri.std(),  np.std(FAKE_RRI))
        np.testing.assert_array_equal(rri.median(),  np.median(FAKE_RRI))
        np.testing.assert_array_equal(rri.max(),  np.max(FAKE_RRI))
        np.testing.assert_array_equal(rri.min(),  np.min(FAKE_RRI))
        np.testing.assert_array_equal(
                rri.amplitude(),
                np.max(FAKE_RRI) - np.min(FAKE_RRI),
        )
        np.testing.assert_array_equal(
                rri.rms(),
                np.sqrt(np.mean(np.square(FAKE_RRI))),
        )

    def test_prepare_rri_description_table(self):
        rri = RRi(FAKE_RRI)

        descr_table = _prepare_table(rri)
        expected = [
                ['', 'rri', 'hr'],
                ['min', 750.0, 73.61963190184049],
                ['max', 815.0, 80.0],
                ['amplitude', 65.0, 6.380368098159508],
                ['mean', 793.75, 75.67342649397864],
                ['median', 805.0, 74.53703703703704],
                ['var', 667.1875, 6.487185483887203],
                ['std', 25.829972899714782, 2.546995383562209],
        ]

        for row in descr_table:
            assert row in expected

    def test_rri_describe(self):
        rri = RRi(FAKE_RRI)
        rri_descr = rri.describe()

        assert isinstance(rri_descr, MutableMapping)
        expected = [
                ['', 'rri', 'hr'],
                ['min', 750.0, 73.61963190184049],
                ['max', 815.0, 80.0],
                ['amplitude', 65.0, 6.380368098159508],
                ['mean', 793.75, 75.67342649397864],
                ['median', 805.0, 74.53703703703704],
                ['var', 667.1875, 6.487185483887203],
                ['std', 25.829972899714782, 2.546995383562209],
        ]
        expected__repr__ = (
                '----------------------------------------\n',
                '                   rri          hr\n',
                '----------------------------------------\n',
                'min             750.00       73.62\n',
                'max             815.00       80.00\n',
                'mean            793.75       75.67\n',
                'var             667.19        6.49\n',
                'std              25.83        2.55\n',
                'median          805.00       74.54\n',
                'amplitude        65.00        6.38\n'
        )

        for field in expected[1:]:
            assert rri_descr[field[0]]['rri'] == field[1]
            assert rri_descr[field[0]]['hr'] == field[2]

        rri_descr_rep = rri_descr.__repr__()
        for table_row in expected__repr__:
            assert table_row in rri_descr_rep

    def test_rri_to_heart_rate(self):
        rri = RRi(FAKE_RRI)
        heart_rate = rri.to_hr()
        expected = np.array([75., 74.07407407, 73.6196319, 80.])

        np.testing.assert_array_almost_equal(heart_rate, expected)

    def test_get_rri_time_interval(self):
        rri = RRi(FAKE_RRI + [817, 785, 910], time=[2, 4, 6, 8, 10, 12, 14])

        rri_interval = rri.time_range(start=10, end=14)
        expected = RRi([817, 785, 910], time=[10, 12, 14])

        assert isinstance(rri_interval, RRi)
        np.testing.assert_array_equal(rri_interval.values, expected.values)
        np.testing.assert_array_equal(rri_interval.time, expected.time)

    def test_reset_time_offset(self):
        rri = RRi(FAKE_RRI, time=[4, 5, 6, 7])

        rri_reset = rri.reset_time()
        expected = RRi(FAKE_RRI, time=[0, 1, 2, 3])

        assert isinstance(rri_reset, RRi)
        np.testing.assert_array_equal(rri_reset.values, expected.values)
        np.testing.assert_array_equal(rri_reset.time, expected.time)

    def test_reset_time_offset_inplace(self):
        rri = RRi(FAKE_RRI, time=[4, 5, 6, 7])

        rri.reset_time(inplace=True)
        expected = RRi(FAKE_RRI, time=[0, 1, 2, 3])

        assert isinstance(rri, RRi)
        np.testing.assert_array_equal(rri.values, expected.values)
        np.testing.assert_array_equal(rri.time, expected.time)


class TestRRiPlotMethods:
    def test_return_figure_objects(self):
        rri = RRi(FAKE_RRI, time=[4, 5, 6, 7])

        fig, ax = rri.plot()

        assert isinstance(fig, matplotlib.figure.Figure)
        assert isinstance(ax, matplotlib.figure.Axes)

    def test_use_already_created_axes_object(self):
        fig, ax = plt.subplots(1, 1)
        rri = RRi(FAKE_RRI, time=[4, 5, 6, 7])

        rri.plot(ax=ax)

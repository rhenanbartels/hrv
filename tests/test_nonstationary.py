from unittest import mock

import pytest
import matplotlib

from hrv.rri import RRi
from hrv.sampledata import load_rest_rri
from hrv.nonstationary import TimeVarying, time_varying


class TestTimeVarying:
    def setUp(self):
        self.results = [
            {
                'rmssd': 30,
                'sdnn': 52,
                'sdsd': 30,
                'nn50': 2,
                'pnn50': 6,
                'mrri': 1003,
                'mhr': 59,
            },
            {
                'rmssd': 31,
                'sdnn': 53,
                'sdsd': 31,
                'nn50': 3,
                'pnn50': 7,
                'mrri': 1004,
                'mhr': 60,
            },
        ]
        self.rri_segments = [
            RRi([810, 800, 815], time=[1, 2, 3]),
            RRi([810, 800, 815], time=[4, 5, 6]),
        ]

    def test_happy_path_results(self):
        rri = load_rest_rri()

        tv_results = time_varying(rri, seg_size=30, overlap=0)
        expected_keys = [
            'rmssd',
            'sdnn',
            'sdsd',
            'nn50',
            'pnn50',
            'mrri',
            'mhr'
        ]

        assert isinstance(tv_results, TimeVarying)
        assert list(tv_results.transponsed.keys()) == expected_keys 
        assert len(tv_results.results) == 32  # number of segments

    def test_index_property(self):
        tv = TimeVarying(self.results, self.rri_segments)

        assert tv.rmssd == [30, 31]
        assert tv.sdnn == [52, 53]
        assert tv.sdsd == [30, 31]
        assert tv.nn50 == [2, 3]
        assert tv.pnn50 == [6, 7]
        assert tv.mrri == [1003, 1004]
        assert tv.mhr == [59, 60]
        with pytest.raises(ValueError):
            tv.dontexist

    def test_plot_time_varying_index(self):
        tv = TimeVarying(self.results, self.rri_segments)
        with mock.patch("hrv.nonstationary.plt.show"):
            fig, ax = tv.plot(index="rmssd")

        assert isinstance(fig, matplotlib.figure.Figure)
        assert isinstance(ax, matplotlib.figure.Axes)

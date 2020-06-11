from hrv.sampledata import load_rest_rri
from hrv.nonstationary import TimeVarying, time_varying


class TestTimeVarying:
    def test_happy_path_results(self):
        rri = load_rest_rri()

        results = time_varying(rri, seg_size=30, overlap=0)

        assert isinstance(results, TimeVarying)

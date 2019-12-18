import os

from hrv.io import read_from_text


def load_sample_data(filename):
    here = os.path.dirname(__file__)
    complete_path = os.path.join(here, filename)
    return read_from_text(complete_path)

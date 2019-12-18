import os

from hrv.io import read_from_text, read_from_hrm


def load_sample_data(filename):
    extension = os.path.splitext(filename)[1]
    handler = {'.txt': read_from_text, '.hrm': read_from_hrm}

    here = os.path.dirname(__file__)
    complete_path = os.path.join(here, filename)
    return handler[extension](complete_path)


def load_rest_rri():
    return load_sample_data('rest_rri.txt')


def load_exercise_rri():
    return load_sample_data('exercise_rri.hrm')

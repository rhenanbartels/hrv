import os

from hrv.io import read_from_text, read_from_hrm


def load_sample_data(filename):
    """
    Parameters
    ----------
    filename : string
         file name of the sample RRi data

    Load RRi series from files with .txt or .hrm extension

    See `hrv.io.read_from_text` and `hrv.io.read_from_hrm` for more information

    Example
    -------
        rri = load_sample_data('rest_rri.txt')
    """
    extension = os.path.splitext(filename)[1]
    handler = {".txt": read_from_text, ".hrm": read_from_hrm}

    here = os.path.dirname(__file__)
    complete_path = os.path.join(here, filename)
    return handler[extension](complete_path)


def load_rest_rri():
    """
    Load RRi series of a subject collected during rest with approximately 900s
    (15 minutes) in the supine position.
    Appearently, this series has no ectopic beat. All RR values were originated
    in the sinusal node.

    Example
    -------
    >>> from hrv.sampledata import load_rest_rri
    >>> load_rest_rri()
    RRi array([1114., 1113., ..., 1066., 1119.])
    """
    return load_sample_data("rest_rri.txt")


def load_exercise_rri():
    """
    Load a RRi series of subject during submaximal exercise in a bicycle.
    The whole signal comprehends three phases:
        1 - Approximetaly 300s (5 minutes) pre-exercise rest seated in the
            bycicle
        2 - Approximetaly 1800s (30 minutes) of submaximal exercise
        3 - Approximetaly 300s (5 minutes) of passive recovery. The subject was
            sitting in the bicycle

    There are some ectopic beats in this RRi series. See `hrv.filters` to
    removed them

    Example
    -------
    >>> from hrv.sampledata import load_exercise_rri
    >>> load_exercise_rri()
    RRi array([1589.,  783.,  752., ...,  562.,  555.,  557.])
    """
    return load_sample_data("exercise_rri.hrm")


def load_noisy_rri():
    """
    Load a RRi series of subject during submaximal exercise in a bicycle with
    many ectopic beats.
    The whole signal comprehends three phases:
        1 - Approximetaly 300s (5 minutes) pre-exercise rest seated in the
            bycicle
        2 - Approximetaly 1800s (30 minutes) of submaximal exercise
        3 - Approximetaly 300s (5 minutes) of passive recovery. The subject was
            sitting in the bicycle

    This signal is good to try the filters provided by the 'hrv' module
    in the 'hrv.filters'

    Example
    -------
    >>> from hrv.sampledata import load_noisy_rri
    >>> load_noisy_rri()
    RRi array([904., 913., 937., ..., 704., 805., 808.])
    """
    return load_sample_data("noisy_rri.hrm")

import numpy as np


class RRi:
    def __init__(self, rri, time=None):
        self.rri = _validate_rri(rri)
        if time is None:
            self.time = _create_time_array(self.rri)
        else:
            self.time = np.array(time)

    @property
    def values(self):
        return self.rri


def _validate_rri(rri):
    rri = np.array(rri)

    # Use RRi series median value to check if it is in seconds or miliseconds
    if np.median(rri) < 10:
        rri *= 1000.0

    return rri


def _validate_time(rri, time):
    if len(rri) != len(time):
        raise ValueError('rri and time series must have the same length')


def _create_time_array(rri):
    return np.cumsum(rri) / 1000.0

import numpy as np


class RRi:
    def __init__(self, rri, time=None):
        self.__rri = _validate_rri(rri)
        if time is None:
            self.__time = _create_time_array(self.rri)
        else:
            self.__time = _validate_time(self.rri, time)

    def __len__(self):
        return len(self.__rri)

    def __getitem__(self, position):
        return self.__rri[position]

    @property
    def values(self):
        return self.rri

    @property
    def rri(self):
        return self.__rri

    @property
    def time(self):
        return self.__time

    def mean(self):
        return np.mean(self.rri)

    def var(self):
        return np.var(self.rri)

    def std(self):
        return np.std(self.rri)

    def median(self):
        return np.median(self.rri)

    def max(self):
        return np.max(self.rri)

    def min(self):
        return np.min(self.rri)

    def amplitude(self):
        return self.max() - self.min()

    def rms(self):
        return np.sqrt(np.mean(self.rri ** 2))


def _validate_rri(rri):
    rri = np.array(rri, dtype=np.float64)

    if any(rri <= 0):
        raise ValueError('rri series can only have positive values')

    # Use RRi series median value to check if it is in seconds or miliseconds
    if np.median(rri) < 10:
        rri *= 1000.0

    return rri


def _validate_time(rri, time):
    time = np.array(time, dtype=np.float64)
    if len(rri) != len(time):
        raise ValueError('rri and time series must have the same length')

    if any(time[1:] == 0):
        raise ValueError(
                'time series cannot have 0 values after first position'
        )

    if not all(np.diff(time) > 0):
        raise ValueError('time series must be monotonically increasing')

    if any(time < 0):
        raise ValueError('time series cannot have negative values')

    return time


def _create_time_array(rri):
    return np.cumsum(rri) / 1000.0

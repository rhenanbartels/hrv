import sys

from collections import MutableMapping, defaultdict

import matplotlib.pyplot as plt
import numpy as np


# TODO: create InterpolatedRRi and DetrendedRRi classes
class RRi:
    def __init__(self, rri, time=None):
        self.__rri = _validate_rri(rri)
        if time is None:
            self.__time = _create_time_array(self.rri)
        else:
            self.__time = _validate_time(self.__rri, time)

    def __len__(self):
        return len(self.__rri)

    def __getitem__(self, position):
        if isinstance(position, (slice, np.ndarray)):
            return RRi(self.__rri[position], self.time[position])
        else:
            return self.__rri[position]

    @property
    def values(self):
        return self.__rri

    @property
    def rri(self):
        return self.__rri

    @property
    def time(self):
        return self.__time

    def describe(self):
        table = _prepare_table(RRi(self.rri))
        rri_descr = RRiDescription(table)
        for row in table[1:]:
            rri_descr[row[0]]['rri'] = row[1]
            rri_descr[row[0]]['hr'] = row[2]

        return rri_descr

    def info(self):
        def _mem_usage(nbytes):
            mem_val = nbytes / 1024
            if mem_val < 1000:
                mem_str = '{:.2f}Kb'.format(mem_val)
            else:
                mem_str = '{:.2f}Mb'.format(mem_val / 1024)

            return mem_str

        n_points = self.__rri.size
        duration = self.__time[-1]
        # Hard coded interp and detrended. Future versions will have proper
        # attributes
        interp = False
        detrended = False
        mem_usage = _mem_usage(self.__rri.nbytes)

        msg_template = 'N Points: {n_points}\nDuration: {duration:.2f}s\n'\
                       'Interpolated: {interp}\nDetrended: {detrended}\n'\
                       'Memory Usage: {mem_usage}'
        sys.stdout.write(msg_template.format(
            n_points=n_points,
            duration=duration,
            interp=interp,
            detrended=detrended,
            mem_usage=mem_usage
        ))

    def to_hr(self):
        return 60 / (self.rri / 1000.0)

    def time_range(self, start, end):
        interval = np.logical_and(self.time >= start, self.time <= end)
        return RRi(self.rri[interval], time=self.time[interval])

    def reset_time(self, inplace=False):
        if inplace:
            self.__time -= self.time[0]
        else:
            return RRi(self.rri, time=self.time-self.time[0])

    def plot(self, ax=None, *args, **kwargs):
        fig = None
        if ax is None:
            fig, ax = plt.subplots(1, 1)

        ax.plot(self.time, self.rri, *args, **kwargs)
        ax.set(xlabel='Time (s)', ylabel='RRi (ms)')
        plt.show(block=False)

        return fig, ax

    def hist(self, hr=False, *args, **kwargs):
        fig, ax = plt.subplots(1, 1)
        if hr:
            ax.hist(self.to_hr(), *args, **kwargs)
            ax.set(xlabel='HR (bpm)', ylabel='Frequency')
        else:
            ax.hist(self.rri, *args, **kwargs)
            ax.set(xlabel='RRi (ms)', ylabel='Frequency')

        plt.show(block=False)

    # TODO: Create methods for time domain to be calculted in the instance

    def mean(self, *args, **kwargs):
        return np.mean(self.rri, *args, **kwargs)

    def var(self, *args, **kwargs):
        return np.var(self.rri, *args, **kwargs)

    def std(self, *args, **kwargs):
        return np.std(self.rri, *args, **kwargs)

    def median(self, *args, **kwargs):
        return np.median(self.rri, *args, **kwargs)

    def max(self, *args, **kwargs):
        return np.max(self.rri, *args, **kwargs)

    def min(self, *args, **kwargs):
        return np.min(self.rri, *args, **kwargs)

    def amplitude(self):
        return self.max() - self.min()

    def rms(self):
        return np.sqrt(np.mean(self.rri ** 2))

    def __repr__(self):
        return 'RRi %s' % np.array_repr(self.rri)

    def __mul__(self, val):
        return RRi(self.rri * val, self.time)

    def __add__(self, val):
        return RRi(self.rri + val, self.time)

    def __sub__(self, val):
        return RRi(self.rri - val, self.time)

    def __truediv__(self, val):
        return RRi(self.rri / val, self.time)

    def __pow__(self, val):
        return RRi(self.rri ** val, self.time)

    def __abs__(self):
        return RRi(np.abs(self.rri), self.time)

    def __eq__(self, val):
        return self.rri == val

    def __ne__(self, val):
        return self.rri != val

    def __gt__(self, val):
        return self.rri > val

    def __ge__(self, val):
        return self.rri >= val

    def __lt__(self, val):
        return self.rri < val

    def __le__(self, val):
        return self.rri <= val


class RRiDescription(MutableMapping):
    def __init__(self, table, *args, **kwargs):
        self.store = defaultdict(dict)
        self.update(dict(*args, **kwargs))
        self.table = table

    def keys(self):
        return self.store.keys()

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __repr__(self):
        descr = ""
        dash = '-' * 40 + "\n"
        for i in range(len(self.table)):
            if i == 0:
                descr += dash
                descr += '{:<10s}{:>12s}{:>12s}\n'.format(
                    self.table[i][0], self.table[i][1], self.table[i][2]
                )
                descr += dash
            else:
                descr += '{:<10s}{:>12.2f}{:>12.2f}\n'.format(
                    self.table[i][0], self.table[i][1], self.table[i][2]
                )

        return descr


def _prepare_table(rri):
    def _amplitude(values):
        return values.max() - values.min()

    header = ['', 'rri', 'hr']
    fields = ['min', 'max', 'mean', 'var', 'std']
    hr = rri.to_hr()

    table = []
    for field in fields:
        rri_var = rri.__getattribute__(field)()
        hr_var = hr.__getattribute__(field)()
        table.append([field, rri_var, hr_var])

    table.append(['median', rri.median(), np.median(hr)])
    table.append(['amplitude', rri.amplitude(), _amplitude(hr)])

    return [header] + table


def _validate_rri(rri):
    # TODO: let the RRi be in seconds if the user wants to
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
    time = np.cumsum(rri) / 1000.0
    return time - time[0]

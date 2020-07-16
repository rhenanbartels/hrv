"""
Objects for dealing with RR intervals series (RRi).

This module offers two classes to represent RRi series as Python objects which
brings widely used methods to extract information from tachograms.
Once RRi or RRiDetrended are instanciated is it possible to calculate simple
descriptive statistics of the RRi series, such: average, median, etc. It is
also possible to visualize the series with the plot method, extract a smaller
segment of the RRi series based on time information

Classes
------
 - `RRi` -- RRi series class
 - `RRiDetrended` -- detrended RRi values
"""

import sys
from collections import MutableMapping, defaultdict

import matplotlib.pyplot as plt
import numpy as np

from .utils import _ellipsedraw

__all__ = ['RRi', 'RRiDetrended']


class RRi:
    """An RRi series class.

       The RRi class provides magic methods that make it instance behave like
       a Python iterable. It also has methods that help to describe the
       statistical properties of the instantiated RRi series and for
       visualization purpose.

       This class performs simple validation of the provided rri values:
            - it can not have negative values
            - if the median values are smaller than 10, it is presumed they
              are in seconds and are transformed into miliseconds
       If time information, which is optional, is provided it is also
       validated:
            - time array must have the same length as the RRi series
            - must be monotonically increasing
            - no negative values
            - only the first value can be zero

        When time information is not provided it will be created with the
        cumulative sum of the RRi values:
            time = np.cumsum(rri) / 1000.0
            time -= time[0]  # to start at zero

        Time is represented in seconds
    """

    def __init__(self, rri, time=None, *args, **kwargs):
        if not isinstance(self, RRiDetrended):
            self.__rri = _validate_rri(rri)
            self.__detrended = False
            self.__interpolated = False
        else:
            self.__rri = np.array(rri)
            self.__detrended = kwargs.pop("detrended")
            self.__interpolated = kwargs.pop("interpolated", False)

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
        """Return a numpy array containing the RRi values"""
        return self.__rri

    @property
    def rri(self):
        """Return a numpy array containing the RRi values"""
        return self.__rri

    @property
    def time(self):
        """Return a numpy array containing the time information"""
        return self.__time

    @property
    def detrended(self):
        """Return if the RRi series is detrended"""
        return self.__detrended

    @property
    def interpolated(self):
        """Return if the RRi series is interpolated"""
        return self.__interpolated

    def describe(self):
        """
        Return a dictionary containing descriptive statistics from the RRi
        series.
        """
        table = _prepare_table(RRi(self.rri))
        rri_descr = RRiDescription(table)
        for row in table[1:]:
            rri_descr[row[0]]["rri"] = row[1]
            rri_descr[row[0]]["hr"] = row[2]

        return rri_descr

    def info(self):
        """
        Print information about RRi`s memory usage, length,
        number of intervals, and if it is interpolated and/or detrended
        """

        def _mem_usage(nbytes):
            mem_val = nbytes / 1024
            if mem_val < 1000:
                mem_str = "{:.2f}Kb".format(mem_val)
            else:
                mem_str = "{:.2f}Mb".format(mem_val / 1024)

            return mem_str

        n_points = self.__rri.size
        duration = self.__time[-1] - self.__time[0]
        # Hard coded interp and detrended. Future versions will have proper
        # attributes
        mem_usage = _mem_usage(self.__rri.nbytes)

        msg_template = (
            "N Points: {n_points}\nDuration: {duration:.2f}s\n"
            "Interpolated: {interp}\nDetrended: {detrended}\n"
            "Memory Usage: {mem_usage}"
        )
        sys.stdout.write(
            msg_template.format(
                n_points=n_points,
                duration=duration,
                interp=self.interpolated,
                detrended=self.detrended,
                mem_usage=mem_usage,
            )
        )

    def to_hr(self):
        """
        Return a numpy array containing the heart rate calculated with
        the RRi series
        """
        return 60 / (self.rri / 1000.0)

    def time_range(self, start, end):
        """
        Crop the RRi series based in time information

        Parameters
        ----------
        start : float
            beginning of the new RRi series

        end : float
            end of the new RRi series
        """
        interval = np.logical_and(self.time >= start, self.time <= end)
        return RRi(self.rri[interval], time=self.time[interval])

    def reset_time(self, inplace=False):
        """
        Reset time information to force it starting from zero

        Parameters
        ----------
        inplace : boolean, default False
            If true, time information of the current RRi series will be reset
        """
        if inplace:
            self.__time -= self.time[0]
        else:
            return RRi(self.rri, time=self.time - self.time[0])

    def plot(self, ax=None, *args, **kwargs):
        """
        Plot RRi series

        Parameters
        ----------
        ax : matplotlib axes object, default None
        """
        fig = None
        if ax is None:
            fig, ax = plt.subplots(1, 1)

        ax.plot(self.time, self.rri, *args, **kwargs)
        ax.set(xlabel="Time (s)", ylabel="RRi (ms)")
        plt.show(block=False)

        return fig, ax

    def hist(self, hr=False, *args, **kwargs):
        """
        Plot the histogram of the RRi series

        Parameters
        ----------
        hr : boolean, optional
            If true, the histogram of the heart rate is depicted
        """
        fig, ax = plt.subplots(1, 1)
        if hr:
            ax.hist(self.to_hr(), *args, **kwargs)
            ax.set(xlabel="HR (bpm)", ylabel="Frequency")
        else:
            ax.hist(self.rri, *args, **kwargs)
            ax.set(xlabel="RRi (ms)", ylabel="Frequency")

        plt.show(block=False)

        return fig, ax

    def poincare_plot(self):
        """
        Poincaré plot of the RRi series
        """
        fig, ax = plt.subplots(1, 1)
        rri_n, rri_n_1 = self.rri[:-1], self.rri[1:]
        ax.plot(rri_n, rri_n_1, ".k")

        ax.set(xlabel="$RRi_n$ (ms)", ylabel="$RRi_{n+1}$ (ms)", title="Poincaré Plot")

        plt.show(block=False)

        # The ellipse drawning is a translation from the Matlab code
        # available at: https://github.com/jramshur/HRVAS

        dx = abs(max(rri_n) - min(rri_n)) * 0.05
        dy = abs(max(rri_n_1) - min(rri_n_1)) * 0.05
        xlim = [min(rri_n) - dx, max(rri_n) + dx]
        ylim = [min(rri_n_1) - dy, max(rri_n_1) + dy]

        from hrv.classical import non_linear

        nl = non_linear(self.rri)
        a = rri_n / np.cos(np.pi / 4.0)
        ca = np.mean(a)

        cx, cy, _ = ca * np.cos(np.pi / 4.0), ca * np.sin(np.pi / 4.0), 0

        width = nl["sd2"]  # to seconds
        height = nl["sd1"]  # to seconds

        # plot fx(x) = x
        sd2_l = ax.plot(
            [xlim[0], xlim[1]], [ylim[0], ylim[1]], "--", color=[0.5, 0.5, 0.5]
        )
        fx = lambda val: -val + 2 * cx

        sd1_l = ax.plot([xlim[0], xlim[1]], [fx(xlim[0]), fx(xlim[1])], "k--")
        ax = _ellipsedraw(
            ax, width, height, cx, cy, np.pi / 4.0, color="r", linewidth=3
        )
        ax.legend(
            (sd1_l[0], sd2_l[0]), ("SD1: %.2fms" % height, "SD2: %.2fms" % width),
        )

        return fig, ax

    # TODO: Create methods for time domain to be calculted in the instance

    def mean(self, *args, **kwargs):
        """Return the average of the RRi series"""
        return np.mean(self.rri, *args, **kwargs)

    def var(self, *args, **kwargs):
        """Return the variance of the RRi series"""
        return np.var(self.rri, *args, **kwargs)

    def std(self, *args, **kwargs):
        """Return the standard deviation of the RRi series"""
        return np.std(self.rri, *args, **kwargs)

    def median(self, *args, **kwargs):
        """Return the median of the RRi series"""
        return np.median(self.rri, *args, **kwargs)

    def max(self, *args, **kwargs):
        """Return the max value of the RRi series"""
        return np.max(self.rri, *args, **kwargs)

    def min(self, *args, **kwargs):
        """Return the min value of the RRi series"""
        return np.min(self.rri, *args, **kwargs)

    def amplitude(self):
        """Return the amplitude (max - min) of the RRi series"""
        return self.max() - self.min()

    def rms(self):
        """Return the root mean squared of the RRi series"""
        return np.sqrt(np.mean(self.rri ** 2))

    def time_split(self, seg_size, overlap=0, keep_last=False):
        """
        Splits the RRi series in smaller segments with approximately
        the same time duration.

        Parameters
        ----------
        seg_size : Number
            The segment size in seconds
        overlap : Number, optional
            The size of overlap between adjacents segments, defaults to 0
        keep_last : boolean, optional
            If set to True the last segment is returned even if smaller than
            `seg_size`, defaults to False
        """
        rri_duration = self.time[-1]
        if overlap > seg_size:
            raise Exception("`overlap` can not be bigger than `seg_size`")
        elif seg_size > rri_duration:
            raise Exception("`seg_size` is longer than RRi duration.")

        begin = 0
        end = seg_size
        step = seg_size - overlap
        n_splits = int((rri_duration - seg_size) / step) + 1
        segments = []
        for i in range(n_splits):
            OP = np.less if i + 1 != n_splits else np.less_equal
            mask = np.logical_and(self.time >= begin, OP(self.time, end))
            segments.append(RRi(self.rri[mask], time=self.time[mask]))
            begin += step
            end += step

        last = segments[-1]
        if keep_last and last.time[-1] < rri_duration:
            mask = self.time > begin
            segments.append(RRi(self.rri[mask], time=self.time[mask]))

        return segments

    def __repr__(self):
        return "RRi %s" % np.array_repr(self.rri)

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


class RRiDetrended(RRi):
    # TODO: add trend as attribute of the instance
    def __init__(self, rri, time, *args, **kwargs):
        detrended = True
        interpolated = kwargs.pop("interpolated", False)
        super().__init__(rri, time, interpolated=interpolated, detrended=detrended)


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
        dash = "-" * 40 + "\n"
        for i in range(len(self.table)):
            if i == 0:
                descr += dash
                descr += "{:<10s}{:>12s}{:>12s}\n".format(
                    self.table[i][0], self.table[i][1], self.table[i][2]
                )
                descr += dash
            else:
                descr += "{:<10s}{:>12.2f}{:>12.2f}\n".format(
                    self.table[i][0], self.table[i][1], self.table[i][2]
                )

        return descr


def _prepare_table(rri):
    def _amplitude(values):
        return values.max() - values.min()

    header = ["", "rri", "hr"]
    fields = ["min", "max", "mean", "var", "std"]
    hr = rri.to_hr()

    table = []
    for field in fields:
        rri_var = rri.__getattribute__(field)()
        hr_var = hr.__getattribute__(field)()
        table.append([field, rri_var, hr_var])

    table.append(["median", rri.median(), np.median(hr)])
    table.append(["amplitude", rri.amplitude(), _amplitude(hr)])

    return [header] + table


def _validate_rri(rri):
    # TODO: let the RRi be in seconds if the user wants to
    rri = np.array(rri, dtype=np.float64)

    if any(rri <= 0):
        raise ValueError("rri series can only have positive values")

    # Use RRi series median value to check if it is in seconds or miliseconds
    if np.median(rri) < 10:
        rri *= 1000.0

    return rri


def _validate_time(rri, time):
    time = np.array(time, dtype=np.float64)
    if len(rri) != len(time):
        raise ValueError("rri and time series must have the same length")

    if any(time[1:] == 0):
        raise ValueError("time series cannot have 0 values after first position")

    if not all(np.diff(time) > 0):
        raise ValueError("time series must be monotonically increasing")

    if any(time < 0):
        raise ValueError("time series cannot have negative values")

    return time


def _create_time_array(rri):
    time = np.cumsum(rri) / 1000.0
    return time - time[0]

import numpy as np


def moving_average(rri, order=3):
    return _moving_function(rri, order, np.mean)


def moving_median(rri, order=3):
    return _moving_function(rri, order, np.median)


def _moving_function(rri, order, func):
    offset = int(order / 2)

    filt_rri = np.array(rri.copy(), dtype=np.float64)
    for i in range(offset, len(rri) - offset, 1):
        filt_rri[i] = func(rri[i-offset:i+offset+1])

    return filt_rri

import numpy as np


def quotient(rri):
    rri = np.array(rri)
    L = len(rri) - 1

    indices = np.where(
            (rri[:L-1]/rri[1:L] < 0.8) | (rri[:L-1]/rri[1:L] > 1.2) |
            (rri[1:L]/rri[:L-1] < 0.8) | (rri[1:L]/rri[:L-1] > 1.2)
    )

    return np.delete(rri, indices)


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

import numpy as np


def moving_average(rri, order=3):
    weights = [1 / order] * order
    n_remove = int(order - 1)
    n_keep = int(order / 2)
    filt_raw = np.convolve(weights, rri)[n_remove:-n_remove]
    return np.concatenate((rri[:n_keep], filt_raw, rri[-n_keep:]))


def moving_median(rri, order=3):
    offset = int(order / 2)

    filt_rri = rri.copy()
    for i in range(offset, len(rri) - offset, 1):
        filt_rri[i] = np.median(rri[i-offset:i+offset+1])

    return filt_rri

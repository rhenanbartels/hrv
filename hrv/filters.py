import numpy as np


def moving_average(rri, order=3):
    weights = [1 / order] * order
    n_remove = int(order - 1)
    n_keep = int(order / 2)
    filt_raw = np.convolve(weights, rri)[n_remove:-n_remove]
    return np.concatenate((rri[:n_keep], filt_raw, rri[-n_keep:]))

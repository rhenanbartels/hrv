import numpy as np
from scipy.interpolate import CubicSpline

from hrv.rri import RRi
from hrv.utils import _create_time_info


def quotient(rri):
    # TODO: Receive option to replaced outliers with stats
    # functions (i.e mean, median etc)
    # TODO: Receive option to re-create time array with cumsum of filtered rri

    if isinstance(rri, RRi):
        rri_time = rri.time
        rri = rri.values
    else:
        rri = np.array(rri)
        rri_time = _create_time_info(rri)

    L = len(rri) - 1

    indices = np.where(
            (rri[:L-1]/rri[1:L] < 0.8) | (rri[:L-1]/rri[1:L] > 1.2) |
            (rri[1:L]/rri[:L-1] < 0.8) | (rri[1:L]/rri[:L-1] > 1.2)
    )

    rri_filt, time_filt = np.delete(rri, indices), np.delete(rri_time, indices)
    return RRi(rri_filt, time_filt)


def moving_average(rri, order=3):
    return _moving_function(rri, order, np.mean)


def moving_median(rri, order=3):
    return _moving_function(rri, order, np.median)


def threshold_filter(rri, threshold=250, local_median_size=5):
    # TODO: DRY
    if isinstance(rri, RRi):
        rri_time = rri.time
        rri = rri.values
    else:
        rri_time = _create_time_info(rri)

    # Filter strength inspired in Kubios guide
    strength = {
        'very low': 450,
        'low': 350,
        'medium': 250,
        'strong': 150,
        'very strong': 50,
    }
    threshold = strength[threshold] if threshold in strength else threshold

    n_rri = len(rri)
    rri_to_remove = []
    # Apply filter in the beginning later
    for j in range(local_median_size, n_rri):
        slice_ = slice(j-local_median_size, j)
        if rri[j] > (np.median(rri[slice_]) + threshold):
            rri_to_remove.append(j)

    first_idx = list(range(local_median_size + 1))
    for j in range(local_median_size):
        slice_ = [f for f in first_idx if not f == j]
        if abs(rri[j] - np.median(rri[slice_])) > threshold:
            rri_to_remove.append(j)

    rri_temp = [r for idx, r in enumerate(rri) if idx not in rri_to_remove]
    time_temp = [
        t for idx, t in enumerate(rri_time) if idx not in rri_to_remove
    ]
    cubic_spline = CubicSpline(time_temp, rri_temp)
    return RRi(cubic_spline(rri_time), rri_time)


def _moving_function(rri, order, func):
    if isinstance(rri, RRi):
        rri_time = rri.time
        rri = rri.values
    else:
        rri_time = _create_time_info(rri)

    offset = int(order / 2)

    # TODO: Implemente copy method for RRi class
    filt_rri = np.array(rri.copy(), dtype=np.float64)
    for i in range(offset, len(rri) - offset, 1):
        filt_rri[i] = func(rri[i-offset:i+offset+1])

    return RRi(filt_rri, rri_time)

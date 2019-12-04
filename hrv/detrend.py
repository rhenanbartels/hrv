import numpy as np
from scipy.interpolate import CubicSpline
from scipy.sparse import spdiags, dia_matrix

from hrv.rri import RRiDetrended, RRi, _create_time_array


def polynomial_detrend(rri, degree):
    if isinstance(rri, RRi):
        time = rri.time
        rri = rri.values
    else:
        time = _create_time_array(rri)

    coef = np.polyfit(time, rri, deg=degree)
    polynomial = np.polyval(coef, time)
    detrended_rri = rri - polynomial
    return RRiDetrended(detrended_rri, time=time)


def smoothness_priors(rri, l=500, fs=4.0):
    if isinstance(rri, RRi):
        time = rri.time
        rri = rri.values
    else:
        time = _create_time_array(rri)

    cubic_spline = CubicSpline(time, rri)
    time_interp = np.arange(time[0], time[-1], 1.0/fs)
    rri_interp = cubic_spline(time_interp)
    N = len(rri_interp)
    identity = np.eye(N)
    B = np.dot(np.ones((N-2, 1)), np.array([[1, -2, 1]]))
    offsets = [0, 1, 2]
    D_2 = dia_matrix((B.T, offsets), shape=(N-2, N))
    inv = np.linalg.inv(identity + l**2 * D_2.T @ D_2)
    z_stat = ((identity - np.linalg.inv(identity + l**2 * D_2.T @ D_2)))\
        @ rri_interp

    rri_interp_detrend = np.squeeze(np.asarray(rri_interp - z_stat))
    return RRiDetrended(
        rri_interp - rri_interp_detrend,
        time=time_interp,
        detrended=True,
        interpolated=True
    )

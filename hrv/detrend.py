import numpy as np

from hrv.rri import RRiDetrended


def polynomial_detrend(rri, degree):
    coef = np.polyfit(rri.time, rri.values, deg=degree)
    polynomial = np.polyval(coef, rri.time)
    detrended_rri = rri.values - polynomial
    return RRiDetrended(detrended_rri, time=rri.time)

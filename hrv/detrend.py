import numpy as np

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

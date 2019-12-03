import numpy as np


def polynomial_detrend(rri, degree):
    coef = np.polyfit(rri.time, rri.values, deg=degree)
    polynomial = np.polyval(coef, rri.time)
    return rri.values - polynomial

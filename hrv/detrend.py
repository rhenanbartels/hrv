import numpy as np
from scipy.interpolate import CubicSpline
from scipy.signal import savgol_filter
from scipy.sparse import spdiags, dia_matrix

from hrv.rri import RRiDetrended, RRi, _create_time_array


__all__ = ['polynomial_detrend', 'smoothness_priors', 'sg_detrend']


def polynomial_detrend(rri, degree=1):
    """
    Fits a polynomial function with degree=`degree` in the RRi series
    and then subtract it from the signal.

    Parameters
    ----------
    rri : array_like
        sequence containing the RRi series
    degree: integer, optional
        degree of the polynomial function to be fitted in the RRi series.
        Defaults to 1

    Returns
    -------
    results : RRi array
        instance of the RRi Detrended class containing the detrended RRi values

    See Also
    -------
    smoothness_priors, sg_detrend

    Examples
    --------
    >>> from hrv.detrend import polynomial_detrend
    >>> from hrv.sampledata import load_rest_rri
    >>> rri = load_rest_rri()
    >>> polynomial_detrend(rri)
    RRi array([ 5.60099763e+01,  5.50082903e+01, ..., 8.00667554e+00])
    """
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
    """
    Estimates the stationary part of the resampled RRi series and subtracts it
    from the signal. The RRi series must have equal time-space between
    adjacents RRi values, therefore the original RRi is interpolated and then
    resampled.

    Parameters
    ----------
    rri : array_like
        sequence containing the RRi series
    l: integer, optional
        the regularization parameter
        Defaults to 500
    fs: integer, optional
        sampling frequency in each the RRi series will be resampled after
        cubic interpolation. Defaults to 4

    .. math::
        The estimated stationary component of the RRi can represented as:
        z_stat = (I - (l**2 @ D2.T @ D2)**2) @ z

        where I is the identity matrix; D2 is the second order difference
        matrix and z is the evenly spaced RRi series (containing both
        stationaty and trend components)

    Returns
    -------
    results : RRi array
        instance of the RRi Detrended class containing the detrended RRi values

    See Also
    -------
    polynomial_detrend, sg_detrend

    References
    ----------
    - M.P.  Tarvainen,  P.O.  Ranta-aho  and  P.A.  Karjalainen,  An  advanced
      detrending  method  with  application  to  HRV  analysis, IEEE
      Transaction on Biomedical Engineering 49 (2002), 172–175.

    Examples
    --------
    >>> from hrv.detrend import smoothness_priors
    >>> from hrv.sampledata import load_rest_rri
    >>> rri = load_rest_rri()
    >>> smoothness_priors(rri)
    RRi array([27.17281349,   46.12837695,   51.21922892, ..., 1042.86845282])
    """
    if isinstance(rri, RRi):
        time = rri.time
        rri = rri.values
    else:
        time = _create_time_array(rri)

    # TODO: only interp if not interpolated yet
    cubic_spline = CubicSpline(time, rri)
    time_interp = np.arange(time[0], time[-1], 1.0 / fs)
    rri_interp = cubic_spline(time_interp)
    N = len(rri_interp)
    identity = np.eye(N)
    B = np.dot(np.ones((N - 2, 1)), np.array([[1, -2, 1]]))
    D_2 = dia_matrix((B.T, [0, 1, 2]), shape=(N - 2, N))
    inv = np.linalg.inv(identity + l ** 2 * D_2.T @ D_2)
    z_stat = ((identity - np.linalg.inv(identity + l ** 2 * D_2.T @ D_2))) @ rri_interp

    rri_interp_detrend = np.squeeze(np.asarray(rri_interp - z_stat))
    return RRiDetrended(
        rri_interp - rri_interp_detrend,
        time=time_interp,
        detrended=True,
        interpolated=True,
    )


def sg_detrend(rri, window_length=51, polyorder=3, *args, **kwargs):
    """
    Remove the low-frequency components of the RRi series with the low-pass
    filter developed by Savitzky-Golay

    Parameters
    ----------
    rri : array_like
        sequence containing the RRi series
    window_length: integer, optional
        The length of the filter window (i.e. the number of coefficients).
        `window_length` must be a positive odd integer. If `mode` is 'interp',
        `window_length` must be less than or equal to the size of `x`.
        Defaults to 51
    polyorder: integer, optional
        The order of the polynomial used to fit the samples.  `polyorder` must
        be less than `window_length`. Defauts to 3

    See scipy.signal.savgol_filter for more information

    Returns
    -------
    results : RRi array
        instance of the RRi Detrended class containing the detrended RRi values

    See Also
    -------
    polynomial_detrend, smoothness_priors

    Examples
    --------
    >>> from hrv.detrend import sg_detrend
    >>> from hrv.sampledata import load_rest_rri
    >>> rri = load_rest_rri()
    >>> sg_detrend(rri)
    RRi array([5.07722695e+01, 4.16090643e+01, ..., -1.26297542e+01])
    """
    if isinstance(rri, RRi):
        time = rri.time
        rri = rri.values
    else:
        time = _create_time_array(rri)

    trend = savgol_filter(
        rri, window_length=window_length, polyorder=polyorder, *args, **kwargs
    )
    return RRiDetrended(rri - trend, time=time, detrended=True)

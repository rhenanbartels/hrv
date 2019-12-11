import numpy as np
from scipy.interpolate import CubicSpline

from hrv.rri import RRi
from hrv.utils import _create_time_info


__all__ = ['quotient', 'moving_average', 'moving_median', 'threshold_filter']


def quotient(rri):
    """
    Remove ectopic beats which the variation of two consecutive values
    exceeds 20%

    Parameters
    ----------
    rri : array_like
        sequence containing the RRi series

    Returns
    -------
    results : RRi array
        instance of the RRi class containing the filtered RRi values

    References
    ----------
    - Piskorski J, Guzik P. Filtering poincare plots.
      Comput Methods Sci Technol. 2005;11(1):39–48.

    Examples
    --------
    >>> from hrv.filters import quotient
    >>> from hrv.io import read_from_text
    >>> rri = read_from_text('/path/to/file.txt')
    >>> quotient(rri)
    RRi array([1114., 1113., 1066., 1119., 1062.,])
    """
    # TODO: Receive option to replaced outliers with stats
    # functions (i.e mean, median etc)
    # TODO: Receive option to re-create time array with cumsum of filtered rri
    # TODO: Receive threshold value

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
    """
    Low-pass filter. Replace each RRi value by the average of its ⌊N/2⌋
    neighbors. The first and the last ⌊N/2⌋ RRi values are not filtered

    Parameters
    ----------
    rri : array_like
        sequence containing the RRi series
    order : int, optional
        Strength of the filter. Number of adjacent RRi values used to calculate
        the average value to replace the current RRi. Defaults to 3.

    .. math::
        considering movinge average of order equal to 3:
            RRi[j] = sum(RRi[j-2] + RRi[j-1] + RRi[j+1] + RRi[j+2]) / 3

    Returns
    -------
    results : RRi array
        instance of the RRi class containing the filtered RRi values

    See Also
    -------
    moving_median, threshold_filter, quotient

    Examples
    --------
    >>> from hrv.filters import moving_average
    >>> from hrv.io import read_from_text
    >>> rri = read_from_text('/path/to/file.txt')
    >>> moving_average(rri)
    RRi array([1114.        , 1097.66666667, 1099.33333333, 1082.33333333,])
    """
    return _moving_function(rri, order, np.mean)


def moving_median(rri, order=3):
    """
    Low-pass filter. Replace each RRi value by the median of its ⌊N/2⌋
    neighbors. The first and the last ⌊N/2⌋ RRi values are not filtered

    Parameters
    ----------
    rri : array_like
        sequence containing the RRi series
    order : int, optional
        Strength of the filter. Number of adjacent RRi values used to calculate
        the median value to replace the current RRi. Defaults to 3.

    .. math::
        considering movinge average of order equal to 3:
            RRi[j] = np.median([RRi[j-2], RRi[j-1], RRi[j+1], RRi[j+2]])

    Returns
    -------
    results : RRi array
        instance of the RRi class containing the filtered RRi values

    See Also
    -------
    moving_average, threshold_filter, quotient

    Examples
    --------
    >>> from hrv.filters import moving_median
    >>> from hrv.io import read_from_text
    >>> rri = read_from_text('/path/to/file.txt')
    >>> moving_median(rri)
    RRi array([1114., 1113., 1113., 1066., ])
    """
    return _moving_function(rri, order, np.median)


def threshold_filter(rri, threshold='medium', local_median_size=5):
    """
    Low-pass filter. Inspired by the threshold-based artifact correction
    algorithm offered by Kubios®. To elect outliers in the tachogram series,
    each RRi is compared to the median value of local RRi (default N=5).
    All the RRi which the difference is greater than the local median value
    plus a threshold is replaced by cubic spline interpolated RRi.

    Parameters
    ----------
    rri : array_like
        sequence containing the RRi series
    threshold : str or int, optional
        Strength of the filter. If str will be translated to a threshold
        in miliseconds according to the dict below. If int, it is considered
        the threshold in miliseconds. Defaults to 'medium' (250ms)
        - Very Low: 450ms
        - Low: 350ms
        - Medium: 250ms
        - Strong: 150ms
        - Very Strong: 50ms
    local_median_size : int, optional
        Number of RRi values considered to caculate a local median to be
        compared with each RRi value

    .. math::
        considering the threshold equal to 'medium' and local_median_size
        equal to 5:
            local median RRi = np.median([RRi[j-5], RRi[j-4], RRi[j-3],
                                          RRi[j-2], RRi[j-1]])
            - Ectopic beat, if abs(RRi[j] - local median RRi) > 250
            - Normal beat, if abs(RRi[j] - local median RRi) <= 250

    Returns
    -------
    results : RRi array
        instance of the RRi class containing the filtered and cubic
        interpolated RRi values

    See Also
    -------
    moving_average, threshold_filter, quotient

    Examples
    --------
    >>> from hrv.filters import threshold_filter
    >>> from hrv.io import read_from_text
    >>> rri = read_from_text('/path/to/file.txt')
    >>> threshold_filter(rri)
    RRi array([1114., 1113., 1066., 1119., 1062.])
    """
    # TODO: DRY
    if isinstance(rri, RRi):
        rri_time = rri.time
        rri = rri.values
    else:
        rri_time = _create_time_info(rri)

    # Filter strength inspired in Kubios threshold based artifact correction
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

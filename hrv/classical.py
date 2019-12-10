# coding: utf-8
import numpy as np

from scipy.signal import welch
from spectrum import pburg

from hrv.detrend import polynomial_detrend
from hrv.rri import RRi
from hrv.utils import (validate_rri, _interpolate_rri)


__all__ = ['time_domain', 'frequency_domain', 'non_linear']


@validate_rri
def time_domain(rri):
    """
    time_domain(rri)

    Calculate time-domain indices from an RRi series

    Parameters
    ----------
    rri : array_like
        sequence containing the RRi series

    Returns
    -------
    results : dict
        Dictionary containing the following time domain indices:
            - rmssd: root mean squared of the successive differences
            - sdnn: standard deviation of the RRi series
            - sdsd: standard deviation of the successive differences
            - nn50: number RRi successive differences greater than 50ms
            - pnn50: percentage of RRi successive differences greater than 50ms
            - mri: average value of the RRi series
            - mhr: average value of the heart rate calculated from the
                   RRi sries

    References
    ----------
    - Heart rate variability. (1996). Standards of measurement, physiological
      interpretation, and clinical use. Task Force of the European Society of
      Cardiology and the North American Society of Pacing and
      Electrophysiology. Eur Heart J, 17, 354-381.

    Examples
    --------
    >>> from hrv.classical import time_domain
    >>> rri = [1, 2, 3, 4, 5, 6]
    >>> time_domain(rri)
    {'rmssd': 1.0,
     'sdnn': 1.8708286933869707,
     'sdsd': 0.0,
     'nn50': 0,
     'pnn50': 0.0,
     'mrri': 3.5,
     'mhr': 24500.0}
    """
    # TODO: let user choose interval for pnn50 and nn50.
    diff_rri = np.diff(rri)
    rmssd = np.sqrt(np.mean(diff_rri ** 2))
    sdnn = np.std(rri, ddof=1)  # make it calculates N-1
    sdsd = np.std(diff_rri, ddof=1)
    nn50 = _nn50(rri)
    pnn50 = _pnn50(rri)
    mrri = np.mean(rri)
    mhr = np.mean(60 / (rri / 1000.0))

    return dict(zip(['rmssd', 'sdnn', 'sdsd', 'nn50', 'pnn50', 'mrri', 'mhr'],
                    [rmssd, sdnn, sdsd, nn50, pnn50, mrri, mhr]))


def _nn50(rri):
    return sum(abs(np.diff(rri)) > 50)


def _pnn50(rri):
    return _nn50(rri) / len(rri) * 100


# TODO: create nperseg, noverlap and detrend arguments
def frequency_domain(rri, time=None, fs=4.0, method='welch',
                     interp_method='cubic', detrend='constant',
                     vlf_band=(0, 0.04), lf_band=(0.04, 0.15),
                     hf_band=(0.15, 0.4), **kwargs):
    """
    Estimate the Power Spectral Density (PSD) of an RRi series and
    calculate the area under the curve (AUC) of the Very Low, Low, and High
    frequency bands. The PSD can be estimated using non-parametric
    (Welch's method) or parametric (Burg's method) approaches. The AUC
    is calculated using the trapezoidal method (numpy.trapz).

    Parameters
    ----------
    rri : array_like
        Sequence containing the RRi series
    time : array_like, optional
        Sequence containing the time associated with the RRi series.
        When not provided time is created from the cumulative sum of the
        values from the RRi series
    method : str, optional
        The method for Power Spectral Density estimation. 'welch' (default),
        'ar' (spectrum, see Cokelaer et al., 2017)
    interp_method : str {'cubic', 'linear'}, optional
        Interpolation funtion applied to the RRi series. If RRi series
        is already interpolated this step is skipped. 'cubic' (default),
        'linear'
    detrend : str or function, optional
       Detrend method applied to the RRi series. Defaults to 'constant'.
       If the rri is an RRiDetrend object this step is skipped.
       See scipy.signal.welch for more information
    vlf_band : tuple (inferior_bound, superior_bound)
        Frenquency interval of the Very Low frequency components of the
        estimated PSD. Defaults to (0, 0.04)
    lf_band : tuple (inferior_bound, superior_bound)
        Frenquency interval of the Low frequency components of the estimated
        PSD. Defaults to (0.04, 0.15)
    hf_band : tuple (inferior_bound, superior_bound)
        Frenquency interval of the High frequency components of the estimated
        PSD. Defaults to (0.15, 0.4)

    Returns
    -------
    results : dict
        Dictionary containing the following frequency domain indices:
            - total power: root mean squared of the successive differences
            - vlf: standard deviation of the RRi series
            - lf: standard deviation of the successive differences
            - hf: number RRi successive differences greater than 50ms
            - lf/hf: percentage of RRi successive differences greater than 50ms
            - lfnu: average value of the RRi series
            - hfnu: average value of the heart rate calculated from the
                    RRi sries

    References
    ----------
    - Heart rate variability. (1996). Standards of measurement, physiological
      interpretation, and clinical use. Task Force of the European Society of
      Cardiology and the North American Society of Pacing and
      Electrophysiology. Eur Heart J, 17, 354-381.
    - Cokelaer et al., (2017). ‘Spectrum’: Spectral Analysis in Python.
      Journal of Open Source Software, 2(18), 348, doi:10.21105/joss.00348

    Examples
    --------
    >>> from hrv.io import read_from_text
    >>> from hrv.classical import frequency_domain
    >>> rri = read_from_text('path/to/file.txt')
    >>> frequency_domain(rri)
    {'total_power': 3376.2107048316066,
     'vlf': 447.31367706350915,
     'lf': 1217.5000069660707,
     'hf': 1711.3970208020266,
     'lf_hf': 0.71140710902693,
     'lfnu': 41.56854936937952,
     'hfnu': 58.43145063062048}
    """

    if isinstance(rri, RRi):
        time = rri.time if time is None else time
        detrend = detrend if not rri.detrended else False
        interp_method = interp_method if not rri.interpolated else None

    if interp_method is not None:
        rri = _interpolate_rri(rri, time, fs, interp_method)

    if method == 'welch':
        fxx, pxx = welch(x=rri, fs=fs, detrend=detrend, **kwargs)
    elif method == 'ar':
        if detrend:
            rri = polynomial_detrend(rri, degree=1)
        fxx, pxx = _calc_pburg_psd(rri=rri,  fs=fs, **kwargs)

    return _auc(fxx, pxx, vlf_band, lf_band, hf_band)


def _auc(fxx, pxx, vlf_band, lf_band, hf_band):
    vlf_indexes = np.logical_and(fxx >= vlf_band[0], fxx < vlf_band[1])
    lf_indexes = np.logical_and(fxx >= lf_band[0], fxx < lf_band[1])
    hf_indexes = np.logical_and(fxx >= hf_band[0], fxx < hf_band[1])

    vlf = np.trapz(y=pxx[vlf_indexes], x=fxx[vlf_indexes])
    lf = np.trapz(y=pxx[lf_indexes], x=fxx[lf_indexes])
    hf = np.trapz(y=pxx[hf_indexes], x=fxx[hf_indexes])
    total_power = vlf + lf + hf
    lf_hf = lf / hf
    lfnu = (lf / (total_power - vlf)) * 100
    hfnu = (hf / (total_power - vlf)) * 100

    return dict(zip(['total_power', 'vlf', 'lf', 'hf', 'lf_hf', 'lfnu',
                    'hfnu'], [total_power, vlf, lf, hf, lf_hf, lfnu, hfnu]))


def _calc_pburg_psd(rri, fs, order=16, nfft=None):
    burg = pburg(data=rri, order=order, NFFT=nfft, sampling=fs)
    burg.scale_by_freq = False
    burg()
    return np.array(burg.frequencies()), burg.psd


@validate_rri
def non_linear(rri):
    sd1, sd2 = _poincare(rri)
    return dict(zip(['sd1', 'sd2'], [sd1, sd2]))


def _poincare(rri):
    diff_rri = np.diff(rri)
    sd1 = np.sqrt(np.std(diff_rri, ddof=1) ** 2 * 0.5)
    sd2 = np.sqrt(2 * np.std(rri, ddof=1) ** 2 - 0.5 * np.std(diff_rri,
                                                              ddof=1) ** 2)
    return sd1, sd2

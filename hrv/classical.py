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

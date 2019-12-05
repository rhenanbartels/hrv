# coding: utf-8
import numpy as np

from scipy.signal import welch
from spectrum import pburg

from hrv.rri import RRi
from hrv.utils import (validate_rri, _interpolate_rri)


@validate_rri
def time_domain(rri):
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
                     interp_method='cubic', vlf_band=(0, 0.04),
                     lf_band=(0.04, 0.15), hf_band=(0.15, 0.4), **kwargs):

    if isinstance(rri, RRi) and time is None:
        time = rri.time

    if interp_method is not None:
        rri = _interpolate_rri(rri, time, fs, interp_method)

    if method == 'welch':
        fxx, pxx = welch(x=rri, fs=fs, **kwargs)
    elif method == 'ar':
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

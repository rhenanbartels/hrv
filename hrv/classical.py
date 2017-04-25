# coding: utf-8
import numpy as np
from scipy.signal import welch

from hrv.utils import (validate_rri, _interpolate_rri,
                       validate_frequency_domain_arguments)


@validate_rri
def time_domain(rri):
    diff_rri = np.diff(rri)
    rmssd = np.sqrt(np.mean(diff_rri ** 2))
    sdnn = np.std(rri, ddof=1)  # make it calculates N-1
    nn50 = sum(abs(diff_rri) > 50)
    pnn50 = (nn50 / len(diff_rri)) * 100
    mrri = np.mean(rri)
    mhr = np.mean(60 / (rri / 1000.0))

    return dict(zip(['rmssd', 'sdnn', 'nn50', 'pnn50', 'mrri', 'mhr'],
                    [rmssd, sdnn, nn50, pnn50, mrri, mhr]))


@validate_frequency_domain_arguments
@validate_rri
def frequency_domain(rri, fs, method, interp_method, vlf_band=(0, 0.04),
                     lf_band=(0.04, 0.15), hf_band=(0.15, 0.4), **kwargs):
    if interp_method is not None:
        time_interp, rri = _interpolate_rri(rri, fs, interp_method)
    if method == 'welch':
        fxx, pxx = welch(x=rri, fs=fs, **kwargs)

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

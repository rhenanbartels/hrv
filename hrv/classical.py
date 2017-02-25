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
                    np.round([rmssd, sdnn, nn50, pnn50, mrri, mhr], 2)))


@validate_frequency_domain_arguments
def frequency_domain(rri, method, interp_freq, segment_size, overlap_size):

    time_interp, rri_interp = _interpolate_rri(rri, interp_freq)
    fxx, pxx = welch(x=rri_interp, fs=interp_freq)

    return _bands_energy(fxx, pxx)


def _bands_energy(fxx, pxx, vlf_band=(0, 0.04), lf_band=(0.04, 0.15),
                  hf_band=(0.15, 0.4)):
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
                    'hfnu'], np.round(
                          [total_power, vlf, lf, hf, lf_hf, lfnu, hfnu], 2)))

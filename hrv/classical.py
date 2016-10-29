# coding: utf-8
import numpy as np
from scipy.signal import welch

from hrv.utils import (validate_rri, _interpolate_rri,
                       validate_frequency_domain_arguments)


@validate_rri
def time_domain(rri):
    diff_rri = np.diff(rri)
    rmssd = np.sqrt(np.mean(diff_rri ** 2))
    sdnn = np.std(diff_rri, ddof=1)  # make it calculates N-1
    nn50 = sum(abs(diff_rri) > 50)
    pnn50 = (nn50 / len(diff_rri)) * 100
    mrri = np.mean(rri)
    mhr = np.mean(60 / (rri / 1000.0))

    return dict(rmssd=rmssd, sdnn=sdnn, nn50=nn50, pnn50=pnn50,
                mrri=mrri, mhr=mhr)


def frequency_domain(rri, interp_freq=4,
                     method='welch', segment_size=256,
                     overlap_size=128,
                     window_function='hanning'):

    return dict(total_power=0.0, vlf=0.0, lf=0.0, hf=0.0, lf_hf=0.0,
                lfnu=0.0, hfnu=0.0)

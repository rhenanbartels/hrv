# coding: utf-8
import numpy as np

from hrv.utils import validate_rri

def time_domain(rri):
    rri = validate_rri(rri)
    diff_rri = np.diff(rri)
    rmssd = np.sqrt(np.mean(diff_rri ** 2))
    sdnn = np.std(diff_rri, ddof=1) # make it calculates N-1
    nn50 = sum(abs(diff_rri) > 50)
    pnn50 = nn50 / float(len(diff_rri))
    mrri = np.mean(rri)
    mhr = np.mean(60 / (rri / 1000.0))
    return dict(rmssd=rmssd, sdnn=sdnn, nn50=nn50, pnn50=pnn50, mrri=mrri, 
                mhr=mhr)

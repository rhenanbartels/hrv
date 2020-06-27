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
            - RMSSD: root mean squared of the successive differences
            - SDNN: standard deviation of the RRi series
            - SDSD: standard deviation of the successive differences
            - NN50: number RRi successive differences greater than 50ms
            - PNN50: percentage of RRi successive differences greater than 50ms
            - MRI: average value of the RRi series
            - MHR: average value of the heart rate calculated from the
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
    >>> from hrv.sampledata import load_rest_rri
    >>> rri = load_rest_rri()
    >>> time_domain(rri)
    {'rmssd': 55.13744203126742,
     'sdnn': 57.81817771970009,
     'sdsd': 55.167700730663555,
     'nn50': 321,
     'pnn50': 35.27472527472528,
     'mrri': 1058.7186813186813,
     'mhr': 56.85278105637358}
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

    return dict(
        zip(
            ["rmssd", "sdnn", "sdsd", "nn50", "pnn50", "mrri", "mhr"],
            [rmssd, sdnn, sdsd, nn50, pnn50, mrri, mhr],
        )
    )


def _nn50(rri):
    return sum(abs(np.diff(rri)) > 50)


def _pnn50(rri):
    return _nn50(rri) / len(rri) * 100


# TODO: create nperseg, noverlap, order, nfft, and detrend arguments
def frequency_domain(
    rri,
    time=None,
    fs=4.0,
    method="welch",
    interp_method="cubic",
    detrend="constant",
    vlf_band=(0, 0.04),
    lf_band=(0.04, 0.15),
    hf_band=(0.15, 0.4),
    **kwargs
):
    """
    Estimate the Power Spectral Density (PSD) of an RRi series and
    calculate the area under the curve (AUC) of the Very Low, Low, and High
    frequency bands. The PSD can be estimated using non-parametric
    (FFT - Welch's method) or parametric (Autoregressive - Burg's method)
    approaches. The AUC is calculated using the trapezoidal method
    (numpy.trapz).

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
    nperseg : int, optional
        The size of each segment used in the FFT-based estimation of the PSD.
        Defaults to 256. ``nperseg <= len(rri)``. See scipy.signal.welch
        for more information
    noverlap : int, optional
        The size of overlap between each adjacent rri segments. If `None`
        ``noverlap = nperseg // 2``. See scipy.signal.welch for more
        information
    detrend : str or function, optional
        Detrend method applied to the RRi series. Defaults to 'constant'.
        If the rri is an RRiDetrend object this step is skipped.
        See scipy.signal.welch for more information
    window : str or tuple or array_like, optional
        Window function applied to each segment of the RRi series to avoid
        spectral leakage. Only applied when welch method is chosen.
        Defaults to Hanning. See scipy.signal.welch for more information
    order : int, optional
        Order of the Autoregressive model. Only applied when method is 'ar'.
        Defaults to 16
    vlf_band : tuple (inferior_bound, superior_bound), optional
        Frenquency interval of the Very Low frequency components of the
        estimated PSD. Defaults to (0, 0.04)
    lf_band : tuple (inferior_bound, superior_bound), optional
        Frenquency interval of the Low frequency components of the estimated
        PSD. Defaults to (0.04, 0.15)
    hf_band : tuple (inferior_bound, superior_bound), optional
        Frenquency interval of the High frequency components of the estimated
        PSD. Defaults to (0.15, 0.4)

    Returns
    -------
    results : dict
        Dictionary containing the following frequency domain indices:
            - Total Power: total energy of the PSD
            - VLF: energy associated with the Very Low frequency components
            - LF: energy associated with the Low frequency components
            - HF: energy associated with the High frequency components
            - LF/HF: ratio between lf and hf indices
            - LFnu: LF indice normalized by the Total Power. See math below
            - HFnu: HF indice normalized by the Total Power. See math below
                    RRi sries

    .. math::

        LFnu = LF / (Total Power - VLF)
        HFnu = HF / (Total Power - VLF)

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
    >>> from hrv.classical import frequency_domain
    >>> from hrv.sampledata import load_rest_rri
    >>> rri = load_rest_rri()
    >>> frequency_domain(rri)
    {'total_power': 2212.2894012201778,
     'vlf': 546.8173917540497,
     'lf': 770.4465329950162,
     'hf': 895.0254764711116,
     'lf_hf': 0.8608096118478296,
     'lfnu': 46.25995084972849,
     'hfnu': 53.740049150271496}
    """

    if isinstance(rri, RRi):
        time = rri.time if time is None else time
        detrend = detrend if not rri.detrended else False
        interp_method = interp_method if not rri.interpolated else None

    if interp_method is not None:
        rri = _interpolate_rri(rri, time, fs, interp_method)

    if method == "welch":
        fxx, pxx = welch(x=rri, fs=fs, detrend=detrend, **kwargs)
    elif method == "ar":
        if detrend:
            rri = polynomial_detrend(rri, degree=1)
        fxx, pxx = _calc_pburg_psd(rri=rri, fs=fs, **kwargs)

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

    return dict(
        zip(
            ["total_power", "vlf", "lf", "hf", "lf_hf", "lfnu", "hfnu"],
            [total_power, vlf, lf, hf, lf_hf, lfnu, hfnu],
        )
    )


def _calc_pburg_psd(rri, fs, order=16, nfft=None):
    burg = pburg(data=rri, order=order, NFFT=nfft, sampling=fs)
    burg.scale_by_freq = False
    burg()
    return np.array(burg.frequencies()), burg.psd


@validate_rri
def non_linear(rri):
    """
    Calculate non-linear indices from RRi series. So far, only SD1 and SD2
    features derived from the Poincaré analysis are available.

    Parameters
    ----------
    rri : array_like
        Sequence containing the RRi series

    Returns
    -------
    results : dict
        Dictionary containing the following non-linear indices:
            - SD1: standard deviation of the points in the Poincaré's plot
              projected in the y = x axis.
            - SD2: standard deviation of the points in the Poincaré's plot
              projected in the y = -x + mrri axis, where mrri is the average
              value of the RRi series.

    .. math::

        SD1 = np.sqrt(0.5 * np.std(np.diff(rri, ddof=1))**2)
        SD2 = np.sqrt(2 * np.std(rri, ddof=1) ** 2 - 0.5
              * np.std(np.diff(rri, ddof=1))**2)

    References
    ----------
    - Heart rate variability. (1996). Standards of measurement, physiological
      interpretation, and clinical use. Task Force of the European Society of
      Cardiology and the North American Society of Pacing and
      Electrophysiology. Eur Heart J, 17, 354-381.

    Examples
    --------
    >>> from hrv.classical import non_linear
    >>> from hrv.sampledata import load_rest_rri
    >>> rri = load_rest_rri()
    >>> non_linear(rri)
    {'sd1': 39.00945528912225, 'sd2': 71.86199098062633}
    """
    sd1, sd2 = _poincare(rri)
    return dict(zip(["sd1", "sd2"], [sd1, sd2]))


def _poincare(rri):
    diff_rri = np.diff(rri)
    sd1 = np.sqrt(np.std(diff_rri, ddof=1) ** 2 * 0.5)
    sd2 = np.sqrt(2 * np.std(rri, ddof=1) ** 2 - 0.5 * np.std(diff_rri, ddof=1) ** 2)
    return sd1, sd2

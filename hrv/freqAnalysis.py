import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from scipy import interpolate
from scipy import signal


class freq_domain:
    def __init__(self, rri, fs=4, method='welch',
                 interp_method='cubic', detrend='linear'):
        self.rri = rri
        self.fs = fs
        self.method = method
        self.interp_method = interp_method
        self.detrend = detrend
        self.vlf_band = (0, 0.04)
        self.lf_band = (0.04, 0.15)
        self.hf_band = (0.15, 0.4)
        self.freq = []
        self.psd = []
        self.calculateFeqAndPsd()

    def calculateFeqAndPsd(self):
        self.freq, self.psd = _get_freq_psd_from_nn_intervals(rri=self.rri, method=self.method,
                                                              fs=self.fs,
                                                              interp_method=self.interp_method)

    def getGraphDataPoints(self):
        return {'freq': self.freq, 'psd': self.psd}

    def getFeatures(self):
        """
        Computes frequency domain features from the power spectral decomposition.

        Parameters
        ---------
        freq : array
            Array of sample frequencies.
        psd : list
            Power spectral density or power spectrum.
        vlf_band : tuple
            Very low frequency bands for features extraction from power spectral density.
        lf_band : tuple
            Low frequency bands for features extraction from power spectral density.
        hf_band : tuple
            High frequency bands for features extraction from power spectral density.

        Returns
        ---------
        freqency_domain_features : dict
            Dictionary containing frequency domain features for HRV analyses. There are details
            about each features given below.
        """

        # Calcul of indices between desired frequency bands
        vlf_indexes = np.logical_and(
            self.freq >= self.vlf_band[0], self.freq < self.vlf_band[1])
        lf_indexes = np.logical_and(
            self.freq >= self.lf_band[0], self.freq < self.lf_band[1])
        hf_indexes = np.logical_and(
            self.freq >= self.hf_band[0], self.freq < self.hf_band[1])

        # Integrate using the composite trapezoidal rule
        lf = np.trapz(y=self.psd[lf_indexes], x=self.freq[lf_indexes])
        hf = np.trapz(y=self.psd[hf_indexes], x=self.freq[hf_indexes])

        # total power & vlf : Feature often used for  "long term recordings" analysis
        vlf = np.trapz(y=self.psd[vlf_indexes], x=self.freq[vlf_indexes])
        total_power = vlf + lf + hf

        lf_hf_ratio = lf / hf
        lfnu = (lf / (lf + hf)) * 100
        hfnu = (hf / (lf + hf)) * 100

        freqency_domain_features = {
            'lf': lf,
            'hf': hf,
            'lf_hf_ratio': lf_hf_ratio,
            'lfnu': lfnu,
            'hfnu': hfnu,
            'total_power': total_power,
            'vlf': vlf
        }

        return freqency_domain_features

    def plot(self):
        # Calcul of indices between desired frequency bands
        vlf_indexes = np.logical_and(
            self.freq >= self.vlf_band[0], self.freq < self.vlf_band[1])
        lf_indexes = np.logical_and(
            self.freq >= self.lf_band[0], self.freq < self.lf_band[1])
        hf_indexes = np.logical_and(
            self.freq >= self.hf_band[0], self.freq < self.hf_band[1])
        frequency_band_index = [vlf_indexes, lf_indexes, hf_indexes]
        label_list = ["VLF component", "LF component", "HF component"]

        # Plot parameters
        style.use("seaborn-darkgrid")
        plt.figure(figsize=(12, 8))
        plt.xlabel("Frequency (Hz)", fontsize=15)
        plt.ylabel("PSD (s2/ Hz)", fontsize=15)
        if self.method == "welch":
            plt.title("FFT Spectrum : Welch's periodogram", fontsize=20)
            for band_index, label in zip(frequency_band_index, label_list):
                plt.fill_between(
                    self.freq[band_index], 0, self.psd[band_index] / (1000 * len(self.psd[band_index])), label=label)
            plt.legend(prop={"size": 15}, loc="best")
            plt.xlim(0, self.hf_band[1])
        else:
            raise ValueError(
                "Not a valid method. Choose 'welch'")
        plt.show()


def _create_timestamp_list(nn_intervals):
    """
    Creates corresponding time interval for all nn_intervals

    Parameters
    ---------
    nn_intervals : list
        List of Normal to Normal Interval.

    Returns
    ---------
    nni_tmstp : list
        list of time intervals between first NN-interval and final NN-interval.
    """
    # Convert in seconds
    nni_tmstp = np.cumsum(nn_intervals) / 1000

    # Force to start at 0
    return nni_tmstp - nni_tmstp[0]


def _create_interpolated_timestamp_list(nn_intervals, sampling_frequency: int = 7):
    """
    Creates the interpolation time used for Fourier transform's method

    Parameters
    ---------
    nn_intervals : list
        List of Normal to Normal Interval.
    sampling_frequency : int
        Frequency at which the signal is sampled.

    Returns
    ---------
    nni_interpolation_tmstp : list
        Timestamp for interpolation.
    """
    time_nni = _create_timestamp_list(nn_intervals)
    # Create timestamp for interpolation
    nni_interpolation_tmstp = np.arange(
        0, time_nni[-1], 1 / float(sampling_frequency))
    return nni_interpolation_tmstp


def _get_freq_psd_from_nn_intervals(rri, method: str = 'welch',
                                    fs: int = 4,
                                    interp_method: str = "linear"):
    """
    Returns the frequency and power of the signal.

    Parameters
    ---------
    rri : list
        list of Normal to Normal Interval
    method : str
        Method used to calculate the psd. Choice are Welch's FFT or Lomb method.
    sampling_frequency : int
        Frequency at which the signal is sampled. Common value range from 1 Hz to 10 Hz,
        by default set to 7 Hz. No need to specify if Lomb method is used.
    interpolation_method : str
        Kind of interpolation as a string, by default "linear". No need to specify if Lomb
        method is used.
    vlf_band : tuple
        Very low frequency bands for features extraction from power spectral density.
    hf_band : tuple
        High frequency bands for features extraction from power spectral density.

    Returns
    ---------
    freq : list
        Frequency of the corresponding psd points.
    psd : list
        Power Spectral Density of the signal.
    """

    timestamp_list = _create_timestamp_list(rri)

    if method == "welch":
        # ---------- Interpolation of signal ---------- #
        funct = interpolate.interp1d(
            x=timestamp_list, y=rri, kind=interp_method)

        timestamps_interpolation = _create_interpolated_timestamp_list(
            rri, fs)
        nni_interpolation = funct(timestamps_interpolation)

        # ---------- Remove DC Component ---------- #
        nni_normalized = nni_interpolation - np.mean(nni_interpolation)

        #  --------- Compute Power Spectral Density  --------- #
        freq, psd = signal.welch(x=nni_normalized, fs=fs, window='hann',
                                 nfft=4096)
    else:
        raise ValueError(
            "Not a valid method. Choose 'welch'")

    return freq, psd

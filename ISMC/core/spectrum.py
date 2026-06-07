# core/spectrum.py
# ------------------------------------------------------------
# Spectrum-related functions
# Covers:
# - FFT
# - PSD
# - bandwidth values
# - Parseval verification
# ------------------------------------------------------------

import numpy as np


def compute_fft_psd(waveform, fs):
    """
    Compute FFT and PSD of the transmitted waveform.

    Returns:
        freq : shifted frequency axis
        X    : shifted FFT
        PSD  : power spectral density estimate
    """
    X = np.fft.fft(waveform)
    X = np.fft.fftshift(X)

    freq = np.fft.fftfreq(len(waveform), d=1 / fs)
    freq = np.fft.fftshift(freq)

    PSD = (np.abs(X) ** 2) / len(waveform)

    return freq, X, PSD


def compute_spectrum(waveform, fs):
    """
    Wrapper function so main.py can use one standard name.
    Returns:
        X_unshifted, X_shifted, freq_unshifted, freq_shifted, PSD
    """
    X_unshifted = np.fft.fft(waveform)
    freq_unshifted = np.fft.fftfreq(len(waveform), d=1 / fs)

    freq_shifted, X_shifted, PSD = compute_fft_psd(waveform, fs)

    return X_unshifted, X_shifted, freq_unshifted, freq_shifted, PSD


def compute_bandwidth_values(fc, Rb):
    """
    Compute lower null, upper null, and null-to-null bandwidth.
    """
    f_lower = fc - Rb
    f_upper = fc + Rb
    BW = 2 * Rb

    return f_lower, f_upper, BW


def compute_bandwidth(fc, Rb):
    """
    Wrapper function for main.py compatibility.
    """
    return compute_bandwidth_values(fc, Rb)


def verify_parseval(waveform, X, fs):
    """
    Verify Parseval's theorem.

    Time-domain energy:
        E_time = sum(x[n]^2) / fs

    Frequency-domain energy:
        E_freq = (1/fs) * (1/L) * sum(|X[k]|^2)

    Returns:
        E_time
        E_freq
        percent_error
    """
    E_time = np.sum(waveform ** 2) / fs
    L = len(waveform)
    E_freq = (1 / fs) * (1 / L) * np.sum(np.abs(X) ** 2)

    percent_error = abs((E_time - E_freq) / E_time) * 100

    return E_time, E_freq, percent_error


def print_co2_results(fc, Rb, f_lower, f_upper, BW, E_time, E_freq, percent_error):
    """
    Print main CO2 numerical outputs in a clean format.
    """
    print("\n" + "=" * 60)
    print("CO2 - FFT, PSD, BANDWIDTH, PARSEVAL")
    print("=" * 60)
    print(f"Carrier frequency fc         = {fc:.2f} Hz")
    print(f"Lower first null             = {f_lower:.2f} Hz")
    print(f"Upper first null             = {f_upper:.2f} Hz")
    print(f"Null-to-null bandwidth BW    = {BW:.2f} Hz")
    print(f"Time-domain energy           = {E_time:.8e} J")
    print(f"Frequency-domain energy      = {E_freq:.8e} J")
    print(f"Parseval percentage error    = {percent_error:.8e} %")
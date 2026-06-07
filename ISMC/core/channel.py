# core/channel.py
# ------------------------------------------------------------
# Channel and receiver functions
# Covers:
# - mild LPF + AWGN channel
# - correlator receiver
# - FIR matched filter receiver
# - equivalence comparison
# ------------------------------------------------------------

import numpy as np
from scipy.signal import lfilter


def apply_channel_and_noise(waveform, h, Eb, EbN0_dB, fs, Rb):
    """
    Pass waveform through mild low-pass filter and then add AWGN.

    Returns:
        tx_filtered
        noise
        rx
        sigma2
        sigma
    """
    tx_filtered = lfilter(h, 1, waveform)

    EbN0_lin = 10 ** (EbN0_dB / 10)
    N0 = Eb / EbN0_lin

    sigma2 = N0 * fs / (2 * Rb)
    sigma = np.sqrt(sigma2)

    noise = sigma * np.random.randn(len(tx_filtered))
    rx = tx_filtered + noise

    return tx_filtered, noise, rx, sigma2, sigma


def correlator_receiver(rx_signal, ref_signal, N):
    """
    Detect bits using correlator receiver.
    """
    detected_bits = []
    correlator_outputs = []

    for i in range(0, len(rx_signal), N):
        segment = rx_signal[i:i + N]

        if len(segment) == N:
            y = np.sum(segment * ref_signal)
            correlator_outputs.append(y)

            if y >= 0:
                detected_bits.append(1)
            else:
                detected_bits.append(0)

    return np.array(detected_bits), np.array(correlator_outputs)


def matched_filter_receiver(rx_signal, s1, fs):
    """
    Matched filter output and frequency response.
    Returns values in the format expected by main.py.
    """
    h_mf = s1[::-1]
    mf_output = lfilter(h_mf, 1, rx_signal)

    H_mf = np.fft.fftshift(np.fft.fft(h_mf, 4096))
    f_mf = np.fft.fftshift(np.fft.fftfreq(4096, d=1 / fs))

    return h_mf, mf_output, H_mf, f_mf


def count_bit_errors(tx_bits, rx_bits):
    """
    Count bit errors between transmitted and detected bits.
    """
    L = min(len(tx_bits), len(rx_bits))
    return np.sum(tx_bits[:L] != rx_bits[:L])


def compare_receivers(bits_corr, bits_mf):
    """
    Check whether correlator and matched filter decisions match.
    """
    L = min(len(bits_corr), len(bits_mf))
    return np.array_equal(bits_corr[:L], bits_mf[:L])


def print_co3_co4_results(EbN0_dB, tx_bits, corr_bits, mf_bits, err_corr, err_mf, same_flag):
    """
    Print channel and receiver outputs clearly.
    """
    print("\n" + "=" * 60)
    print("CO3 / CO4 - CHANNEL AND RECEIVER RESULTS")
    print("=" * 60)
    print(f"Selected Eb/N0 (dB)          = {EbN0_dB}")

    print("\nTransmitted bits             =", tx_bits)
    print("Detected bits (Correlator)   =", corr_bits)
    print("Detected bits (Matched Filt) =", mf_bits)

    print(f"\nBit errors - Correlator      = {err_corr}")
    print(f"Bit errors - Matched Filter  = {err_mf}")
    print(f"Receiver equivalence check   = {same_flag}")
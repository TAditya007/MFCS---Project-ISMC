# core/bpsk.py
# ------------------------------------------------------------
# BPSK signal generation functions
# Covers:
# - one-bit symbol creation
# - energy per bit calculation
# - 10-bit waveform generation
# ------------------------------------------------------------

import numpy as np


def generate_bpsk_symbols(fc, Rb, fs, A):
    """
    Generate one-bit BPSK symbols for bit 1 and bit 0.

    bit 1 -> +cos carrier
    bit 0 -> -cos carrier

    Returns:
        t_bit : time axis for one bit
        s1    : waveform for bit 1
        s0    : waveform for bit 0
        Tb    : bit duration
        N     : samples per bit
    """
    Tb = 1 / Rb
    N = int(fs / Rb)
    t_bit = np.arange(0, Tb, 1 / fs)

    s1 = A * np.cos(2 * np.pi * fc * t_bit)
    s0 = -A * np.cos(2 * np.pi * fc * t_bit)

    return t_bit, s1, s0, Tb, N


def compute_energy_per_bit(s1, fs, Tb, A):
    """
    Compute energy per bit in two ways:
    1. Numerical value using sampled signal
    2. Theoretical value using formula A^2 * Tb / 2

    Returns:
        Eb_num
        Eb_theory
        percent_error
    """
    Eb_num = np.sum(s1 ** 2) / fs
    Eb_theory = (A ** 2 * Tb) / 2
    percent_error = abs((Eb_num - Eb_theory) / Eb_theory) * 100

    return Eb_num, Eb_theory, percent_error


def generate_10bit_waveform(bits, s1, s0, fs):
    """
    Join one-bit BPSK symbols one after another
    to form the full transmitted waveform.
    """
    waveform = np.array([])

    for bit in bits:
        if bit == 1:
            waveform = np.concatenate((waveform, s1))
        else:
            waveform = np.concatenate((waveform, s0))

    t_wave = np.arange(0, len(waveform) / fs, 1 / fs)
    t_wave = t_wave[:len(waveform)]

    return t_wave, waveform


def check_antipodal(s1, s0):
    """
    Check whether s0 is exactly the negative of s1.
    In BPSK this should be true.
    """
    return np.allclose(s0, -s1)


def print_co1_results(Tb, N, Eb_num, Eb_theory, percent_error, antipodal_ok):
    """
    Print the main CO1 numerical outputs in a clean format.
    """
    print("\n" + "=" * 60)
    print("CO1 - BPSK SIGNAL GENERATION AND ENERGY")
    print("=" * 60)
    print(f"Bit duration Tb              = {Tb:.6e} s")
    print(f"Samples per bit N            = {N}")
    print(f"Antipodal check (s0 = -s1)   = {antipodal_ok}")
    print(f"Numerical energy per bit     = {Eb_num:.8e} J")
    print(f"Theoretical energy per bit   = {Eb_theory:.8e} J")
    print(f"Percentage error             = {percent_error:.6f} %")
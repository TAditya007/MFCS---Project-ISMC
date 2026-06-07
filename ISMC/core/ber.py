# core/ber.py
# ------------------------------------------------------------
# BER simulation functions for MFCS BPSK project
# Covers:
# - Monte Carlo BER simulation
# - theoretical BER calculation
# ------------------------------------------------------------

import numpy as np
from scipy.signal import lfilter
from scipy.special import erfc


def simulate_ber(n_bits, N, h, EbN0_dB_range):
    """
    Monte Carlo BER simulation using oversampled baseband BPSK.

    Why baseband model?
    - It is much faster than full carrier simulation.
    - It is acceptable for BER analysis.
    - It still lets us include mild LPF + AWGN effect.

    Steps:
    1) Generate random bits
    2) Map bits to BPSK symbols: 0 -> -1, 1 -> +1
    3) Repeat each symbol N times
    4) Pass through mild LPF channel
    5) Add AWGN
    6) Detect using correlator over each bit block

    Returns:
        BER_sim : simulated BER array
    """
    bits = np.random.randint(0, 2, n_bits)
    symbols = 2 * bits - 1

    # Oversampled baseband waveform
    tx_wave = np.repeat(symbols, N)

    BER_sim = []
    ref = np.ones(N)

    for EbN0_dB in EbN0_dB_range:
        EbN0_lin = 10 ** (EbN0_dB / 10)

        # Normalized energy-per-bit model
        # This keeps BER simulation simple and fast
        sigma2 = N / (2 * EbN0_lin)
        sigma = np.sqrt(sigma2)

        # Apply mild low-pass channel
        tx_filtered = lfilter(h, 1, tx_wave)

        # Add white Gaussian noise
        noise = sigma * np.random.randn(len(tx_filtered))
        rx = tx_filtered + noise

        # Bit detection using block correlation
        detected_bits = np.zeros(n_bits, dtype=int)

        for i in range(n_bits):
            segment = rx[i * N:(i + 1) * N]
            y = np.sum(segment * ref)
            detected_bits[i] = 1 if y >= 0 else 0

        errors = np.sum(bits != detected_bits)
        ber = errors / n_bits
        BER_sim.append(ber)

    return np.array(BER_sim)


def theoretical_ber(EbN0_dB_range):
    """
    Theoretical BER for BPSK over AWGN:
        Pe = 0.5 * erfc(sqrt(Eb/N0))
    """
    BER_theory = []

    for EbN0_dB in EbN0_dB_range:
        EbN0_lin = 10 ** (EbN0_dB / 10)
        ber = 0.5 * erfc(np.sqrt(EbN0_lin))
        BER_theory.append(ber)

    return np.array(BER_theory)


def print_ber_results(EbN0_dB_range, BER_sim, BER_theory):
    """
    Print BER table in a report-friendly format.
    """
    print("\n" + "=" * 60)
    print("CO5 - BER RESULTS")
    print("=" * 60)
    print("Eb/N0(dB)   Simulated BER      Theoretical BER")

    for i in range(len(EbN0_dB_range)):
        print(f"{EbN0_dB_range[i]:>3}        {BER_sim[i]:.6e}     {BER_theory[i]:.6e}")
# core/capacity.py
# ------------------------------------------------------------
# Shannon capacity and gap functions for MFCS BPSK project
# Covers:
# - Shannon capacity calculation
# - capacity at 10 dB
# - gap from Shannon limit
# ------------------------------------------------------------

import numpy as np


def shannon_capacity(Rb):
    """
    Compute Shannon capacity using:
        B = 2*Rb
        C = B * log2(1 + SNR)

    SNR range:
        0 dB to 20 dB in steps of 2 dB
    """
    B = 2 * Rb
    SNR_dB = np.arange(0, 21, 2)
    SNR_lin = 10 ** (SNR_dB / 10)
    C = B * np.log2(1 + SNR_lin)

    return B, SNR_dB, SNR_lin, C


def capacity_at_10dB(B):
    """
    Compute capacity at 10 dB.
    """
    SNR_dB_mark = 10
    SNR_lin_mark = 10 ** (SNR_dB_mark / 10)
    C_mark = B * np.log2(1 + SNR_lin_mark)

    return SNR_dB_mark, SNR_lin_mark, C_mark


def shannon_gap():
    """
    Compute gap between uncoded BPSK and Shannon limit.

    Given in project:
        Uncoded BPSK for BER = 1e-5 -> 9.6 dB
        Shannon limit               -> 1.59 dB
    """
    EbN0_req = 9.6
    EbN0_shannon = 1.59
    gap = EbN0_req - EbN0_shannon

    return EbN0_req, EbN0_shannon, gap


def print_capacity_results(B, SNR_dB_mark, C_mark, EbN0_req, EbN0_shannon, gap):
    """
    Print capacity and gap values clearly.
    """
    print("\n" + "=" * 60)
    print("CO6 - SHANNON CAPACITY AND GAP")
    print("=" * 60)
    print(f"Bandwidth B                  = {B:.2f} Hz")
    print(f"Capacity at {SNR_dB_mark} dB           = {C_mark:.2f} bps")
    print(f"Uncoded BPSK requirement     = {EbN0_req:.2f} dB")
    print(f"Shannon limit                = {EbN0_shannon:.2f} dB")
    print(f"Performance gap              = {gap:.2f} dB")
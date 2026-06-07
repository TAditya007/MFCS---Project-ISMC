# main.py
# ============================================================
# MFCS PROJECT - BATCH 9
# Case Study on Complete CommLink-BPSK System Development
# for Reliable Sensor Data Transmission Using Python
# Application Theme: Industrial Sensor Monitoring Communication
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter

# Import project modules
from config import *

from core.bpsk import *
from core.spectrum import *
from core.channel import *
from core.ber import *
from core.capacity import *

# For repeatable random outputs
np.random.seed(42)

# ============================================================
# PART A - SIGNAL REPRESENTATION AND BPSK WAVEFORM (CO1)
# ============================================================
print("\n" + "=" * 70)
print("PART A - SIGNAL REPRESENTATION AND BPSK WAVEFORM (CO1)")
print("=" * 70)

# Generate one-bit BPSK symbols directly from bpsk.py
t, s1, s0, Tb, N = generate_bpsk_symbols(fc, Rb, fs, A)

print(f"Application Theme = Industrial Sensor Monitoring Communication")
print(f"Carrier frequency fc = {fc} Hz")
print(f"Bit rate Rb = {Rb} bps")
print(f"Sampling frequency fs = {fs} Hz")
print(f"Amplitude A = {A} V")
print(f"Bit duration Tb = {Tb:.6e} s")
print(f"Samples per bit N = {N}")

# Plot one-bit symbols
plt.figure(figsize=(10, 4))
plt.plot(t * 1e3, s1, label='s1(t) for bit 1', linewidth=2)
plt.plot(t * 1e3, s0, label='s0(t) for bit 0', linewidth=2, linestyle='--')
plt.title('One-Bit BPSK Symbols')
plt.xlabel('Time (ms)')
plt.ylabel('Amplitude (V)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Antipodal check
antipodal_ok = check_antipodal(s1, s0)
print(f"Antipodal check (s0 = -s1): {antipodal_ok}")

# Energy per bit
Eb_num, Eb_theory, Eb_error = compute_energy_per_bit(s1, fs, Tb, A)

print(f"Numerical Eb     = {Eb_num:.8e} J")
print(f"Theoretical Eb   = {Eb_theory:.8e} J")
print(f"Percentage error = {Eb_error:.6f} %")

# Generate 10-bit waveform
time_axis, waveform = generate_10bit_waveform(bits_plot, s1, s0, fs)

plt.figure(figsize=(12, 4))
plt.plot(time_axis * 1e3, waveform, color='b', linewidth=1.5)
for k in range(len(bits_plot) + 1):
    plt.axvline(k * Tb * 1e3, color='r', linestyle='--', alpha=0.5)

plt.title('10-Bit BPSK Waveform')
plt.xlabel('Time (ms)')
plt.ylabel('Amplitude (V)')
plt.grid(True)
plt.tight_layout()
plt.show()

print("Observation:")
print("- BPSK uses the same carrier for both bits.")
print("- Bit 0 is represented by a 180 degree phase reversal.")
print("- So the waveform changes sign when the transmitted bit is 0.")


# ============================================================
# PART B - FFT, PSD, AND PARSEVAL (CO2)
# ============================================================
print("\n" + "=" * 70)
print("PART B - FFT, PSD, AND PARSEVAL (CO2)")
print("=" * 70)

# FFT and PSD
X, X_shift, freq, freq_shift, PSD = compute_spectrum(waveform, fs)

f_lower_null = fc - Rb
f_upper_null = fc + Rb
BW = 2 * Rb

print(f"Lower first null = {f_lower_null:.2f} Hz")
print(f"Upper first null = {f_upper_null:.2f} Hz")
print(f"Null-to-null bandwidth = {BW:.2f} Hz")

plt.figure(figsize=(12, 4))
plt.plot(freq_shift / 1e3, np.abs(X_shift), linewidth=1.2)
plt.axvline(fc / 1e3, color='r', linestyle='--', label='Carrier fc')
plt.axvline(f_lower_null / 1e3, color='g', linestyle='--', label='First nulls')
plt.axvline(f_upper_null / 1e3, color='g', linestyle='--')
plt.title('Magnitude Spectrum of BPSK Signal')
plt.xlabel('Frequency (kHz)')
plt.ylabel('|X(f)|')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 4))
plt.plot(freq_shift / 1e3, PSD, linewidth=1.2)
plt.axvline(fc / 1e3, color='r', linestyle='--', label='Carrier fc')
plt.axvline(f_lower_null / 1e3, color='g', linestyle='--', label='First nulls')
plt.axvline(f_upper_null / 1e3, color='g', linestyle='--')
plt.title('Power Spectral Density of BPSK Signal')
plt.xlabel('Frequency (kHz)')
plt.ylabel('PSD')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Parseval verification
E_time, E_freq, parseval_error = verify_parseval(waveform, X, fs)

print(f"Time-domain energy = {E_time:.8e} J")
print(f"Freq-domain energy = {E_freq:.8e} J")
print(f"Parseval error     = {parseval_error:.8e} %")

if parseval_error < 1e-6:
    print("Parseval theorem is satisfied very closely.")
else:
    print("Parseval theorem is approximately satisfied with very small error.")

# ============================================================
# PART C - CHANNEL AND RECEIVER (CO3)
# ============================================================
print("\n" + "=" * 70)
print("PART C - CHANNEL AND RECEIVER (CO3)")
print("=" * 70)

EbN0_dB_test = 6
EbN0_lin_test = 10 ** (EbN0_dB_test / 10)

# Pass signal through mild LPF + AWGN
tx_filtered, noise, rx, sigma2, sigma = apply_channel_and_noise(
    waveform, h, Eb_theory, EbN0_dB_test, fs, Rb
)

print(f"Selected Eb/N0 = {EbN0_dB_test} dB")
print(f"Noise variance = {sigma2:.8e}")
print(f"Noise std dev  = {sigma:.8e}")

plt.figure(figsize=(12, 4))
plt.plot(time_axis * 1e3, waveform, label='Transmitted waveform', linewidth=1.2)
plt.title('Transmitted BPSK Waveform')
plt.xlabel('Time (ms)')
plt.ylabel('Amplitude (V)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 4))
plt.plot(time_axis * 1e3, rx, label='Filtered + noisy received waveform', color='orange', linewidth=1.2)
plt.title('Received Waveform After Mild LPF + AWGN')
plt.xlabel('Time (ms)')
plt.ylabel('Amplitude (V)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Correlator receiver
detected_corr, y_corr = correlator_receiver(rx, s1, N)
bit_errors_corr = np.sum(bits_plot != detected_corr)

print("\nCorrelator Receiver Results")
print("Transmitted bits     :", bits_plot)
print("Detected bits        :", detected_corr)
print("Number of bit errors :", bit_errors_corr)

# ============================================================
# PART D - FIR MATCHED FILTER (CO4)
# ============================================================
print("\n" + "=" * 70)
print("PART D - FIR MATCHED FILTER (CO4)")
print("=" * 70)

h_mf, mf_output, H_mf, f_mf = matched_filter_receiver(rx, s1, fs)

plt.figure(figsize=(10, 4))
plt.plot(np.arange(len(h_mf)), h_mf, linewidth=1.2)
plt.title('FIR Matched Filter Impulse Response')
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 4))
plt.plot(np.arange(len(mf_output)), mf_output, linewidth=1.2, color='purple')
plt.title('Matched Filter Output')
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 4))
plt.plot(f_mf / 1e3, np.abs(H_mf), linewidth=1.2)
plt.title('Frequency Response Magnitude of Matched Filter')
plt.xlabel('Frequency (kHz)')
plt.ylabel('|H(e^jω)|')
plt.grid(True)
plt.tight_layout()
plt.show()

# Decision from matched filter output
sample_indices = np.arange(N - 1, len(mf_output), N)
mf_samples = mf_output[sample_indices]
detected_mf = (mf_samples >= 0).astype(int)
bit_errors_mf = np.sum(bits_plot != detected_mf[:len(bits_plot)])

print("\nMatched Filter Receiver Results")
print("Detected bits        :", detected_mf[:len(bits_plot)])
print("Number of bit errors :", bit_errors_mf)

# Equivalence check
same_decisions = np.array_equal(detected_corr, detected_mf[:len(detected_corr)])
print(f"\nDo correlator and matched filter decisions match? {same_decisions}")

# ============================================================
# PART E - BER SIMULATION (CO5)
# ============================================================
print("\n" + "=" * 70)
print("PART E - BER SIMULATION (CO5)")
print("=" * 70)

BER_sim = simulate_ber(n_bits, N, h, EbN0_dB_range)
BER_theory = theoretical_ber(EbN0_dB_range)

print_ber_results(EbN0_dB_range, BER_sim, BER_theory)

plt.figure(figsize=(10, 5))
plt.semilogy(EbN0_dB_range, BER_sim, 'o-', label='Simulated BER', linewidth=2)
plt.semilogy(EbN0_dB_range, BER_theory, 's-', label='Theoretical BER', linewidth=2)
plt.title('BER Performance of BPSK')
plt.xlabel('Eb/N0 (dB)')
plt.ylabel('Bit Error Rate (BER)')
plt.grid(True, which='both')
plt.legend()
plt.tight_layout()
plt.show()

print("Observation:")
print("- BER decreases as Eb/N0 increases because the signal becomes stronger compared to noise.")
print("- At high Eb/N0, the simulated BER may fluctuate slightly because very few errors occur.")

# ============================================================
# PART F - SHANNON CAPACITY (CO6)
# ============================================================
print("\n" + "=" * 70)
print("PART F - SHANNON CAPACITY (CO6)")
print("=" * 70)

B, SNR_dB, SNR_lin, C = shannon_capacity(Rb)
SNR_dB_mark, SNR_lin_mark, C_mark = capacity_at_10dB(B)
EbN0_req, EbN0_shannon, gap = shannon_gap()

print_capacity_results(B, SNR_dB_mark, C_mark, EbN0_req, EbN0_shannon, gap)

plt.figure(figsize=(10, 5))
plt.plot(SNR_dB, C, 'o-', linewidth=2, label='Shannon Capacity')
plt.scatter(SNR_dB_mark, C_mark, color='red', s=80, zorder=5)
plt.annotate(f'10 dB, {C_mark:.2f} bps',
             xy=(SNR_dB_mark, C_mark),
             xytext=(11, C_mark + 800),
             arrowprops=dict(arrowstyle='->'))
plt.title('Shannon Capacity versus SNR')
plt.xlabel('SNR (dB)')
plt.ylabel('Capacity (bps)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

print("Discussion:")
print("- Capacity increases when SNR increases.")
print("- Capacity also increases with bandwidth.")
print("- Practical uncoded BPSK needs more Eb/N0 than Shannon limit.")
print("- Coding methods like LDPC and Turbo codes can reduce this gap.")

# ============================================================
# FINAL REPORT-READY VALUES
# ============================================================
print("\n" + "=" * 70)
print("FINAL REPORT-READY VALUES")
print("=" * 70)

print(f"Tb                     = {Tb:.6e} s")
print(f"N                      = {N}")
print(f"Eb (theory)            = {Eb_theory:.8e} J")
print(f"Lower first null       = {f_lower_null:.2f} Hz")
print(f"Upper first null       = {f_upper_null:.2f} Hz")
print(f"Null-to-null BW        = {BW:.2f} Hz")
print(f"Bandwidth B            = {B:.2f} Hz")
print(f"Capacity at 10 dB      = {C_mark:.2f} bps")
print(f"Gap to Shannon limit   = {gap:.2f} dB")

print("\nExecution completed successfully.")
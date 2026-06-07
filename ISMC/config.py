# config.py
# ------------------------------------------------------------
# Central place for all fixed parameters used in the ISMC project,
# including communication parameters, channel characteristics,
# and simulation settings.
# Industrial Sensor Monitoring Communication
# ------------------------------------------------------------

import numpy as np

# Fixed communication parameters
fc = 15e3          # carrier frequency in Hz
Rb = 1e3           # bit rate in bits per second
fs = 200e3         # sampling frequency in Hz
A = 1.0            # signal amplitude in volts

# 10-bit sequence used for waveform plotting
bits_plot = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 0])

# Mild low-pass channel impulse response
h = np.array([0.2, 0.6, 0.2])

# Number of bits for BER simulation
n_bits = 10**5

# Eb/N0 range for Batch 9
EbN0_dB_range = np.array([2, 4, 6, 8, 10, 12, 14])

# One representative Eb/N0 value for channel demonstration
EbN0_dB_demo = 6
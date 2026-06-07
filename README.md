# Industrial Sensor Monitoring Communication (ISMC)

A compact academic project that models and analyzes a **BPSK-based digital communication system** for industrial sensor monitoring using Python and LaTeX.

The repository combines simulation code, generated plots, and a structured technical report. The project demonstrates how binary information from an industrial sensor can be encoded, transmitted through a noisy channel, recovered at the receiver, and evaluated using key communication metrics such as signal energy, spectrum, BER, matched filtering, and channel capacity.

## Project Overview

This project was developed as part of **Mathematics for Communication Systems (MFCS)**. It presents both the theoretical and simulation-based study of a Binary Phase Shift Keying (BPSK) communication system.

The repository has two major parts:

- **Python code** for simulation, processing, and plot generation.
- **LaTeX report** for academic documentation of the work.

## Objectives

The project is designed to:

- Model BPSK signal generation for digital transmission.
- Compute bit energy and verify theoretical values.
- Visualize transmitted and received waveforms.
- Analyze magnitude spectrum and power spectral density.
- Simulate an AWGN channel.
- Study matched filter operation at the receiver.
- Evaluate BER performance over different SNR values.
- Analyze Shannon capacity versus SNR.
- Present all results in a professionally structured report.

## Repository Structure

```text
ISMC/
|-- core/
|   |-- ber.py
|   |-- bpsk.py
|   |-- capacity.py
|   |-- channel.py
|   `-- spectrum.py
|-- plots/
|   |-- 10-bit_wave.png
|   |-- ber.png
|   |-- bpsk.png
|   |-- fir_impulse_response.png
|   |-- frequency_response_matched_filter.png
|   |-- magnitude_spectrum_of_bpsk.png
|   |-- matched_filter_output.png
|   |-- power_spectral_density_bpsk.png
|   |-- received_wave.png
|   |-- shannon_capacity_vs_snr.png
|   `-- transmitted_bpsk.png
|-- report/
|   |-- appendix/
|   |-- assets/
|   |-- chapter/
|   |-- frontmatter/
|   |-- plots/
|   `-- main.tex
|-- config.py
|-- main.py
`-- .gitignore
```

## Main Components

### Python Modules

- `main.py` — main entry point of the simulation.
- `config.py` — stores system-level parameters.
- `core/bpsk.py` — generates BPSK symbols and waveforms.
- `core/channel.py` — applies channel effects.
- `core/spectrum.py` — computes spectral characteristics.
- `core/ber.py` — calculates BER values.
- `core/capacity.py` — evaluates channel capacity.

### Report Files

- `report/main.tex` — main LaTeX file.
- `report/frontmatter/` — title page, certificate, declaration, acknowledgement, abstract, and keywords.
- `report/chapter/` — chapter-wise project content.
- `report/appendix/` — source code and supplementary content.
- `report/plots/` — figures used in the report.
- `report/assets/` — static assets such as the logo.

## Tools and Technologies

- **Python**
- **NumPy**
- **Matplotlib**
- **LaTeX**
- **XeLaTeX**
- **Git and GitHub**

## How to Run the Project

### Prerequisites

Make sure the following are installed on your system:

- Python 3.x
- NumPy
- Matplotlib
- LaTeX distribution with **XeLaTeX** support

You can install the required Python packages using:

```bash
pip install numpy matplotlib
```

### Step 1: Clone the repository

```bash
git clone https://github.com/TAditya007/MFCS---Project-ISMC.git
cd MFCS---Project-ISMC
```

### Step 2: Check the project structure

Make sure the following key files are present:

- `main.py`
- `config.py`
- `core/`
- `plots/`
- `report/main.tex`

### Step 3: Run the Python project

Execute the main Python file:

```bash
python main.py
```

If your system uses `python3`, run:

```bash
python3 main.py
```

### Step 4: Verify generated outputs

After execution, check whether the plot files are available in the `plots/` folder. These figures are used in the report.

Expected outputs include:

- transmitted BPSK waveform
- received signal plot
- BER curve
- matched filter output
- spectrum and PSD plots
- Shannon capacity plot

### Step 5: Open the report folder

```bash
cd report
```

### Step 6: Compile the LaTeX report

Compile the report using **XeLaTeX**:

```bash
xelatex main.tex
```

Run the compile command 2–3 times if needed so that:

- table of contents is updated
- figure numbers are correct
- references and page numbers are resolved properly

### Step 7: View the final report

After compilation, the final PDF file will be available as:

```text
report/main.pdf
```

## Alternative: Run using VS Code

If you are using VS Code:

1. Open the project folder.
2. Run `main.py` using the Python extension.
3. Open the `report/` folder.
4. Open `main.tex`.
5. Select **XeLaTeX** as the compiler in LaTeX Workshop.
6. Build the report PDF.

## Output

The project produces:

- BPSK signal plots
- received waveform plots
- BER analysis results
- matched filter plots
- spectral analysis plots
- capacity analysis plots
- final academic report in PDF format

## Academic Scope

This repository is useful for students working on:

- digital communication systems
- signal analysis
- communication theory
- BER simulation
- LaTeX-based project documentation
- Python-based academic modeling

## Notes

- Use **XeLaTeX** instead of pdfLaTeX for the report.
- Generated LaTeX files such as `.aux`, `.log`, `.out`, and `.synctex.gz` are build files and not core source files.
- The `plots/` folder stores the generated figures used in the documentation.

## Repository Link

[https://github.com/TAditya007/MFCS---Project-ISMC](https://github.com/TAditya007/MFCS---Project-ISMC)

# MoS2 particulate-photocatalyst calculation codes

This repository contains two Python programs supporting calculations for
MoS2-based particulate photocatalysts for overall water splitting:

1. solar-to-hydrogen (STH) efficiency;
2. lattice mismatch between two monolayers.

No molecular-dynamics structures, bond-analysis data, or additional datasets
are included.

## 1. STH-efficiency.py

`STH-efficiency.py` estimates the ideal solar-to-hydrogen conversion efficiency
from:

- an ASTM AM1.5 solar spectrum;
- valence-band maximum and conduction-band minimum energies;
- HER and OER redox levels;
- optional HER and OER overpotentials.

The supplied defaults evaluate the MoS2/PtSe2 and MoS2/WS2 particulate
photocatalyst systems for:

- an ideal zero-overpotential case;
- HER and OER overpotentials of 0.20 and 0.60 eV, respectively.

### Requirements

- Python 3.10 or newer;
- NumPy;
- pandas;
- openpyxl when an `.xlsx` spectrum is used.

Install the required packages with:

```bash
python -m pip install numpy pandas openpyxl
```

### Solar-spectrum format

The default settings expect:

- two non-data rows at the top of the file;
- wavelength in column 1, expressed in nm;
- spectral irradiance in column 3, expressed in W m^-2 nm^-1.

Excel, CSV, and whitespace-delimited text files are accepted. Column positions
and skipped rows can be changed using command-line options.

### Run the calculation

```bash
python STH-efficiency.py --spectrum ASTM_G173.xlsx
```

Display every available option with:

```bash
python STH-efficiency.py --help
```

For example, calculate only the case with overpotentials:

```bash
python STH-efficiency.py --spectrum ASTM_G173.xlsx --scenario overpotential
```

The program reports:

- the minimum excitation energy for each absorber;
- the individual STH contribution of each absorber;
- the total ideal STH efficiency.

### Method and assumptions

For each absorber, the minimum excitation energy is

```text
E_min = E_g + max(0, eta_HER - DeltaE_HER)
              + max(0, eta_OER - DeltaE_OER)
```

where `E_g` is the band gap and `DeltaE_HER` and `DeltaE_OER` are the available
band-edge driving energies. The photon flux is integrated over non-overlapping
energy intervals, and 1.23 eV per transferred electron is treated as useful
chemical energy.

This is an idealized theoretical estimate. It does not include optical losses,
charge recombination, kinetic losses beyond the specified overpotentials,
mass-transfer limitations, or wavelength-dependent quantum yields.

To evaluate another material system, edit the `SYSTEMS` dictionary near the
top of `STH-efficiency.py`. All band-edge energies are in eV relative to vacuum.

## 2. lattice-mismatch-code-for-MoS2-PtSe2.py

This program searches for low-mismatch square supercell combinations between
two hexagonal monolayers. The default calculation uses:

- MoS2 lattice constant: 3.1809599400 Angstrom;
- PtSe2 lattice constant: 3.7453484619855373 Angstrom;
- maximum mismatch: 3%;
- maximum total atoms: 400;
- three atoms per primitive cell for each monolayer.

The mismatch is defined relative to the first material:

```text
mismatch (%) = abs(L1 - L2) / L1 * 100
```

### Run the calculation

```bash
python lattice-mismatch-code-for-MoS2-PtSe2.py
```

The default leading result is:

```text
MoS2 7x7 / PtSe2 6x6
Lattice mismatch: 0.922324%
Total atoms: 255
```

Display all available options with:

```bash
python lattice-mismatch-code-for-MoS2-PtSe2.py --help
```

For example, evaluate another pair of lattice constants:

```bash
python lattice-mismatch-code-for-MoS2-PtSe2.py \
  --material-1 Material-A \
  --material-2 Material-B \
  --lattice-1 3.18 \
  --lattice-2 3.20
```

The program prints every configuration satisfying the selected mismatch and
atom-count limits, followed by the best-ranked configurations.

## Reproducibility notes

- Input values are not fitted, normalized, or modified automatically.
- Review the band edges, redox levels, overpotentials, lattice constants, and
  atom counts before applying the calculations to another system.
- Numerical results should be reported together with the input values and the
  assumptions used in the calculation.

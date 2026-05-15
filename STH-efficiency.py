mport numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.integrate import quad

# --------------------------------------------------
# Constants
# --------------------------------------------------

h = 6.6262e-34
c = 2.99792458e8
eV = 1.60217646e-19
kb = 1.3806488e-23

# --------------------------------------------------
# Import AM1.5 solar spectrum
# --------------------------------------------------

file_path = r"C:\Users\sypot\Desktop\MoS2-PtSe2\manuscript-writing-related\efficiency formula\ASTM G173-03 Reference Spectra__neat.xls"

solar_raw = pd.read_excel(file_path, header=None)

# Drop first two rows and take columns 1 and 3
solar = solar_raw.iloc[2:, [0, 2]].astype(float).values

# --------------------------------------------------
# Convert wavelength (nm) -> energy (eV)
# --------------------------------------------------

solar[:, 0] = ((h * c) / (solar[:, 0] * 1e-9)) / eV

# --------------------------------------------------
# Convert spectrum
# --------------------------------------------------

solar[:, 1] = (
    solar[:, 1]
    * (h * c)
    / ((solar[:, 0] * eV) ** 2 * 1e-9)
    * eV
)

# --------------------------------------------------
# Interpolation
# --------------------------------------------------

funsolar = interp1d(
    solar[:, 0],
    solar[:, 1],
    kind='linear',
    bounds_error=False,
    fill_value=0
)

# --------------------------------------------------
# Total solar power
# --------------------------------------------------

Suntot, _ = quad(lambda x: funsolar(x), 0, 4.5)

# --------------------------------------------------
# Photon flux
# --------------------------------------------------

def Qsfun(Egs1):

    Qs = []

    for i in range(len(Egs1) - 1):

        val, _ = quad(
            lambda x: funsolar(x) / (x * eV),
            Egs1[i] / eV,
            Egs1[i + 1] / eV
        )

        Qs.append(val)

    return Qs

# --------------------------------------------------
# Minimum excitation energy
# --------------------------------------------------

def Emin(Evbm, Ecbm, Eher, Eoer):

    kH2 = Ecbm - Eher
    kO2 = Eoer - Evbm

    return (
        Ecbm - Evbm
        + (0 if kH2 >= HERoverp else HERoverp - kH2)
        + (0 if kO2 >= OERoverp else OERoverp - kO2)
    )

# --------------------------------------------------
# Main function
# --------------------------------------------------

def MultijunctionCell(Eedges0, Eher, Eoer):

    # Add band gaps
    Eedges1 = []

    for item in Eedges0:

        Evbm = item[0]
        Ecbm = item[1]
        name = item[2]

        Eg = Ecbm - Evbm

        Eedges1.append([Evbm, Ecbm, name, Eg])

    # Sort according to band gap
    Eedges1.sort(key=lambda x: x[3])

    # Minimum required energies
    Eedges = [
        Emin(item[0], item[1], Eher, Eoer)
        for item in Eedges1
    ]

    # Upper limit = 4.5 eV
    Egs1 = Eedges + [4.5 * eV]

    # Photon flux
    Qs = Qsfun(Egs1)

    Qs = [max(q, 0) for q in Qs]

    # STH efficiency
    ans = [(q * (1.23 * eV) / Suntot) for q in Qs]

    total_sth = sum(ans) * 100

    print(
        f"Total STH = {total_sth:.4f}%; "
        f"individual contribution = "
        f"{[round(a * 100, 5) for a in ans]}%"
    )

    print(Eedges1)

    return total_sth

# --------------------------------------------------
# Example 1
# --------------------------------------------------

HERoverp = 0 * eV
OERoverp = 0 * eV

MultijunctionCell(
    [
        [-5.85 * eV, -4.14 * eV, "PtSe2"],
        [-6.44 * eV, -4.21 * eV, "MoS2"]
    ],
    -4.44 * eV,
    -5.67 * eV
)

# --------------------------------------------------
# Example 2
# --------------------------------------------------

HERoverp = 0.2 * eV
OERoverp = 0.6 * eV

MultijunctionCell(
    [
        [-5.85 * eV, -4.14 * eV, "PtSe2"],
        [-6.44 * eV, -4.21 * eV, "MoS2"]
    ],
    -4.44 * eV,
    -5.67 * eV
)

# --------------------------------------------------
# Example 3
# --------------------------------------------------

HERoverp = 0.2 * eV
OERoverp = 0.6 * eV

MultijunctionCell(
    [
        [-6.44 * eV, -4.21 * eV, "MoS2"],
        [-6.08 * eV, -3.89 * eV, "WS2"]
    ],
    -4.44 * eV,
    -5.67 * eV
)

# --------------------------------------------------
# Example 4
# --------------------------------------------------

HERoverp = 0 * eV
OERoverp = 0 * eV

MultijunctionCell(
    [
        [-6.44 * eV, -4.21 * eV, "MoS2"],
        [-6.08 * eV, -3.89 * eV, "WS2"]
    ],
    -4.44 * eV,
    -5.67 * eV
)

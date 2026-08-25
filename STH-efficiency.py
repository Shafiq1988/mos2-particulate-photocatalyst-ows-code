"""Estimate ideal solar-to-hydrogen efficiency for particulate photocatalysts.

The calculation combines user-supplied band-edge positions with an ASTM AM1.5
solar spectrum. Energies in ``SYSTEMS`` are in electronvolts (eV), referenced
to the vacuum level.

Run with: ``python STH-efficiency.py --spectrum ASTM_G173.xlsx``

The defaults report MoS2/PtSe2 and MoS2/WS2 for zero overpotential and for
0.20 eV HER / 0.60 eV OER overpotentials. Edit ``SYSTEMS`` to evaluate another
particulate photocatalyst.

Required packages: numpy, pandas, and openpyxl for XLSX input.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

import numpy as np
import pandas as pd


PLANCK_CONSTANT = 6.6262e-34  # J s
SPEED_OF_LIGHT = 2.99792458e8  # m s^-1
ELEMENTARY_CHARGE = 1.60217646e-19  # J eV^-1
WATER_SPLITTING_ENERGY = 1.23  # eV per transferred electron


@dataclass(frozen=True)
class BandEdges:
    """Valence- and conduction-band edges for one absorber, in eV."""

    name: str
    vbm: float
    cbm: float

    @property
    def band_gap(self) -> float:
        return self.cbm - self.vbm


@dataclass(frozen=True)
class STHResult:
    """Calculated efficiency and the energy assigned to each absorber."""

    total_percent: float
    contributions_percent: tuple[tuple[str, float], ...]
    excitation_thresholds_ev: tuple[tuple[str, float], ...]


SYSTEMS: dict[str, tuple[BandEdges, ...]] = {
    "MoS2/PtSe2": (
        BandEdges("PtSe2", vbm=-5.85, cbm=-4.14),
        BandEdges("MoS2", vbm=-6.44, cbm=-4.21),
    ),
    "MoS2/WS2": (
        BandEdges("MoS2", vbm=-6.44, cbm=-4.21),
        BandEdges("WS2", vbm=-6.08, cbm=-3.89),
    ),
}


def load_am15_spectrum(
    path: str | Path,
    *,
    skip_rows: int = 2,
    wavelength_column: int = 0,
    irradiance_column: int = 2,
) -> Callable[[float], float]:
    """Interpolate an AM1.5 spectrum as irradiance versus photon energy.

    Wavelength must be in nm and irradiance in W m^-2 nm^-1. Excel, CSV, and
    whitespace-delimited text files are accepted.
    """

    source = Path(path).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(f"Solar-spectrum file not found: {source}")

    suffix = source.suffix.lower()
    if suffix in {".xls", ".xlsx"}:
        raw = pd.read_excel(source, header=None, skiprows=skip_rows)
    elif suffix == ".csv":
        raw = pd.read_csv(source, header=None, skiprows=skip_rows)
    else:
        raw = pd.read_csv(source, sep=r"\s+", header=None, skiprows=skip_rows)

    largest_index = max(wavelength_column, irradiance_column)
    if raw.shape[1] <= largest_index:
        raise ValueError(
            f"Spectrum has {raw.shape[1]} columns; column {largest_index} "
            "was requested."
        )

    spectrum = raw.iloc[:, [wavelength_column, irradiance_column]].apply(
        pd.to_numeric, errors="coerce"
    )
    spectrum = spectrum.dropna().to_numpy(dtype=float)
    if spectrum.size == 0:
        raise ValueError("No numeric wavelength/irradiance rows were found.")

    wavelength_nm = spectrum[:, 0]
    irradiance_per_nm = spectrum[:, 1]
    if np.any(wavelength_nm <= 0) or np.any(irradiance_per_nm < 0):
        raise ValueError("Wavelengths must be positive and irradiance nonnegative.")

    energy_ev = PLANCK_CONSTANT * SPEED_OF_LIGHT / (
        wavelength_nm * 1e-9 * ELEMENTARY_CHARGE
    )
    # |d(lambda_nm)/d(E_eV)| converts W m^-2 nm^-1 to W m^-2 eV^-1.
    jacobian = (
        PLANCK_CONSTANT
        * SPEED_OF_LIGHT
        * 1e9
        / (ELEMENTARY_CHARGE * energy_ev**2)
    )
    irradiance_per_ev = irradiance_per_nm * jacobian

    order = np.argsort(energy_ev)
    energy_ev = energy_ev[order]
    irradiance_per_ev = irradiance_per_ev[order]
    if np.any(np.diff(energy_ev) <= 0):
        raise ValueError("The converted energy grid contains duplicate values.")

    return lambda energy: float(
        np.interp(energy, energy_ev, irradiance_per_ev, left=0.0, right=0.0)
    )


def integrate(
    function: Callable[[float], float],
    lower: float,
    upper: float,
    *,
    points: int = 20_001,
) -> float:
    """Numerically integrate a scalar function using the trapezoidal rule."""

    if upper <= lower:
        return 0.0
    grid = np.linspace(lower, upper, points)
    values = np.fromiter((function(float(value)) for value in grid), dtype=float)
    return float(np.trapezoid(values, grid))


def minimum_excitation_energy(
    material: BandEdges,
    *,
    her_level: float,
    oer_level: float,
    her_overpotential: float,
    oer_overpotential: float,
) -> float:
    """Calculate the minimum excitation energy for one absorber, in eV."""

    if material.band_gap <= 0:
        raise ValueError(f"{material.name} has a nonpositive band gap.")
    her_driving_energy = material.cbm - her_level
    oer_driving_energy = oer_level - material.vbm
    return (
        material.band_gap
        + max(0.0, her_overpotential - her_driving_energy)
        + max(0.0, oer_overpotential - oer_driving_energy)
    )


def calculate_sth_efficiency(
    spectrum: Callable[[float], float],
    materials: Iterable[BandEdges],
    *,
    her_level: float = -4.44,
    oer_level: float = -5.67,
    her_overpotential: float = 0.0,
    oer_overpotential: float = 0.0,
    maximum_energy: float = 4.5,
) -> STHResult:
    """Calculate ideal STH efficiency using non-overlapping photon intervals."""

    if min(her_overpotential, oer_overpotential) < 0:
        raise ValueError("Overpotentials cannot be negative.")
    if maximum_energy <= 0:
        raise ValueError("maximum_energy must be positive.")

    thresholds = [
        (
            material,
            minimum_excitation_energy(
                material,
                her_level=her_level,
                oer_level=oer_level,
                her_overpotential=her_overpotential,
                oer_overpotential=oer_overpotential,
            ),
        )
        for material in materials
    ]
    thresholds.sort(key=lambda item: item[1])
    if not thresholds:
        raise ValueError("At least one absorber must be supplied.")

    total_solar_power = integrate(spectrum, 0.0, maximum_energy)
    if total_solar_power <= 0:
        raise ValueError("Integrated solar power is zero; check the spectrum columns.")

    upper_limits = [threshold for _, threshold in thresholds[1:]] + [maximum_energy]
    contributions: list[tuple[str, float]] = []
    for (material, lower), upper in zip(thresholds, upper_limits):
        lower = max(0.0, lower)
        upper = min(maximum_energy, upper)
        if lower >= upper:
            efficiency_percent = 0.0
        else:
            photon_flux = integrate(
                lambda energy: spectrum(energy) / (energy * ELEMENTARY_CHARGE),
                lower,
                upper,
            )
            useful_power = photon_flux * WATER_SPLITTING_ENERGY * ELEMENTARY_CHARGE
            efficiency_percent = 100.0 * useful_power / total_solar_power
        contributions.append((material.name, efficiency_percent))

    return STHResult(
        total_percent=sum(value for _, value in contributions),
        contributions_percent=tuple(contributions),
        excitation_thresholds_ev=tuple(
            (material.name, threshold) for material, threshold in thresholds
        ),
    )


def print_result(system_name: str, scenario: str, result: STHResult) -> None:
    """Print one result in a compact, readable format."""

    print(f"\n{system_name} - {scenario}")
    print("-" * 60)
    for name, threshold in result.excitation_thresholds_ev:
        print(f"Minimum excitation energy ({name}): {threshold:.4f} eV")
    for name, contribution in result.contributions_percent:
        print(f"STH contribution ({name}): {contribution:.4f}%")
    print(f"Total STH efficiency: {result.total_percent:.4f}%")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spectrum", required=True, help="AM1.5 XLS/XLSX/CSV/TXT file")
    parser.add_argument("--skip-rows", type=int, default=2)
    parser.add_argument("--wavelength-column", type=int, default=0)
    parser.add_argument("--irradiance-column", type=int, default=2)
    parser.add_argument("--maximum-energy", type=float, default=4.5, help="eV")
    parser.add_argument(
        "--scenario",
        choices=("both", "ideal", "overpotential"),
        default="both",
    )
    parser.add_argument("--her-overpotential", type=float, default=0.20, help="eV")
    parser.add_argument("--oer-overpotential", type=float, default=0.60, help="eV")
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    spectrum = load_am15_spectrum(
        args.spectrum,
        skip_rows=args.skip_rows,
        wavelength_column=args.wavelength_column,
        irradiance_column=args.irradiance_column,
    )

    scenarios = []
    if args.scenario in {"both", "ideal"}:
        scenarios.append(("ideal (zero overpotential)", 0.0, 0.0))
    if args.scenario in {"both", "overpotential"}:
        scenarios.append(
            ("with overpotentials", args.her_overpotential, args.oer_overpotential)
        )

    for system_name, materials in SYSTEMS.items():
        for label, her_overpotential, oer_overpotential in scenarios:
            result = calculate_sth_efficiency(
                spectrum,
                materials,
                her_overpotential=her_overpotential,
                oer_overpotential=oer_overpotential,
                maximum_energy=args.maximum_energy,
            )
            print_result(system_name, label, result)


if __name__ == "__main__":
    main()

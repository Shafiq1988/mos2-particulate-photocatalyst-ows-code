"""Find low-mismatch square supercells for two hexagonal monolayers.

The defaults reproduce the MoS2/PtSe2 search used in this repository. Lattice
constants are in Angstrom. Mismatch is ``abs(L1 - L2) / L1 * 100``. The atom
count assumes three atoms per primitive cell for both monolayers.

Run with: ``python lattice-mismatch-code-for-MoS2-PtSe2.py``
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Configuration:
    """One commensurate-supercell candidate."""

    multiple_1: int
    multiple_2: int
    length_1: float
    length_2: float
    mismatch_percent: float
    atoms_1: int
    atoms_2: int
    selection: str

    @property
    def total_atoms(self) -> int:
        return self.atoms_1 + self.atoms_2


def find_configurations(
    lattice_1: float,
    lattice_2: float,
    *,
    atoms_per_cell_1: int = 3,
    atoms_per_cell_2: int = 3,
    maximum_multiple: int = 15,
    mismatch_limit_percent: float = 3.0,
    atom_limit: int = 400,
) -> list[Configuration]:
    """Return valid supercell pairs sorted by increasing lattice mismatch."""

    if min(lattice_1, lattice_2) <= 0:
        raise ValueError("Lattice constants must be positive.")
    if min(atoms_per_cell_1, atoms_per_cell_2, maximum_multiple, atom_limit) <= 0:
        raise ValueError("Atom counts, limits, and multiples must be positive.")
    if mismatch_limit_percent < 0:
        raise ValueError("The mismatch limit cannot be negative.")

    configurations: list[Configuration] = []
    seen_pairs: set[tuple[int, int]] = set()

    for multiple_1 in range(1, maximum_multiple + 1):
        length_1 = multiple_1 * lattice_1
        estimated_multiple_2 = length_1 / lattice_2
        candidates = (
            (math.floor(estimated_multiple_2), "floor"),
            (math.ceil(estimated_multiple_2), "ceiling"),
        )

        for multiple_2, selection in candidates:
            pair = (multiple_1, multiple_2)
            if multiple_2 <= 0 or pair in seen_pairs:
                continue
            seen_pairs.add(pair)

            length_2 = multiple_2 * lattice_2
            mismatch_percent = abs(length_1 - length_2) / length_1 * 100.0
            atoms_1 = atoms_per_cell_1 * multiple_1**2
            atoms_2 = atoms_per_cell_2 * multiple_2**2
            total_atoms = atoms_1 + atoms_2

            if mismatch_percent < mismatch_limit_percent and total_atoms < atom_limit:
                configurations.append(
                    Configuration(
                        multiple_1=multiple_1,
                        multiple_2=multiple_2,
                        length_1=length_1,
                        length_2=length_2,
                        mismatch_percent=mismatch_percent,
                        atoms_1=atoms_1,
                        atoms_2=atoms_2,
                        selection=selection,
                    )
                )

    return sorted(
        configurations,
        key=lambda item: (item.mismatch_percent, item.total_atoms),
    )


def print_table(
    configurations: list[Configuration],
    *,
    material_1: str,
    material_2: str,
) -> None:
    """Print all configurations without requiring an external table package."""

    headers = (
        f"{material_1} n",
        f"{material_2} n",
        "L1 (Angstrom)",
        "L2 (Angstrom)",
        "Mismatch (%)",
        f"{material_1} atoms",
        f"{material_2} atoms",
        "Total atoms",
        "Choice",
    )
    rows = [
        (
            item.multiple_1,
            item.multiple_2,
            f"{item.length_1:.6f}",
            f"{item.length_2:.6f}",
            f"{item.mismatch_percent:.6f}",
            item.atoms_1,
            item.atoms_2,
            item.total_atoms,
            item.selection,
        )
        for item in configurations
    ]
    widths = [
        max(len(str(header)), *(len(str(row[index])) for row in rows))
        for index, header in enumerate(headers)
    ]
    format_row = "  ".join(f"{{:<{width}}}" for width in widths).format

    print(format_row(*headers))
    print(format_row(*("-" * width for width in widths)))
    for row in rows:
        print(format_row(*row))


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--material-1", default="MoS2")
    parser.add_argument("--material-2", default="PtSe2")
    parser.add_argument(
        "--lattice-1", type=float, default=3.1809599400, help="Angstrom"
    )
    parser.add_argument(
        "--lattice-2", type=float, default=3.7453484619855373, help="Angstrom"
    )
    parser.add_argument("--atoms-per-cell-1", type=int, default=3)
    parser.add_argument("--atoms-per-cell-2", type=int, default=3)
    parser.add_argument("--maximum-multiple", type=int, default=15)
    parser.add_argument("--mismatch-limit", type=float, default=3.0, help="percent")
    parser.add_argument("--atom-limit", type=int, default=400)
    parser.add_argument("--top", type=int, default=3)
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    configurations = find_configurations(
        args.lattice_1,
        args.lattice_2,
        atoms_per_cell_1=args.atoms_per_cell_1,
        atoms_per_cell_2=args.atoms_per_cell_2,
        maximum_multiple=args.maximum_multiple,
        mismatch_limit_percent=args.mismatch_limit,
        atom_limit=args.atom_limit,
    )

    print(f"Lattice-mismatch analysis: {args.material_1}/{args.material_2}")
    print(
        f"Criteria: mismatch < {args.mismatch_limit:.3f}% and "
        f"total atoms < {args.atom_limit}\n"
    )
    if not configurations:
        print("No configurations satisfy the selected criteria.")
        return

    print_table(
        configurations,
        material_1=args.material_1,
        material_2=args.material_2,
    )

    print(f"\nTop {min(args.top, len(configurations))} configuration(s):")
    for rank, item in enumerate(configurations[: args.top], start=1):
        print(
            f"{rank}. {args.material_1} {item.multiple_1}x{item.multiple_1} / "
            f"{args.material_2} {item.multiple_2}x{item.multiple_2}: "
            f"{item.mismatch_percent:.6f}% mismatch, "
            f"{item.total_atoms} atoms ({item.selection})"
        )


if __name__ == "__main__":
    main()

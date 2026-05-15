mport math
from tabulate import tabulate

# Lattice constants for MoS2 and PtSe2
a1 = 3.1809599400  # MoS2 lattice constant in Å
a2 = 3.7453484619855373  # PtSe2 lattice constant in Å

mismatch_threshold = 0.03  # Maximum acceptable mismatch (3%)
atom_limit = 400  # Maximum total atoms for practical supercells

# Print header
print("Lattice Mismatch Analysis for MoS2/PtSe2 Heterostructure")
print("=" * 60)
print("n1: Supercell multiple for MoS2, n2: Supercell multiple for PtSe2")
print("l1: Supercell length for MoS2, l2/l3: Supercell length for PtSe2")
print("Mismatch: Relative lattice mismatch, Atoms: Total (3*n1^2 + 3*n2^2)")
print("-" * 60)

# Collect results
results = []

for n1 in range(1, 16):  # Extended range to find more options

    # Ratio of supercell lengths
    tmp = n1 * a1 / a2

    # Supercell length for MoS2
    l1 = n1 * a1

    # ---------------- Floor case ----------------
    n2_floor = math.floor(tmp)
    l2 = n2_floor * a2

    mismatch_floor = abs((l1 - l2) / l1)

    atoms_mos2 = 3 * n1 * n1  # 3 atoms per unit cell
    atoms_ptse2_floor = 3 * n2_floor * n2_floor

    total_atoms_floor = atoms_mos2 + atoms_ptse2_floor

    # Store valid floor configuration
    if (
        mismatch_floor < mismatch_threshold
        and total_atoms_floor < atom_limit
        and n2_floor > 0
    ):
        results.append([
            n1,
            n2_floor,
            l1,
            l2,
            mismatch_floor * 100,  # convert to %
            atoms_mos2,
            atoms_ptse2_floor,
            total_atoms_floor,
            "Floor"
        ])

    # ---------------- Ceiling case ----------------
    n2_ceiling = math.ceil(tmp)
    l3 = n2_ceiling * a2

    mismatch_ceiling = abs((l1 - l3) / l1)

    atoms_ptse2_ceiling = 3 * n2_ceiling * n2_ceiling

    total_atoms_ceiling = atoms_mos2 + atoms_ptse2_ceiling

    # Store valid ceiling configuration
    if (
        mismatch_ceiling < mismatch_threshold
        and total_atoms_ceiling < atom_limit
    ):
        results.append([
            n1,
            n2_ceiling,
            l1,
            l3,
            mismatch_ceiling * 100,  # convert to %
            atoms_mos2,
            atoms_ptse2_ceiling,
            total_atoms_ceiling,
            "Ceiling"
        ])

# Sort results by mismatch
sorted_results = sorted(results, key=lambda x: x[4])

# Display results in a table
if len(sorted_results) > 0:

    print(f"Possible Configurations with mismatch < {mismatch_threshold*100}% "
          f"and atoms < {atom_limit}:\n")

    headers = [
        "n1",
        "n2",
        "l1 (Å)",
        "l2/l3 (Å)",
        "Mismatch (%)",
        "MoS2 Atoms",
        "PtSe2 Atoms",
        "Total Atoms",
        "n2 Type"
    ]

    print(tabulate(sorted_results, headers=headers, floatfmt=".6f"))

else:
    print(f"No configurations found with mismatch < "
          f"{mismatch_threshold*100}% and < {atom_limit} atoms.")

# Highlight top 3 configurations
print("=" * 60)
print("Top 3 Configurations with Lowest Mismatch:")

if len(sorted_results) > 0:

    for i, config in enumerate(sorted_results[:3], start=1):

        print(f"Configuration {i}:")
        print(f"MoS2 Supercell: {config[0]} × {config[0]}")
        print(f"PtSe2 Supercell: {config[1]} × {config[1]}")
        print(f"Supercell Length (MoS2): {config[2]:.6f} Å")
        print(f"Supercell Length (PtSe2): {config[3]:.6f} Å")
        print(f"Lattice Mismatch: {config[4]:.6f}%")
        print(f"Atoms (MoS2): {config[5]} "
              f"(1 Mo, 2 S per unit cell)")
        print(f"Atoms (PtSe2): {config[6]} "
              f"(1 Pt, 2 Se per unit cell)")
        print(f"Total Atoms: {config[7]} ({config[8]})")
        print("")

else:
    print(f"No configurations found with mismatch < "
          f"{mismatch_threshold*100}% and < {atom_limit} atoms.")
Lattice Mismatch Analysis for MoS2/PtSe2 Heterostructure

============================================================

n1: Supercell multiple for MoS2, n2: Supercell multiple for PtSe2

l1: Supercell length for MoS2, l2/l3: Supercell length for PtSe2

Mismatch: Relative lattice mismatch, Atoms: Total (3*n1^2 + 3*n2^2)

------------------------------------------------------------

Possible Configurations with mismatch < 3.0% and atoms < 400:

  n1    n2     l1 (Å)    l2/l3 (Å)    Mismatch (%)    MoS2 Atoms    PtSe2 Atoms    Total Atoms  n2 Type
----  ----  ---------  -----------  --------------  ------------  -------------  -------------  ---------
   7     6  22.266720    22.472091        0.922324           147            108            255  Ceiling
   6     5  19.085760    18.726742        1.881074           108             75            183  Floor
============================================================

Top 3 Configurations with Lowest Mismatch:

Configuration 1:

MoS2 Supercell: 7 × 7

PtSe2 Supercell: 6 × 6

Supercell Length (MoS2): 22.266720 Å

Supercell Length (PtSe2): 22.472091 Å

Lattice Mismatch: 0.922324%

Atoms (MoS2): 147 (1 Mo, 2 S per unit cell)

Atoms (PtSe2): 108 (1 Pt, 2 Se per unit cell)

Total Atoms: 255 (Ceiling)

Configuration 2:

MoS2 Supercell: 6 × 6

PtSe2 Supercell: 5 × 5

Supercell Length (MoS2): 19.085760 Å

Supercell Length (PtSe2): 18.726742 Å

Lattice Mismatch: 1.881074%

Atoms (MoS2): 108 (1 Mo, 2 S per unit cell)

Atoms (PtSe2): 75 (1 Pt, 2 Se per unit cell)

Total Atoms: 183 (Floor)

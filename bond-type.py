# -*- coding: utf-8 -*-

from ase.io import read
import numpy as np
import matplotlib.pyplot as plt

# Read trajectory
traj = read("XDATCAR", index=":")

# Atom indices
s_indices  = list(range(0, 72))
mo_indices = list(range(72, 108))
pt_indices = list(range(108, 133))
se_indices = list(range(133, 183))

mo_s_dist = []
pt_se_dist = []

for atoms in traj:

    mo_step = []
    pt_step = []

    # Mo-S bonds
    for mo in mo_indices:
        dists = [atoms.get_distance(mo, s, mic=True) for s in s_indices]
        mo_step.append(np.mean(sorted(dists)[:6]))

    # Pt-Se bonds
    for pt in pt_indices:
        dists = [atoms.get_distance(pt, se, mic=True) for se in se_indices]
        pt_step.append(np.mean(sorted(dists)[:6]))

    mo_s_dist.append(np.mean(mo_step))
    pt_se_dist.append(np.mean(pt_step))

# Time axis
time = np.arange(len(traj))

# Save data
np.savetxt(
    "bond_MoS2_PtSe2.dat",
    np.column_stack((time, mo_s_dist, pt_se_dist)),
    header="Step Mo-S(A) Pt-Se(A)"
)

# Plot
plt.figure(figsize=(8,5))

plt.plot(time, mo_s_dist, label="Mo-S")
plt.plot(time, pt_se_dist, label="Pt-Se")

plt.xlabel("MD Step")
plt.ylabel("Average nearest-neighbor bond distance (A)")

plt.legend()
plt.tight_layout()

plt.savefig("bond_MoS2_PtSe2.png", dpi=300)

print("Saved successfully")

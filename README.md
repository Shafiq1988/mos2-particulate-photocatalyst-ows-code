# MoS2-photoanode-ows-data
The repository contains the data and codes associated with the manuscript entitled:
“Photocorrosion-Inhibited MoS₂-Based Heterostructures for Stable Photoanodes in Neutral pH Overall Water Splitting”
All scripts are written in Python and are briefly described below.
1. bond-type.py
This script was designed for the statistical analysis of the average nearest neighbour bond distances Mo-S, W-S, Pt-Se of the heterostructures in water as a function of time (ps). The script can be excuted by using the Atomic Simulation Environment (ASE) with command -> python bond-type.py
The script output includes:
Time-dependent bond length evolution (in ps)
Corresponding data files (.dat)
Plots of bond statistics and structural stability (png)
2. STH-efficiency.py
This code was developed to calculates the solar-to-hydrogen (STH) conversion efficiency of hybrid photocatalyst systems based on band-edge positions and the AM1.5 solar spectrum.
It can be run with any standard Python version:
python STH-efficiency.py
Before running the script, please ensure that:
The file path to the solar spectrum is correctly specified
The band-edge values and band gaps are updated for the desired material system
The script outputs:
Total STH efficiency
Individual contributions from each material in the heterostructure
3. lattice-mismatch-code-for-MoS2-PtSe2.py
This code evaluates lattice compatibility between two materials by calculating lattice mismatch for different combinations for example the lattice mistmatch was 0.5% for MoS2/WS2 and 0.9% for Mos2/PtSe2.
Note: Users must input the lattice parameters of the two materials of interest. The script then identifies the optimal heterostructure combinations with minimal lattice mismatch.
The output includes:
Best matching lattice configurations
Corresponding mismatch percentages

This set of tools is intended to support reproducibility and facilitate the design and analysis of 2D heterostructures for photocatalytic applications.

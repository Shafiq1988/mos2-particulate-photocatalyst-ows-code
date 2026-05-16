# MoS₂-photoanode-ows-data
The repository contains the data and codes associated with the manuscript entitled:
“Photocorrosion-Inhibited MoS₂-Based Heterostructures for Stable Photoanodes in Neutral pH Overall Water Splitting”
All codes are written in Python and are freely available for use. The descriptions and usage instructions for the Python codes are provided below.
# 1. bond-type.py
This code was designed for the statistical analysis of the average nearest neighbour bond distances Mo-S, W-S and Pt-Se of the heterostructures in water as a function of time (ps). The script can be excuted by using the Atomic Simulation Environment (ASE) with command -> python bond-type.py.
The script output includes:
Time-dependent bond length evolution (in ps)
corresponding data files (.dat)
Plots of bond statistics and structural stability (png).
# 2. STH-efficiency.py
This code was developed to calculates the solar-to-hydrogen (STH) conversion efficiency of hybrid photocatalyst systems based on band-edge positions and the AM1.5 solar spectrum.
It can be run with any standard Python version:
python STH-efficiency.py.
Before running the code, please ensure that:
the file path to the solar spectrum is correctly specified and
the band-edges values are updated for the desired material system.
The code outputs:
Total STH efficiency
Individual contributions from each material in the heterostructure.
# 3. Lattice-mismatch-code-for-MoS₂-PtSe₂.py
This code evaluates lattice compatibility between two materials by calculating lattice mismatch for different combinations for example the lattice mistmatch was 0.5% for MoS₂/WS₂ and 0.9% for MoS₂/PtSe2.
Note: Users must input the lattice parameters of the two materials of interest. The code then identifies the optimal heterostructure combinations with minimal lattice mismatch.
The output includes:
Best matching lattice configurations
corresponding mismatch percentages
# 4. MoS₂/WS₂_MD_cif-files
This folder contains all the structure files (cif) of the initial and final states of MoS₂/WS₂ heterostructure at 300K and 400K temperatures.The sequence are accroding to the figures in the manuscript.
# 5. MoS₂/PtSe₂_MD_cif-files 
This folder contains all the structure files (cif) of the initial and final states of MoS₂/PtSe₂ heterostructure at 300K and 400K temperatures.The sequence are accroding to the figures in the manuscript.
# 6. Heterostructures_cif-files
This folder contains the structure files (cif) of MoS₂/WS₂ and MoS₂/PtSe₂ heterostructures.
# Note: 
This set of tools is intended to support reproducibility and facilitate the design and analysis of 2D heterostructures for photocatalytic applications.


"""
ConceptParamFileGenerator.py
============================
This is a python3 script that reads in a csv file containing a table with an arbitrary number
of rows and exactly 8 columns. Each column must refer to a cosmological parameter of the 
EuclidEmulator2 parameter space in the following order:

       Omega_b, Omega_m, sum_m_nu, n_s, h, w_0, w_a, A_s

The script can be called as follows:

        python3 EE2_ConceptParamFileGenerator.py <InputFile.csv>

Upon execution the file will produce as many .param files as there are lines in the InputFile.csv.
Each of the created .param files can be read-in by the CONCEPT code (J. Dakin).
"""

import numpy as np
import sys, os

EDfile = sys.argv[1]

Omega_b, Omega_m, sum_m_nu, n_s, h, w_0, w_a, A_s = np.loadtxt(EDfile, delimiter=",", unpack=True)

# Check ranges
everythingOK = True
if not all(Omega_b >= 0.04) and all(Omega_b <= 0.06):
    everythingOK = False
if not all(Omega_m >= 0.24) and all(Omega_m <= 0.40):
    everythingOK = False
if not all(sum_m_nu >= 0.00) and all(sum_m_nu <= 0.15):
    everythingOK = False
if not all(n_s >= 0.92) and all(n_s <= 1.00):
    everythingOK = False
if not all(h >= 0.61) and all(h <= 0.73):
    everythingOK = False
if not all(w_0 >= -1.3) and all(w_0 <= -0.7):
    everythingOK = False
if not all(w_a >= -1.0) and all(w_a <= 1.0):
    everythingOK = False
if not all(A_s >= 1.7e-9) and all(A_s <= 2.5e-9):
    everythingOK = False

if not everythingOK:
	raise ValueError("An input parameter does not respect the EE2 parameter box boundaries.\n")
	sys.exit(1)

# Convert parameters
Omega_cdm = Omega_m - Omega_b
Hubble = 100*h
nu_mass = sum_m_nu/3.0

# Info
nTrainingEx = len(Omega_b)
print("There are %d training examples in this file." % nTrainingEx)

# Write file
for i in range(nTrainingEx):
    cid = "C"+str(i).zfill(3)
    with open(cid+".concept.params", "w") as fp:
        fp.write("# This is the default parameter file used by the CLASS utility.\n")
        fp.write("# It is set up to yield cosmologies with neutrinos,\n")
        fp.write("# the masses of which is specified in _mν below.\n")
        fp.write("# The number of neutrinos is inferred from the number of\n")
        fp.write("# elements in _mν. Masses of zero are allowed.\n")
        fp.write("# Specifying the same mass for multiple neutrinos result in a\n")
        fp.write("# single degenerate neutrino species.\n")
        fp.write("_w0 = %.9f\n" % w_0[i])
        fp.write("_wa = %.9f\n" % w_a[i])
        fp.write("_mν = [%.9f, %.9f, %.9f]  # Neutrino masses in eV\n" % (nu_mass[i], nu_mass[i], nu_mass[i]))
        fp.write("_precision = 100\n")
        fp.write("\n")
        fp.write("_k_min   = 5e-5*h/Mpc\n")
        fp.write("_k_max   = 17*h/Mpc\n")
        fp.write("_k_modes = 256\n")
        fp.write("\n")
        fp.write("# Input\n")
        fp.write("output_dirs = {'powerspec': paths['output_dir'] + f'/%s/'}\n" % cid)
        fp.write("\n")
        fp.write("# Numerical parameters\n")
        fp.write("boxsize = 2*pi/_k_min\n")
        fp.write("φ_gridsize = int(2/sqrt(3)*_k_max/_k_min + 1)\n")
        fp.write("φ_gridsize += 1 if φ_gridsize%2 else 0\n")
        fp.write("modes_per_decade = _k_modes/log10(_k_max/_k_min)\n")
        fp.write("\n")
        fp.write("# Cosmology\n")
        fp.write("H0      = %.9f*km/(s*Mpc)\n" % Hubble[i])
        fp.write("Ωcdm    = %.9f - Ων\n" % Omega_cdm[i])
        fp.write("Ωb      = %.9f\n" % Omega_b[i])
        fp.write("a_begin = 1/(1 + 250)\n")
        fp.write("class_params = {\n")
        fp.write("      # Photons and neutrino precision parameters\n")
        fp.write("      'radiation_streaming_approximation': 3,\n")
        fp.write("      'ur_fluid_approximation'           : 3,\n")
        fp.write("      'l_max_g'                          : 1001,\n")
        fp.write("      'l_max_pol_g'                      : 1001,\n")
        fp.write("      'l_max_ur'                         : 1001,\n")
        fp.write("      # Add neutrino hierarchy\n")
        fp.write("      'N_ur'    : 0,\n")
        fp.write("      'N_ncdm'  : len(set(_mν)),\n")
        fp.write("      'deg_ncdm': [_mν.count(mν) for mν in sorted(set(_mν))],\n")
        fp.write("      'm_ncdm'  : [mν if mν else 1e-100 for mν in sorted(set(_mν))],\n")
        fp.write("      'T_ncdm'  : [(4/11)**(1/3)*(3.046/len(_mν))**(1/4)]*len(set(_mν)),  # Ensure N_eff = 3.046\n")
        fp.write("      # Neutrino precision parameters\n")
        fp.write("      'ncdm_fluid_approximation': 3,\n")
        fp.write("      'Quadrature strategy'     : [3]*len(set(_mν)),\n")
        fp.write("      'l_max_ncdm'              : 2*_precision+1,\n")
        fp.write("      'Number of momentum bins' : [min([_precision, 50])]*len(set(_mν)),\n")
        fp.write("      'Maximum q'               : [18]*len(set(_mν)),\n")
        fp.write("      # General precision parameters\n")
        fp.write("      'evolver'                     : 0,\n")
        fp.write("      'recfast_Nz0'                 : 1e+5,\n")
        fp.write("      'tol_thermo_integration'      : 1e-6,\n")
        fp.write("      'perturb_integration_stepsize': 0.25,\n")
        fp.write("      'perturb_sampling_stepsize'   : 0.01,\n")
        fp.write("}\n")
        fp.write("\n")
        fp.write("# fld\n")
        fp.write("class_params.update({\n")
        fp.write("      'Omega_Lambda': 0,\n")
        fp.write("      'w0_fld'      : _w0,\n")
        fp.write("      'wa_fld'      : _wa,\n")
        fp.write("})\n")
        fp.write("\n")
        fp.write("# Simulation options\n")
        fp.write("class_k_max = {}\n")
        fp.write("class_reuse = True\n")
        fp.write("class_plot_perturbations = False\n")
        fp.write("class_extra_background = []\n")
        fp.write("class_extra_perturbations = []\n")
        fp.write("\n")
        fp.write("# System of units\n")
        fp.write("unit_length = 'Mpc'\n")
        fp.write("unit_time   = 'Gyr'\n")
        fp.write("unit_mass   = '10¹⁰ m☉'\n")

"""
EE2_PkdgravParFileGenerator.py
==============================
This is a python script that reads in a csv file containing a table with an arbitrary number
of rows and exactly 8 columns. Each column must refer to a cosmological parameter of the 
EuclidEmulator2 parameter space in the following order:

       Omega_b, Omega_m, sum_m_nu, n_s, h, w_0, w_a, A_s

The script can be called as follows:

        python3 EE2_PkdgravParFileGenerator.py <InputFile.csv>

Upon execution the file will produce as many .par file pairs as there are lines in the InputFile.csv.
Each of the created .par files can be read-in by the PKDGRAV code (Potter & Stadel). 
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

nTrainingEx = len(Omega_b)
print("There are %d training examples in this file." % nTrainingEx)

for i in range(nTrainingEx):
    cid = "C"+str(i).zfill(3)
    for PFphase in [0,1]:
        with open(cid+".PF"+str(PFphase)+".par", "w") as fp:
            fp.write("# Memory and performance\n")
            fp.write("# ----------------------\n")
            fp.write("bMemUnordered    = 1      # Order replaced by potential and group id\n")
            fp.write("bNewKDK          = 1      # No accelerations in the particle, dual tree possible\n")
            fp.write("bDualTree        = 1      # Use two trees\n")
            fp.write("bMemPotential    = 0\n")
            fp.write("nBucket          = 24\n")
            fp.write("dExtraStore      = 0.02\n")
            fp.write("\n")
            fp.write("# Simulation Mode\n")
            fp.write("# ---------------\n")
            fp.write("# In the bClass=1 mode the cosmology is entirely read from the\n")
            fp.write("# HDF5 file specified in 'achClassFilename' parameter below.\n")
            fp.write("bClass           = 1\n")
            fp.write("dOmega0          = 0.0    # This is a dummy parameter, just to have the parameter define")
            fp.write("\n")
            fp.write("# Initial Condition\n")
            fp.write("# -----------------\n")
            fp.write("dBoxSize         = 1000   # Mpc/h\n")
            fp.write("nGrid            = 3000   # Simulation has nGrid^3 particles\n")
            fp.write("b2LPT            = 0      # second order IC\n")
            fp.write("iSeed            = 31415  # Random seed ==> Cosmic variance is the same across all cosmologies\n")
            fp.write("dRedFrom         = 99     # Starting redshift\n")
            fp.write("bFixedAmpIC      = 1      # we use P+F to get rid of cosmic variance\n")
            fp.write("dFixedAmpPhasePI = %d\n" % PFphase)
            fp.write("\n")
            fp.write("# Measure P(k)\n")
            fp.write("# ------------\n")
            fp.write("nGridPk          = 3000\n")
            fp.write("iPkInterval      = 1\n")
            fp.write("iDeltakInterval  = 3\n") 
            fp.write("\n")
            fp.write("# Linear theory\n")
            fp.write("# -------------\n")
            fp.write("achClassFilename = \"C"+str(i).zfill(3)+".hdf5\"\n")
            fp.write("nGridLin         = 750\n")
            fp.write("achLinSpecies    = \"g+ncdm[0]+fld+metric\" # these species are considered in the evolution\n")
            fp.write("achPkSpecies     = \"g+ncdm[0]+fld\"        # these species are considered in the power computation\n")
            fp.write("dNormalization   = %.9e\n" % A_s[i])
            fp.write("dSpectral        = %.9e\n" % n_s[i])
            fp.write("\n")
            fp.write("# Simulation parameters\n")
            fp.write("# ---------------------\n")
            fp.write("iStartStep       = 0\n")
            fp.write("nSteps           = 160\n")
            fp.write("nSteps10         = 60\n")
            fp.write("dRedTo           = 0\n")
            fp.write("\n")
            fp.write("# Logging/Output\n")
            fp.write("# --------------\n")
            fp.write("bWriteIC         = 0\n")
            fp.write("iLogInterval     = 1     # Log every major time step\n")
            fp.write("iOutInterval     = 0     # Do not dump snapshots\n")
            fp.write("iCheckInterval   = 40    # Checkpoints\n")
            fp.write("iWallRunTime     = 1320  # = 22 hours\n")
            fp.write("bDoDensity       = 0\n")
            fp.write("bVDetails        = 1\n")
            fp.write("dHubble0         = 2.8944050182330705\n")
            fp.write("bOverwrite       = 1\n")
            fp.write("bParaRead        = 1     # Read in parallel\n")
            fp.write("bParaWrite       = 1     # Write in parallel (does not work on all file systems)\n")
            fp.write("nParaRead        = 28    # setting this to the number of nodes is a reasonable choice\n")
            fp.write("nParaWrite       = 28    # setting this to the number of nodes is a reasonable choice\n")
            fp.write("\n")
            fp.write("# Cosmological Simulation\n")
            fp.write("# -----------------------\n")
            fp.write("bComove          = 1     # Use comoving coordinates\n")
            fp.write("bPeriodic        = 1     # with a periodic box\n")
            fp.write("bEwald           = 1     # enable Ewald periodic boundaries\n")
            fp.write("\n")
            fp.write("# Accuracy Parameters\n")
            fp.write("# -------------------\n")
            fp.write("bEpsAccStep      = 1     # Choose eps/a timestep criteria\n")
            fp.write("dTheta           = 0.40  # accuracy of forces for z > 20\n")
            fp.write("dTheta20         = 0.55\n")
            fp.write("dTheta2          = 0.70\n")
            fp.write("dEta             = 0.20\n")
            fp.write("\n")
            fp.write("# Do fewer domain decompositions\n")
            fp.write("# ------------------------------\n")
            fp.write("dFracNoDomainDimChoice = 0.10\n")
            fp.write("dFracNoDomainRootFind  = 0.10\n")
            fp.write("dFracNoDomainDecomp    = 0.10\n")
            fp.write("dFracDualTree          = 0.05\n")

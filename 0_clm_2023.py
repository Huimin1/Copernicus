"""
export SPACK_ROOT=$(pwd)/spack
source spack/share/spack/setup-env.sh
spack load parflow
"""

# # Set the environment variable for PARFLOW_DIR
import os
os.environ['PARFLOW_DIR'] = '/global-scratch/bulk_pool/huiminw/spack/opt/spack/linux-centos7-skylake_avx512/gcc-12.2.0/parflow-3.9.0-uqrrtk6sf5be3xkhmqamahznsu7lzbtk'

# Source the pf-cmake-env.sh file
os.system('. ' + os.path.join(os.environ['PARFLOW_DIR'], 'config', 'pf-cmake-env.sh'))

# Verify Environment Variables:
# print(os.environ['PARFLOW_DIR'])

# Import the ParFlow package
from parflow import Run
import shutil
import numpy as np
import sys
from multiprocessing import Pool
from parflow.tools.fs import mkdir

# %%
# Set the base directory
# base = os.path.join(os.getcwd(), "forcing_2023days")
base = os.path.join(os.getcwd())
mkdir(base)
# print(f"base: {base}")

def distribute_forcings(t_ini, year_to_simulate, day):
    first_hour = day*24 + 1 + t_ini
    last_hour = (day+1)*24 + t_ini

    Calibration.dist(f'/global-scratch/bulk_pool/huiminw/forcings/PFB/FORCING_lombardy_2023/FORCING_lombardy.DSWR.{first_hour:06d}_to_{last_hour:06d}.pfb', NZ = 24)
    Calibration.dist(f'/global-scratch/bulk_pool/huiminw/forcings/PFB/FORCING_lombardy_2023/FORCING_lombardy.DLWR.{first_hour:06d}_to_{last_hour:06d}.pfb', NZ = 24)
    Calibration.dist(f'/global-scratch/bulk_pool/huiminw/forcings/PFB/FORCING_lombardy_2023/FORCING_lombardy.APCP.{first_hour:06d}_to_{last_hour:06d}.pfb', NZ = 24)
    Calibration.dist(f'/global-scratch/bulk_pool/huiminw/forcings/PFB/FORCING_lombardy_2023/FORCING_lombardy.Temp.{first_hour:06d}_to_{last_hour:06d}.pfb', NZ = 24)
    Calibration.dist(f'/global-scratch/bulk_pool/huiminw/forcings/PFB/FORCING_lombardy_2023/FORCING_lombardy.UGRD.{first_hour:06d}_to_{last_hour:06d}.pfb', NZ = 24)
    Calibration.dist(f'/global-scratch/bulk_pool/huiminw/forcings/PFB/FORCING_lombardy_2023/FORCING_lombardy.VGRD.{first_hour:06d}_to_{last_hour:06d}.pfb', NZ = 24)
    Calibration.dist(f'/global-scratch/bulk_pool/huiminw/forcings/PFB/FORCING_lombardy_2023/FORCING_lombardy.Press.{first_hour:06d}_to_{last_hour:06d}.pfb', NZ = 24)
    Calibration.dist(f'/global-scratch/bulk_pool/huiminw/forcings/PFB/FORCING_lombardy_2023/FORCING_lombardy.SPFH.{first_hour:06d}_to_{last_hour:06d}.pfb', NZ = 24)


# t_ini = int(sys.argv[1])
# t_end = int(sys.argv[2])
# days_to_simulate = int(sys.argv[3])
# year_to_simulate = int(sys.argv[4])
# combination = int(sys.argv[5])
#---------------------------------------------------------
# Define RunName and create run directory
#---------------------------------------------------------
Calibration = Run("Calibration", __file__)
#---------------------------------------------------------
# Processor Topology
#---------------------------------------------------------
Calibration.Process.Topology.P = 6
Calibration.Process.Topology.Q = 3
Calibration.Process.Topology.R = 1

#---------------------------------------------------------
# Computational Grid
#---------------------------------------------------------
Calibration.ComputationalGrid.Lower.X = 0.0
Calibration.ComputationalGrid.Lower.Y = 0.0
Calibration.ComputationalGrid.Lower.Z = 0.0

Calibration.ComputationalGrid.NX = 265
Calibration.ComputationalGrid.NY = 165
Calibration.ComputationalGrid.NZ = 6

Calibration.ComputationalGrid.DX = 2000.0
Calibration.ComputationalGrid.DY = 2000.0
Calibration.ComputationalGrid.DZ = 37.5

#---------------------------------------------------------
# The Names of the GeomInputs
#---------------------------------------------------------
Calibration.GeomInput.Names = 'domaininput'
Calibration.GeomInput.domaininput.GeomNames = 'domain'
Calibration.GeomInput.domaininput.InputType = 'SolidFile'
Calibration.GeomInput.domaininput.FileName = 'My_solid.pfsol'
Calibration.Geom.domain.Patches = 'Bottom Top west east'
Calibration.Domain.GeomName = 'domain'

#---------------------------------------------------------
# Variable Dz
#---------------------------------------------------------
Calibration.Solver.Nonlinear.VariableDz = True
Calibration.dzScale.GeomNames = 'domain'
Calibration.dzScale.Type = 'nzList'
Calibration.dzScale.nzListNumber = 6

Calibration.Cell._0.dzScale.Value = 170.0/37.5
Calibration.Cell._1.dzScale.Value = 40.0/37.5
Calibration.Cell._2.dzScale.Value = 13.0/37.5
Calibration.Cell._3.dzScale.Value = 1.4/37.5
Calibration.Cell._4.dzScale.Value = 0.45/37.5
Calibration.Cell._5.dzScale.Value = 0.15/37.5

#-----------------------------------------------------------------------------
# Assign Material Parameters and slopes
#-----------------------------------------------------------------------------
# Permeability
Calibration.Geom.Perm.Names = 'domain'
Calibration.Geom.domain.Perm.Type = 'PFBFile'
Calibration.Geom.domain.Perm.FileName = 'k_eq.pfb'
Calibration.Perm.TensorType = 'TensorByGeom'
Calibration.Geom.Perm.TensorByGeom.Names = 'domain'
Calibration.Geom.domain.Perm.TensorValX = 100.0
Calibration.Geom.domain.Perm.TensorValY = 100.0
Calibration.Geom.domain.Perm.TensorValZ = 1.0

# Specific Storage
Calibration.SpecificStorage.Type = 'Constant'
Calibration.SpecificStorage.GeomNames = 'domain'
Calibration.Geom.domain.SpecificStorage.Value = 0.00016

# Porosity
Calibration.Geom.Porosity.GeomNames = 'domain'
Calibration.Geom.domain.Porosity.Type = 'PFBFile'
Calibration.Geom.domain.Porosity.FileName = 'porosity_eq.pfb'

# Relative Permeability
Calibration.Phase.RelPerm.Type = 'VanGenuchten'
Calibration.Phase.RelPerm.GeomNames = 'domain'
Calibration.Phase.RelPerm.VanGenuchten.File = 1
Calibration.Geom.domain.RelPerm.Alpha.Filename = 'alpha_eq.pfb'
Calibration.Geom.domain.RelPerm.N.Filename = 'n_eq.pfb'

# Saturation
Calibration.Phase.Saturation.Type = 'VanGenuchten'
Calibration.Phase.Saturation.GeomNames = 'domain'
Calibration.Phase.Saturation.VanGenuchten.File = 1
Calibration.Geom.domain.Saturation.Alpha.Filename = 'alpha_eq.pfb'
Calibration.Geom.domain.Saturation.N.Filename = 'n_eq.pfb'
Calibration.Geom.domain.Saturation.SRes.Filename = 'sres_eq.pfb'
Calibration.Geom.domain.Saturation.SSat.Filename = 'ssat_eq.pfb'

# Topo slopes in x-direction
Calibration.TopoSlopesX.Type = 'PFBFile'
Calibration.TopoSlopesX.GeomNames = 'domain'
Calibration.TopoSlopesX.FileName = 'slope_x.pfb'

# Topo slopes in y-direction
Calibration.TopoSlopesY.Type = 'PFBFile'
Calibration.TopoSlopesY.GeomNames = 'domain'
Calibration.TopoSlopesY.FileName = 'slope_y.pfb'

# Mannings coefficient
Calibration.Mannings.GeomNames = 'domain'
Calibration.Mannings.Type = 'PFBFile'
Calibration.Mannings.FileName = 'mannings.pfb'

#-----------------------------------------------------------------------------
# Timing
#-----------------------------------------------------------------------------
# Timing parameters
Calibration.TimingInfo.BaseUnit = 1.0
# Calibration.TimingInfo.StartCount = t_ini
# Calibration.TimingInfo.StartTime = t_ini
# Calibration.TimingInfo.StopTime = t_end
Calibration.TimingInfo.StartCount = 0
Calibration.TimingInfo.StartTime = 0
Calibration.TimingInfo.StopTime = 120
Calibration.TimingInfo.DumpInterval = 12
Calibration.TimeStep.Type = 'Constant'
Calibration.TimeStep.Value = 1.0

# Time Cycles
Calibration.Cycle.Names = 'constant'
Calibration.Cycle.constant.Names = 'alltime'
Calibration.Cycle.constant.alltime.Length = 10000000
Calibration.Cycle.constant.Repeat = -1

#-----------------------------------------------------------------------------
# Boundary and Initial Conditions
#-----------------------------------------------------------------------------
# Boundary conditions
Calibration.BCPressure.PatchNames = "east Top"
Calibration.Patch.east.BCPressure.Type = 'DirEquilRefPatch'
Calibration.Patch.east.BCPressure.Cycle = 'constant'
Calibration.Patch.east.BCPressure.RefGeom = 'domain'
Calibration.Patch.east.BCPressure.RefPatch = 'Bottom'
Calibration.Patch.east.BCPressure.alltime.Value = 224.9

Calibration.Patch.Top.BCPressure.Type = 'OverlandKinematic'
Calibration.Patch.Top.BCPressure.Cycle = 'constant'
Calibration.Patch.Top.BCPressure.alltime.Value = 0.0

# Initial conditions
Calibration.ICPressure.Type = 'PFBFile'
Calibration.ICPressure.GeomNames = 'domain'
Calibration.Geom.domain.ICPressure.FileName = 'ip_solid.pfb'

#-----------------------------------------------------------------------------
# Solver parameters
#-----------------------------------------------------------------------------
Calibration.Solver = 'Richards'
Calibration.Solver.MaxIter = 1000000
Calibration.Solver.TerrainFollowingGrid = True
Calibration.Solver.Nonlinear.MaxIter = 200
Calibration.Solver.Nonlinear.ResidualTol = 1e-5
Calibration.Solver.Drop = 1E-20
Calibration.Solver.AbsTol = 1E-10
Calibration.Solver.Nonlinear.UseJacobian = True
Calibration.Solver.Nonlinear.StepTol = 1e-20
Calibration.Solver.Nonlinear.Globalization = 'LineSearch'
Calibration.Solver.Linear.KrylovDimension = 15
Calibration.Solver.Linear.MaxRestarts = 10
Calibration.Solver.MaxConvergenceFailures = 8
Calibration.Solver.Linear.Preconditioner = 'PFMG'
Calibration.Solver.PrintSubsurf = True
Calibration.Solver.PrintSaturation = True
Calibration.Solver.PrintSlopes = True
Calibration.Solver.PrintMannings = True
Calibration.Solver.PrintVelocities = False
Calibration.Solver.EvapTransFile = True
Calibration.Solver.EvapTrans.FileName = "PIME_PFB.pfb"

#---------------------------------------------------------
# CLM settings
#---------------------------------------------------------
Calibration.Solver.LSM = 'CLM'
Calibration.Solver.CLM.IstepStart = 1
# Calibration.Solver.CLM.IstepStart = t_ini+1
Calibration.Solver.CLM.MetForcing  = '3D'
Calibration.Solver.CLM.MetFileName = 'FORCING_lombardy'
# Calibration.Solver.CLM.MetFilePath = f'../../../../../../leonardo_scratch/large/userexternal/rsandova/FORCINGS/pars_{combination}/{year_to_simulate}/pfb_format/'
Calibration.Solver.CLM.MetFilePath = f'/global-scratch/bulk_pool/huiminw/forcings/PFB/FORCING_lombardy_2023/'
Calibration.Solver.CLM.MetFileNT = 24

Calibration.Solver.PrintCLM = True
Calibration.Solver.WriteCLMBinary = False
Calibration.Solver.CLM.BinaryOutDir = False
Calibration.Solver.CLM.SingleFile = True
Calibration.Solver.CLM.CLMDumpInterval = 1

Calibration.Solver.CLM.WriteLogs = False
Calibration.Solver.CLM.WriteLastRST = True
Calibration.Solver.CLM.DailyRST = False
Calibration.Solver.CLM.ResSat = 0.01
Calibration.Solver.CLM.RootZoneNZ = 3
Calibration.Solver.CLM.SoiLayer = 3

#---------------------------------------------------------
# Distribute files
#---------------------------------------------------------
Calibration.dist('k_eq.pfb', NZ = 6)
Calibration.dist('porosity_eq.pfb', NZ = 6)
Calibration.dist('alpha_eq.pfb', NZ = 6)
Calibration.dist('n_eq.pfb', NZ = 6)
Calibration.dist('sres_eq.pfb', NZ = 6)
Calibration.dist('ssat_eq.pfb', NZ = 6)
Calibration.dist('slope_x.pfb')
Calibration.dist('slope_y.pfb')
Calibration.dist('mannings.pfb')
Calibration.dist('ip_solid.pfb', NZ = 6)
Calibration.dist('PIME_PFB.pfb', NZ = 6)


num_cores = 18
# days = [day for day in range(days_to_simulate)]
days = [day for day in range(5)]

with Pool(processes=num_cores) as pool:
    # pool.starmap(distribute_forcings, [(t_ini, year_to_simulate, day) for day in days])
    pool.starmap(distribute_forcings, [(0, 2023, day) for day in days])

#-----------------------------------------------------------------------------
# Properties that we never change
#-----------------------------------------------------------------------------

#Phase sources
Calibration.Phase.Names = 'water'
Calibration.Phase.water.Density.Type = 'Constant'
Calibration.Phase.water.Density.Value = 1.0
Calibration.Phase.water.Viscosity.Type = 'Constant'
Calibration.Phase.water.Viscosity.Value = 1.0

# Contaminants
Calibration.Contaminants.Names = ''

# Retardation
Calibration.Geom.Retardation.GeomNames = ''

# Gravity
Calibration.Gravity = 1.0

# Phase sources:
Calibration.PhaseSources.water.Type = 'Constant'
Calibration.PhaseSources.water.GeomNames = 'domain'
Calibration.PhaseSources.water.Geom.domain.Value = 0.0

# Exact solution specification for error calculations
Calibration.KnownSolution = 'NoKnownSolution'

#-----------------------------------------------------------------------------
# Wells
#-----------------------------------------------------------------------------
Calibration.Wells.Names = ''

#-----------------------------------------------------------------------------
# Run
#-----------------------------------------------------------------------------
Calibration.run()
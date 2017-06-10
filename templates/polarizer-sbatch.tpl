#!/bin/bash
#SBATCH --job-name={__NAME__}
#SBATCH --time={__TIME__}
#SBATCH --ntasks=152
#SBATCH -o job-out.log
#SBATCH -e job-err.log

#SBATCH --account={__ACCOUNT__}
#SBATCH --partition={__PARTITION__}
#SBATCH --reservation=7new-McPherson

cd "{__WORKDIR__}"

rm -rf ./meep-out

module load intel/2017.0.098
module load impi/5.1.3
module load meep/1.3
export GUILE_WARN_DEPRECATED="no"

mpirun -np $SLURM_NTASKS meep-mpi meep.ctl > run.log

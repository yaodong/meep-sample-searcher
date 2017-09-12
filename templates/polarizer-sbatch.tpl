#!/bin/bash
#SBATCH --job-name={__NAME__}
#SBATCH --time={__TIME__}
#SBATCH --ntasks=80
#SBATCH -o job-out.log
#SBATCH -e job-err.log

#SBATCH --account={__ACCOUNT__}
#SBATCH --partition={__PARTITION__}
#SBATCH --reservation=xinbo-amo-3

cd "{__WORKDIR__}"

rm -rf ./meep-out

module load gcc/4.8.5
module load mvapich2/2.2.g
module load meep/1.3

mpirun -np $SLURM_NTASKS meep-mpi meep.ctl > run.log

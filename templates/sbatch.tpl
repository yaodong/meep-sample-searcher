#!/bin/bash
#SBATCH --job-name={__NAME__}
#SBATCH --time={__TIME__}
#SBATCH --ntasks=80
#SBATCH -o job-out-{__MAX_MIN__}.log
#SBATCH -e job-err-{__MAX_MIN__}.log

#SBATCH --account={__ACCOUNT__}
#SBATCH --partition={__PARTITION__}
#SBATCH --res=xinbo-amo-5

cd "{__WORKDIR__}"

rm -rf ./meep-{__MAX_MIN__}-out

module load gcc/4.8.5
module load mpich/3.2.g
module load meep/1.3

mpirun -np $SLURM_NTASKS meep-mpi meep-{__MAX_MIN__}.ctl > run-{__MAX_MIN__}.log

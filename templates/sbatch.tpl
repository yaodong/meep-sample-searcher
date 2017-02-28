#!/bin/bash
#SBATCH --job-name={__NAME__}
#SBATCH --time={__TIME__}
#SBATCH --ntasks=152
#SBATCH -o job-out-{__MAX_MIN__}.log
#SBATCH -e job-err-{__MAX_MIN__}.log

#SBATCH --account={__ACCOUNT__}
#SBATCH --partition={__PARTITION__}

cd "{__ROOT_DIR__}/{__SUB_DIR__}"

rm -rf ./meep-{__MAX_MIN__}-out
rm -f has-done-{__MAX_MIN__}.lock

module load intel/2016.0.109
module load impi/5.1.1.109
module load mpb/1.5.impi
module load meep/1.3
export GUILE_WARN_DEPRECATED="no"

echo "__START__"

mpirun -np $SLURM_NTASKS meep-mpi meep-{__MAX_MIN__}.ctl > run-{__MAX_MIN__}.log

touch has-done-{__MAX_MIN__}.lock

echo "__DONE__"

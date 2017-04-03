#!/bin/sh
# script for execution of deployed applications
#
# Sets up the MATLAB Runtime environment for the current $ARCH and executes
# the specified command.
#
cd "$(dirname "$0")"

MCRROOT="/uufs/chpc.utah.edu/sys/installdir/matlab/R2016b"
LD_LIBRARY_PATH=.:${MCRROOT}/runtime/glnxa64 ;
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MCRROOT}/bin/glnxa64 ;
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MCRROOT}/sys/os/glnxa64;
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MCRROOT}/sys/opengl/lib/glnxa64;
export LD_LIBRARY_PATH;

if [ ! -f result.txt ]; then
  if [ -f meep-out/hx-000200.00.h5 ]; then
    cd meep-out
    ~/bin/matlab_{__MATLAB_NAME__} > ../result.txt
    cd ..
  fi
fi

exit

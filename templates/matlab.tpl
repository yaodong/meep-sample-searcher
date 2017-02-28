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

if [ ! -f loss-max.txt ]; then
  if [ -f has-done-max.lock ]; then
    cd meep-max-out
    ~/bin/matlab_{__MATLAB_NAME__} > ../loss-max.txt
    cd ..
  fi
fi

if [ ! -f loss-min.txt ]; then
  if [ -f has-done-min.lock ]; then
    cd meep-min-out
    ~/bin/matlab_{__MATLAB_NAME__} > ../loss-min.txt
    cd ..
  fi
fi

exit

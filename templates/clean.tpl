#!/bin/bash
# script for execution of deployed applications
#
# Sets up the MATLAB Runtime environment for the current $ARCH and executes
# the specified command.
#

cd "$(dirname "$0")"
rm -r meep-max-out
rm -r meep-min-out

rm *.lock

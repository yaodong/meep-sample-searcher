#!/bin/bash

cd "$(dirname "$0")"

module load gcc/4.9.2
module load python/3.5.1

python3 ./facts.py

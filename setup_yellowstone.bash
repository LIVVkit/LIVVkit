#!/bin/bash

# This combination of modules worked as of:
#     December 7 2015
# You may need to adjust these as systems change.

module load python
module load numpy
module load matplotlib/1.3.1
module load netcdf
#module load hdf5
module load netcdf4python
module load nco
module load ncl

module load scipy/0.14.0
module load numexpr
module load bottleneck
module load pyside
module load pandas

module list

#!/bin/bash
# Load modules for big machines

# Make sure usage of this script is appropriate
`module list` >> /dev/null
if [ $? != 0 ]; then
	echo "This machine does not use modules to load packages."
else 
	# Go ahead and load them
	echo -n "Loading modules...."
	module load python
	module load ncl
	module load nco
	module load python_matplotlib
	module load hdf5
	module load netcdf
	module load python_numpy
	module load python_netcdf4
	echo "done!"
fi

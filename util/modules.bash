#!/bin/bash
# Load modules for big machines

# Make sure usage of this script is appropriate
`which module` >> /dev/null
if [ $? != 0 ]; then
	echo "This machine does not use modules to load packages."
else 
	# Go ahead and load them
	echo -n "Loading modules...."
	module load python/2.7.5
	module load ncl/6.1.0
	module load nco/4.3.9
	module load python_matplotlib/1.3.1
	module load hdf5/1.8.11
	module load netcdf/4.1.3
	module load python_numpy/1.8.0
	module load python_netcdf4/1.0.6
	echo "done!"
fi
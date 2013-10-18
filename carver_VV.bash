#!/bin/bash

#KJE, AJB, NRM 8/2013 evanskj@ornl.gov
#This is the master script to set the parameters and paths to run the LIVV kit on lens
#Efforts funded by DOE BER PISCEES SciDAC project
#Currently it is designed specifically for the GLIDE dycore of the CISM model, because it is
#designed to read its output

# load these before running, note that on Carver, laoding python also loads numpy and matplotlib
source $MODULESHOME/init/bash
module load ncl/6.0.0
module load nco/4.0.7
module unload python/2.7
module load python/2.7.3
module load numpy/1.6.1
module load matplotlib/1.1.0
module load netcdf/4.2.0
module load netcdf4-python/1.0.6

#define user for website
export USERNAME=$USER

#user added comment of analysis to be performed
export COMMENT="evaluating code and test suite for CISM2.0 release"

#specify location of executables 
#/reg_test and /livv needs to be placed in the subdirectory below
export TEST_FILEPATH="$GSCRATCH/higher-order"
export SCRIPT_PATH="$TEST_FILEPATH/livv"
export DATA_DIR="data_hopper"

#specify location where the html files will be sent 
export HTML_PATH="/project/projectdirs/piscees/www"
# providing a username creates a directory by that name in the location above in which all the web files will go
export HTML_LINK="portal.nersc.gov/project/~piscees"

# flags to select verification tests
export RUN_DOME30_DIAGNOSTIC=1
export RUN_DOME30_EVOLVING=0
export RUN_CIRCULAR_SHELF=1
export RUN_CONFINED_SHELF=1
export RUN_ISMIP_HOM_A80=1
export RUN_ISMIP_HOM_A20=1
export RUN_ISMIP_HOM_C=0
export RUN_GIS_10KM=0

# flags to run the production analysis - always run the test suite
export GIS_LARGE_TESTS=0
export RUN_DOME500=0
export RUN_GIS_5KM=0

export RUN_ANT=0

if (($RUN_ANT == 1)); then
		#  directory of run
		export ANT_FILEPATH="$TEST_FILEPATH/ant"
		#  cofigure file
		export ANT_CONFIG="ant_5km.config"
		#  production run screen output for collecting convergence information
		export ANT_OUTPUT="out.gnu"
	fi

#TODO once list of plots created, add feature to have user pick which plots to make, default provided

#From here below, the commands are set automatically and don't require changing by the user

#resulting pathnames from settings given by user
export GIS_OUTPUT_FILEPATH="$PERF_FILEPATH/data"

# date stamp of LIVV run to put with comments
NOW=$(date +"%m-%d-%Y-%r")
echo $NOW $COMMENT

# settings not generally altered, but leaving the option open for future extension
#location where the livv code is located
export PY_PATH="$SCRIPT_PATH/bin"
#location where the ncl directory of the ncl scripts and .nc files are located
export NCL_PATH="$SCRIPT_PATH/plots"

#command to run python script while inputting all of the files listed above
#NOTE: not all settings are required to run the python script, type "python VV_main -h" in the command line for a full list of options
#TODO include options if RUN_ANT is turned on, right now only have settings for GIS
if (($GIS_LARGE_TESTS == 1)); then
		python $PY_PATH/VV_main.py -b "$SCRIPT_PATH" -j "$HTML_PATH" -l "$HTML_LINK" -k "$NCL_PATH" -d "$DATA_DIR" -t "$TEST_FILEPATH" -i "$NOW" -m "$COMMENT" -u "$USERNAME" -D "$RUN_DOME30_DIAGNOSTIC" -E "$RUN_DOME30_EVOLVING" -I "$RUN_CIRCULAR_SHELF" -O "$RUN_CONFINED_SHELF" -A "$RUN_ISMIP_HOM_A80" -B "$RUN_ISMIP_HOM_A20" -C "$RUN_ISMIP_HOM_C" -G "$RUN_GIS_10KM" -F "$RUN_DOME500" -H "$RUN_GIS_5KM" #-a "$DATA_PATH"
else

		python $PY_PATH/VV_main.py -b "$SCRIPT_PATH" -j "$HTML_PATH" -l "$HTML_LINK" -k "$NCL_PATH" -d "$DATA_DIR" -t "$TEST_FILEPATH" -i "$NOW" -m "$COMMENT" -u "$USERNAME" -D "$RUN_DOME30_DIAGNOSTIC" -E "$RUN_DOME30_EVOLVING" -I "$RUN_CIRCULAR_SHELF" -O "$RUN_CONFINED_SHELF" -A "$RUN_ISMIP_HOM_A80" -B "$RUN_ISMIP_HOM_A20" -C "$RUN_ISMIP_HOM_C" -G "$RUN_GIS_10KM" -F "$RUN_DOME500" -H "$RUN_GIS_5KM"
fi

#type "python VV_main -h" in the command line for a full list of options

chmod -R 2775 $HTML_PATH/$USER
chgrp -R piscees $HTML_PATH/$USER


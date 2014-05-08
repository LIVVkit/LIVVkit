#!/bin/bash

#KJE, AJB, NRM 02/2014 evanskj@ornl.gov
#This is the master script to set the parameters and paths to run the LIVV kit on rhea at OLCF
#Efforts funded by DOE BER PISCEES SciDAC project
#Currently it is designed specifically for the GLIDE dycore of the CISM model, because it is 
#designed to read its output

# load these before running (they will automatically load)
source $MODULESHOME/init/bash #make sure to put "source $MODULESHOME/init/bash" in your .bashrc file
module load ncl/6.1.0
module load nco/4.3.9
module load python/2.7.5
module load python_numpy/1.8.0
module load python_matplotlib/1.3.1
module load netcdf/4.1.3
module load python_netcdf4/1.0.6

# the below settings highlighted between the ***'s need to be changed by the user:
#*******************************************************************************
# user added comment of analysis to be performed
COMMENT="test run of code"

# /reg_test and /livv needs to be placed in the subdirectory below
export TEST_FILEPATH=$TEST_DIR

# specify location where the html files will be sent so they are viewable on the web
# livv will create the www directory in the HTML_PATH if it does not already exist
export HTML_PATH="/ccs/home/$USER/www/"

# flags to select verification tests, 1=yes
export RUN_DOME30_DIAGNOSTIC=1
export RUN_DOME30_EVOLVING=1
export RUN_CIRCULAR_SHELF=1
export RUN_CONFINED_SHELF=1
export RUN_ISMIP_HOM_A80=1
export RUN_ISMIP_HOM_A20=1
export RUN_ISMIP_HOM_C80=1
export RUN_ISMIP_HOM_C20=1

# flags to select performance analysis
export RUN_DOME60=0
export RUN_DOME120=0
export RUN_DOME240=0
export RUN_DOME500=0
export RUN_DOME1000=0
export RUN_GIS_1KM=0
export RUN_GIS_2KM=0
export RUN_GIS_4KM=0

# flag to select validation analysis
export RUN_VALIDATION=0

# flag to select Antarctica analysis (keep turned off for now)
export RUN_ANT=0
#*******************************************************************************

# From here below, the commands are set automatically and don't require changing by the user

# points to livv in the directory set above
export SCRIPT_PATH="$TEST_FILEPATH/livv"
# data_dir changes based on what machine livv is run on (choices: titan, hopper, mac)
export DATA_DIR="data_titan"
# creates HTML_LINK based on HTML_PATH given above
export HTML_LINK="http://users.nccs.gov/~$USER/"

# providing a username creates a directory by that name in the location above in which all the web files will go
USERNAME=$USER

if (($RUN_ANT == 1)); then
		#  directory of run
		export ANT_FILEPATH="$TEST_FILEPATH/ant"
		#  cofigure file
		export ANT_CONFIG="ant_5km.config"
		#  production run screen output for collecting convergence information
		export ANT_OUTPUT="out.gnu"
	fi

# date stamp of LIVV run to put with comments
NOW=$(date +"%m-%d-%Y-%r")
echo $NOW $COMMENT

# settings not generally altered, but leaving the option open for future extension
# location where the livv code is located
export PY_PATH="$SCRIPT_PATH/bin"
# location where the ncl directory of the ncl scripts and .nc files are located
export NCL_PATH="$SCRIPT_PATH/plots"

# command to run python script while inputting all of the files listed above
# NOTE: not all settings are required to run the python script, type "python VV_main -h" in the command line for a full list of options
# TODO include options if RUN_ANT is turned on, right now only have settings for GIS
		
python $PY_PATH/VV_main.py -j "$HTML_PATH" -l "$HTML_LINK" -k "$NCL_PATH" -d "$DATA_DIR" -t "$TEST_FILEPATH" -i "$NOW" -m "$COMMENT" -u "$USERNAME" -D "$RUN_DOME30_DIAGNOSTIC" -E "$RUN_DOME30_EVOLVING" -I "$RUN_CIRCULAR_SHELF" -O "$RUN_CONFINED_SHELF" -A "$RUN_ISMIP_HOM_A80" -B "$RUN_ISMIP_HOM_A20" -C "$RUN_ISMIP_HOM_C80" -X "$RUN_ISMIP_HOM_C20" -J "$RUN_DOME60" -K "$RUN_DOME120" -L "$RUN_DOME240" -F "$RUN_DOME500" -M "$RUN_DOME1000" -T "$RUN_GIS_1KM" -U "$RUN_GIS_2KM" -W "$RUN_GIS_4KM" -V "$RUN_VALIDATION"

chmod -R 775 $HTML_PATH/*

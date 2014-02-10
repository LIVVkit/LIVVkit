#!/bin/bash

#KJE 1/2013 evanskj@ornl.gov
#This is the master script to set the parameters and paths to run the LIVV kit on mac os computer
#Efforts funded by DOE BER PISCEES SciDAC project
#Currently it is designed specifically for the GLIDE dycore of the CISM model, because it is
#designed to read its output

# load these before running
#source $MODULESHOME/init/bash
#module load ncl/6.0.0
#module load nco/4.0.7
#module load python/2.7
#module load netcdf/4.1.3

nargs=${#}
if ((nargs >= 1)); then
 if (($1 == "from-script")); then
  source ~/.bashrc 
 fi
fi

# the below settings highlighted between the ***'s need to be changed by the user:
#*******************************************************************************
# set path to python version on mac
export MY_PYTHON="/opt/local/bin/python2.7"

# user added comment of analysis to be performed
COMMENT="test run of code"

# change to the location of the directory that holds the livv and reg_test directory
export TEST_FILEPATH="$TEST_DIR"

# specify location where the html files will be sent so they are viewable on the web
# livv will create the www directory in the HTML_PATH if it does not already exist
export HTML_PATH="$TEST_FILEPATH/html/"

# flags to select verification tests, 1=yes
export RUN_DOME30_DIAGNOSTIC=1
export RUN_DOME30_EVOLVING=0
export RUN_CIRCULAR_SHELF=1
export RUN_CONFINED_SHELF=1
export RUN_ISMIP_HOM_A80=1
export RUN_ISMIP_HOM_A20=1
export RUN_ISMIP_HOM_C=0
export RUN_GIS_10KM=0

export RUN_ANT=0
#*******************************************************************************

# From here below, the commands are set automatically and don't require changing by the user

export SCRIPT_PATH="$TEST_FILEPATH/livv"
#data_dir changes based on what machine livv is run on (choices: titan, hopper, mac)
export DATA_DIR="data_mac"
export HTML_LINK="file://$HTML_PATH"

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

# resulting pathnames from settings given by user
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

if [[ ((($nargs == 1) && ($1 == "quick-test")) || (($nargs == 2) && ($2 == "quick-test"))) ]]; then
 rm $HTML_PATH/livv/*
		$MY_PYTHON $PY_PATH/VV_main.py -d "$PY_PATH" -j "$HTML_PATH" -l "$HTML_LINK" -k "$NCL_PATH" -d "$DATA_DIR" -t "$TEST_FILEPATH" -i "$NOW" -m "$COMMENT" -u "$USERNAME" -D "$RUN_DOME30_DIAGNOSTIC" 
fi
chmod 744 $HTML_PATH/*

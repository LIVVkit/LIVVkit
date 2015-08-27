#!/bin/bash

# Script to run lvargo13.ncl

#******************************************************
# Variables to be defined in call to NCL
#******************************************************
# gl_data       -- Greenland base dataset 
#
# model_prefix  -- 
# model_suffix  -- 
# file_start    -- 
# file_end      -- 
#
# out_file -- the output file for the plot
#
#******************************************************


ncl 'gl_data = addfile("/home/fjk/Documents/Code/lvargo13-ncl/data/Greenland_5km_v1.1_SacksRev_c110629.nc", "r") ' \
    'vel_data = addfile("/home/fjk/Documents/Code/lvargo13-ncl/data/greenland_1km_2015_06_03.mcb.nc","r") ' \
    'model_prefix = "/home/fjk/Documents/Code/lvargo13-ncl/data/BG_CISM1_parallel_updating.cism.h." ' \
    'model_suffix = "-01-01-00000.nc" ' \
    'model_start = 208 ' \
    'model_end = 210 ' \
    'plot_file_base = "lvargo13" ' \
    lvargo13.ncl
    
#    'vel_data = addfile("/home/fjk/Documents/Code/lvargo13-ncl/data/Joughin-GIS-InSAR-Vels-2015-1km.nc","r") ' \

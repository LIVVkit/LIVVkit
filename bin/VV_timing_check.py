#!/usr/bin/env

#NOTE: need to module unload python/2.7
#module load python/2.7.3
#module load python_matplotlib
#module load python_numpy

import sys  
import os
import numpy as np
from optparse import OptionParser
import subprocess

def timing(file1,flag):
    try: 
        output = open(file1, 'r') 
    except:
        print "error reading" + file1
        sys.exit(1)
        raise
                                                    
    if flag == 0: 
        for line in output:
            if "simple glide" in line:
                sg_walltotal = float(line.split()[5])
                sg_processes = float(line.split()[2])
                sg_avg = sg_walltotal / sg_processes
        return sg_avg


#definition to collect the averages from 10 timing runs and relay information to livv
def timing_averages(file,flag):
    sg_avg_list = [] 

#collect data from all JFNK timing files
    if flag == 0:
        for i in range(1,10):
            file1 = file + str(i) + "/seacism_timing_stats"
            sg_avg = timing(file1,flag)
            sg_avg_list.append(sg_avg)
            
#calculate averages across all 10 runs for simple glide
        sg_avgs = ['Simple Glide']
        list = sg_avg_list
        sg_sum = 0
        for i in range(0,len(list)):
            sg_sum += list[i]
        sg_sumavg = sg_sum / (len(list))
        sg_avgs.append(sg_sumavg)
        sg_avgs.append(max(list))
        sg_avgs.append(min(list))
        return sg_avgs

def timing_check(file,flag,test):
    if flag == 0:
        #check if 10 timing files exist, otherwise can't run timing
        t_flag = []
        for i in range(1,10):
            file1 = file + str(i)
            if os.path.isdir(file1) == True:
                t_flag.append(0)
            else:
                t_flag.append(1)

        #check for current run timing file
        if os.path.isdir(file) == True:
            t_flag.append(0)
        else:
            t_flag.append(1)
        
        if 1 in t_flag:
            print "Cannot Generate Timing Check for " + test + ": Missing at least one of the 10 timing directories and/or the current run. Go to perf_test directory to run the ijob_timing file and/or ijob scripts."
            sys.exit(0)
        else:
            #call above definitions to get averages of avg, max, and min for each timer across 10 files
            sg_avgs = timing_averages(file,flag)

            #gather timing data from current run
            file1 = file + '/seacism_timing_stats'
            sg_avg = timing(file1,flag)
            sg_avgs.append(sg_avg)

            #calculate range for checking
            list = sg_avgs
            run = list[-1]
            max = list[2]
            min = list[3]
            diff = run - max
            diff2 = min - run
            if diff > 0:
                return 1
            elif diff2 > 0:
                return 2
            else:
                return 0

#!/usr/bin/env

import sys
import os
from optparse import OptionParser
import subprocess
import collections

def jobprocess(file,job_name): # Reading a job output file for production run

    # Initialize lists
    proclist = []
    procttl  = []
    nonlist  = []
    list     = []
    avg      = []
    avg2     = []
    total    = 0.000
    average  = 0.000
    out_flag = 0
    linear_flag = 0

# open output file (from job)
    if file:
        try:
            logfile = open(file, "r")
        except:
            print "error reading " + file
            sys.exit(1)
            raise
        
    for line in logfile:
        
        #calculate total number of processors used
        if ('total procs = ' in line):
            proclist.append(int(line.split()[7]))
            proctotal = sum(proclist)
            procttl.append(proctotal)
        
        #create nonlinear iterations list
        if ('Nonlinear Solver Step' in line):
            current_step = int(line.split()[4])

        #create linear interations list
        if ('"SOLVE_STATUS_CONVERGED"' in line):
            linear_flag = 1
            phrase = '"SOLVE_STATUS_CONVERGED"'
            split = line.split()
            ind = split.index(phrase)
            ind2 = ind + 2
            list.append(int(line.split()[ind2]))
            for value in list:
                total += value
            average = total / len(list)
            avg.append(average)
            for n in avg:
                avg2.append(str(round(n,3)))
            
        #calculate average number of linear iterations if time step converges
        if ('Converged!' in line):
            nonlist.append(current_step)
            if linear_flag == 1:
                for n in avg:
                    avg2.append(str(round(n,3)))
            list    = []
            total   = 0.000
            average = 0.000
            avg     = []

        #calculate average number of linear iterations if there is a time step that fails to converge
        elif ('Failed!' in line):
            nonlist.append(str(current_step) + '***')
            for value in list:
                total += value
            average = total / len(list)
            avg.append(average)
            for n in avg:
                avg2.append(str(round(n,3)))
            list     = []
            total    = 0.000
            average  = 0.000
            avg      = []
            out_flag = 1

    #write nonlinear solver iteration data
    nd_name = '/newton_' + job_name + '.asc'
    ld_name = '/fgmres_' + job_name + '.asc'

    #write linear solver iteration data
    try:
        iter_n = open('data/' + nd_name, 'w')
    except:
        print "error reading newton solver iteration count file"
        sys.exit(1)
        raise
    for line in nonlist:
        snonlist = str(line)
        iter_n.write(snonlist +'\n')
    iter_n.close()

    try:
        iter_l = open('data/' + ld_name, 'w')
    except:
        print "error reading fgmres solver iteration count file"
        sys.exit(1)
        raise
    for line in avg2:
        savg2 = str(line)
        iter_l.write(savg2 +'\n')
    iter_l.close()

    return procttl, nonlist, avg2, out_flag, nd_name, ld_name

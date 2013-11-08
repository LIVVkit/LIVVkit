#!/usr/bin/env

import sys
import os
from optparse import OptionParser
import subprocess
import collections

def jobprocess(file,job_name):

    proclist = []
    procttl  = []
    nonlist  = []
    list     = []
    avg      = []
    avg2     = []
    total    = 0.000
    average  = 0.000
    out_flag = 0

    if file:
        try:
            logfile = open(file, "r")
        except:
            print "error reading " + file
            sys.exit(1)
            raise
        
    for line in logfile:

        if ('total procs = ' in line):
            proclist.append(int(line.split()[7]))
            proctotal = sum(proclist)
            procttl.append(proctotal)

        if ('Nonlinear Solver Step' in line):
            current_step = int(line.split()[4])

        if ('"SOLVE_STATUS_CONVERGED"' in line):
            phrase = '"SOLVE_STATUS_CONVERGED"'
            split = line.split()
            ind = split.index(phrase)
            ind2 = ind + 2
            list.append(int(line.split()[ind2]))

        if ('Converged!' in line):
            nonlist.append(current_step)
            for value in list:
                total += value
            average = total / len(list)
            avg.append(average)
            for n in avg:
                avg2.append(str(round(n,3)))
            list    = []
            total   = 0.000
            average = 0.000
            avg     = []

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


    nd_name = '/newton_' + job_name + '.asc'
    ld_name = '/fgmres_' + job_name + '.asc'

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









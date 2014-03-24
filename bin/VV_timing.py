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
               # sg_max = float(line.split()[6])
               # sg_min = float(line.split()[10])
            if "glissade_initial_diag_var_solve" in line:
                gid_walltotal = float(line.split()[4])
                gid_processes = float(line.split()[1])
                gid_avg = gid_walltotal / gid_processes
                #gid_max = float(line.split()[5])
                #gid_min = float(line.split()[9])
            if "glam_velo_driver" in line:
                gv_walltotal = float(line.split()[4])
                gv_processes = float(line.split()[1])
                gv_avg = gv_walltotal / gv_processes
                #gv_max = float(line.split()[5])
                #gv_min = float(line.split()[9])
        #    if "JFNK_noxsolve" in line:
        #      gi_walltotal = float(line.split()[5])
        #      gi_processes = float(line.split()[2])
        #      gi_avg = gi_walltotal / gi_processes
        #      gi_max = float(line.split()[6])
        #      gi_min = float(line.split()[10])
            if "Calc_F " in line:
                cf_walltotal = float(line.split()[4])
                cf_processes = float(line.split()[1])
                cf_avg = cf_walltotal / cf_processes
                #cf_max = float(line.split()[5])
                #cf_min = float(line.split()[9])
        #if "NOX: Total Linear Solve Time" in line:
        #    ntl_walltotal = float(line.split()[5])
        #    ntl_processes = float(line.split()[2])
        #    ntl_avg = gi_walltotal / gi_processes
        #    ntl_max = float(line.split()[6])
        #    ntl_min = float(line.split()[10])
            if "Belos: Operation Prec*x" in line:
                bop_walltotal = float(line.split()[6])
                bop_processes = float(line.split()[3])
                bop_avg = bop_walltotal / bop_processes
                #bop_max = float(line.split()[7])
                #bop_min = float(line.split()[11])
            if "nox_precond_u" in line:
                npu_walltotal = float(line.split()[4])
                npu_processes = float(line.split()[1])
                npu_avg = npu_walltotal / npu_processes
                #npu_max = float(line.split()[5])
                #npu_min = float(line.split()[9])
            if "nox_precond_v" in line:
                npv_walltotal = float(line.split()[4])
                npv_processes = float(line.split()[1])
                npv_avg = npv_walltotal / npv_processes
                #npv_max = float(line.split()[5])
                #npv_min = float(line.split()[9])
            if "glide_io_writeall" in line:
                gio_walltotal = float(line.split()[4])
                gio_processes = float(line.split()[1])
                gio_avg = gio_walltotal / gio_processes
                #gio_max = float(line.split()[5])
                #gio_min = float(line.split()[9])

        return sg_avg,gid_avg,gv_avg,cf_avg,bop_avg,npu_avg,npv_avg,gio_avg
    
    if flag == 1:
        for line in output:
            if "simple glide" in line:
                sg_walltotal = float(line.split()[5])
                sg_processes = float(line.split()[2])
                sg_avg = sg_walltotal / sg_processes
                #sg_max = float(line.split()[6])
                #sg_min = float(line.split()[10])
            if "glissade_initial_diag_var_solve" in line:
                gid_walltotal = float(line.split()[4])
                gid_processes = float(line.split()[1])
                gid_avg = gid_walltotal / gid_processes
                #gid_max = float(line.split()[5])
                #gid_min = float(line.split()[9])
            if "glam_velo_driver" in line:
                gv_walltotal = float(line.split()[4])
                gv_processes = float(line.split()[1])
                gv_avg = gv_walltotal / gv_processes
                #gv_max = float(line.split()[5])
                #gv_min = float(line.split()[9])
        #    if "JFNK_noxsolve" in line:
        #      gi_walltotal = float(line.split()[5])
        #      gi_processes = float(line.split()[2])
        #      gi_avg = gi_walltotal / gi_processes
        #      gi_max = float(line.split()[6])
        #      gi_min = float(line.split()[10])
        #   if "NOX: Total Linear Solve Time" in line:
        #      ntl_walltotal = float(line.split()[5])
        #      ntl_processes = float(line.split()[2])
        #      ntl_avg = gi_walltotal / gi_processes
        #      ntl_max = float(line.split()[6])
        #      ntl_min = float(line.split()[10])
            if "Belos: Operation Prec*x" in line:
                bop_walltotal = float(line.split()[6])
                bop_processes = float(line.split()[3])
                bop_avg = bop_walltotal / bop_processes
                #bop_max = float(line.split()[7])
                #bop_min = float(line.split()[11])
            if "glide_io_writeall" in line:
                gio_walltotal = float(line.split()[4])
                gio_processes = float(line.split()[1])
                gio_avg = gio_walltotal / gio_processes
                #gio_max = float(line.split()[5])
                #gio_min = float(line.split()[9])
    
        return sg_avg,gid_avg,gv_avg,bop_avg,gio_avg

# definition to collect the averages from 10 timing runs and relay information to livv
def timing_averages(file,flag):

    sg_avg_list = []
    #sg_max_list = []
    #sg_min_list = []
    gid_avg_list = []
    #gid_max_list = []
    #gid_min_list = []
    gv_avg_list = []
    #gv_max_list = []
    #gv_min_list = []
    cf_avg_list = []
    #cf_max_list = []
    #cf_min_list = []
    bop_avg_list = []
    #bop_max_list = []
    #bop_min_list = []
    npu_avg_list = []
    #npu_max_list = []
    #npu_min_list = []
    npv_avg_list = []
    #npv_max_list = []
    #npv_min_list = []
    gio_avg_list = []
    #gio_max_list = []
    #gio_min_list = []

#collect data from all JFNK timing files
    if flag == 0:
        for i in range(1,10):
            file1 = file + str(i) + "/seacism_timing_stats"
            sg_avg,gid_avg,gv_avg,cf_avg,bop_avg,npu_avg,npv_avg,gio_avg = timing(file1,flag)
            sg_avg_list.append(sg_avg)
            #sg_max_list.append(sg_max)
            #sg_min_list.append(sg_min)
            gid_avg_list.append(gid_avg)
            #gid_max_list.append(gid_max)
            #gid_min_list.append(gid_min)
            gv_avg_list.append(gv_avg)
            #gv_max_list.append(gv_max)
            #gv_min_list.append(gv_min)
            cf_avg_list.append(cf_avg)
            #cf_max_list.append(cf_max)
            #cf_min_list.append(cf_min)
            bop_avg_list.append(bop_avg)
            #bop_max_list.append(bop_max)
            #bop_min_list.append(bop_min)
            npu_avg_list.append(npu_avg)
            #npu_max_list.append(npu_max)
            #npu_min_list.append(npu_min)
            npv_avg_list.append(npv_avg)
            #npv_max_list.append(npv_max)
            #npv_min_list.append(npv_min)
            gio_avg_list.append(gio_avg)
            #gio_max_list.append(gio_max)
            #gio_min_list.append(gio_min)

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
        
        #list = sg_max_list
        #sg_sum = 0
        #for i in range(0,len(list)):
        #    sg_sum += list[i]
        #sg_summax = sg_sum / (len(list))
        #sg_avgs.append(sg_summax)
        #list = sg_min_list
        #sg_sum = 0
        #for i in range(0,len(list)):
        #    sg_sum += list[i]
        #sg_summin = sg_sum / (len(list))
        #sg_avgs.append(sg_summin)

        #calculate averages across all 10 runs for glissade initial diag var solver
        gid_avgs = ['Glissade Initial Diag Var Solver']
        list = gid_avg_list
        gid_sum = 0
        for i in range(0,len(list)):
            gid_sum += list[i]
        gid_sumavg = gid_sum / (len(list))
        gid_avgs.append(gid_sumavg)
        gid_avgs.append(max(list))
        gid_avgs.append(min(list))        
        
        #list = gid_max_list
        #gid_sum = 0
        #for i in range(0,len(list)):
        #    gid_sum += list[i]
        #gid_summax = gid_sum / (len(list))
        #gid_avgs.append(gid_summax)
        #list = gid_min_list
        #gid_sum = 0
        #for i in range(0,len(list)):
        #    gid_sum += list[i]
        #gid_summin = gid_sum / (len(list))

        #calculate averages across all 10 runs for glam velo driver
        gv_avgs = ['Glam Velo Driver']
        list = gv_avg_list
        gv_sum = 0
        for i in range(0,len(list)):
            gv_sum += list[i]
        gv_sumavg = gv_sum / (len(list))
        gv_avgs.append(gv_sumavg)
        gv_avgs.append(max(list))
        gv_avgs.append(min(list))        
        
        #list = gv_max_list
        #gv_sum = 0
        #for i in range(0,len(list)):
        #    gv_sum += list[i]
        #gv_summax = gv_sum / (len(list))
        #gv_avgs.append(gv_summax)
        #list = gv_min_list
        #gv_sum = 0
        #for i in range(0,len(list)):
        #    gv_sum += list[i]
        #gv_summin = gv_sum / (len(list))

        #calculate averages across all 10 runs for calc f
        cf_avgs = ['Calc F']
        list = cf_avg_list
        cf_sum = 0
        for i in range(0,len(list)):
            cf_sum += list[i]
        cf_sumavg = cf_sum / (len(list))
        cf_avgs.append(cf_sumavg)
        cf_avgs.append(max(list))
        cf_avgs.append(min(list))        
        
        #list = cf_max_list
        #cf_sum = 0
        #for i in range(0,len(list)):
        #    cf_sum += list[i]
        #cf_summax = cf_sum / (len(list))
        #cf_avgs.append(cf_summax)
        #list = cf_min_list
        #cf_sum = 0
        #for i in range(0,len(list)):
        #    cf_sum += list[i]
        #cf_summin = cf_sum / (len(list))

        #calculate averages across all 10 runs for belos operation op*x
        bop_avgs = ['Belos: Operation Prec*x']
        list = bop_avg_list
        bop_sum = 0
        for i in range(0,len(list)):
            bop_sum += list[i]
        bop_sumavg = bop_sum / (len(list))
        bop_avgs.append(bop_sumavg)
        bop_avgs.append(max(list))
        bop_avgs.append(min(list))        
        
        #list = bop_max_list
        #bop_sum = 0
        #for i in range(0,len(list)):
        #    bop_sum += list[i]
        #bop_summax = bop_sum / (len(list))
        #bop_avgs.append(bop_summax)
        #list = bop_min_list
        #bop_sum = 0
        #for i in range(0,len(list)):
        #    bop_sum += list[i]
        #bop_summin = bop_sum / (len(list))

        #calculate averages across all 10 runs for nox precond u
        npu_avgs = ['Nox Preconditioner U']
        list = npu_avg_list
        npu_sum = 0
        for i in range(0,len(list)):
            npu_sum += list[i]
        npu_sumavg = npu_sum / (len(list))
        npu_avgs.append(npu_sumavg)
        npu_avgs.append(max(list))
        npu_avgs.append(min(list))        
        
        #list = npu_max_list
        #npu_sum = 0
        #for i in range(0,len(list)):
        #    npu_sum += list[i]
        #npu_summax = npu_sum / (len(list))
        #npu_avgs.append(npu_summax)
        #list = npu_min_list
        #npu_sum = 0
        #for i in range(0,len(list)):
        #    npu_sum += list[i]
        #npu_summin = npu_sum / (len(list))

        #calculate averages across all 10 runs for nox precond v
        npv_avgs = ['Nox Preconditioner V']
        list = npv_avg_list
        npv_sum = 0
        for i in range(0,len(list)):
            npv_sum += list[i]
        npv_sumavg = npv_sum / (len(list))
        npv_avgs.append(npv_sumavg)
        npv_avgs.append(max(list))
        npv_avgs.append(min(list))        
        
        #list = npv_max_list
        #npv_sum = 0
        #for i in range(0,len(list)):
        #    npv_sum += list[i]
        #npv_summax = npv_sum / (len(list))
        #npv_avgs.append(npv_summax)
        #list = npv_min_list
        #npv_sum = 0
        #for i in range(0,len(list)):
        #    npv_sum += list[i]
        #npv_summin = npv_sum / (len(list))

        #calculate averages across all 10 runs for glide io writeall
        gio_avgs = ['Glide IO Writeall']
        list = gio_avg_list
        gio_sum = 0
        for i in range(0,len(list)):
            gio_sum += list[i]
        gio_sumavg = gio_sum / (len(list))
        gio_avgs.append(gio_sumavg)
        gio_avgs.append(max(list))
        gio_avgs.append(min(list))        
        
        #list = gio_max_list
        #gio_sum = 0
        #for i in range(0,len(list)):
        #    gio_sum += list[i]
        #gio_summax = gio_sum / (len(list))
        #gio_avgs.append(gio_summax)
        #list = gio_min_list
        #gio_sum = 0
        #for i in range(0,len(list)):
        #    gio_sum += list[i]
        #gio_summin = gio_sum / (len(list))

        return sg_avgs,gid_avgs,gv_avgs,cf_avgs,bop_avgs,npu_avgs,npv_avgs,gio_avgs

#collect data from all PIC timing files
    if flag == 1:
        for i in range(1,11):
            file1 = file + str(i) + "/seacism_timing_stats"
            sg_avg,gid_avg,gv_avg,bop_avg,gio_avg = timing(file1,flag)
            sg_avg_list.append(sg_avg)
            #sg_max_list.append(sg_max)
            #sg_min_list.append(sg_min)
            gid_avg_list.append(gid_avg)
            #gid_max_list.append(gid_max)
            #gid_min_list.append(gid_min)
            gv_avg_list.append(gv_avg)
            #gv_max_list.append(gv_max)
            #gv_min_list.append(gv_min)
            bop_avg_list.append(bop_avg)
            #bop_max_list.append(bop_max)
            #bop_min_list.append(bop_min)
            gio_avg_list.append(gio_avg)
            #gio_max_list.append(gio_max)
            #gio_min_list.append(gio_min)

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
        
        #list = sg_max_list
        #sg_sum = 0
        #for i in range(0,len(list)):
        #    sg_sum += list[i]
        #sg_summax = sg_sum / (len(list))
        #sg_avgs.append(sg_summax)
        #list = sg_min_list
        #sg_sum = 0
        #for i in range(0,len(list)):
        #    sg_sum += list[i]
        #sg_summin = sg_sum / (len(list))
        #sg_avgs.append(sg_summin)

        #calculate averages across all 10 runs for glissade initial diag var solver
        gid_avgs = ['Glissade Initial Diag Var Solver']
        list = gid_avg_list
        gid_sum = 0
        for i in range(0,len(list)):
            gid_sum += list[i]
        gid_sumavg = gid_sum / (len(list))
        gid_avgs.append(gid_sumavg)
        gid_avgs.append(max(list))
        gid_avgs.append(min(list))        
        
        #list = gid_max_list
        #gid_sum = 0
        #for i in range(0,len(list)):
        #    gid_sum += list[i]
        #gid_summax = gid_sum / (len(list))
        #gid_avgs.append(gid_summax)
        #list = gid_min_list
        #gid_sum = 0
        #for i in range(0,len(list)):
        #    gid_sum += list[i]
        #gid_summin = gid_sum / (len(list))

        #calculate averages across all 10 runs for glam velo driver
        gv_avgs = ['Glam Velo Driver']
        list = gv_avg_list
        gv_sum = 0
        for i in range(0,len(list)):
            gv_sum += list[i]
        gv_sumavg = gv_sum / (len(list))
        gv_avgs.append(gv_sumavg)
        gv_avgs.append(max(list))
        gv_avgs.append(min(list))        
        
        #list = gv_max_list
        #gv_sum = 0
        #for i in range(0,len(list)):
        #    gv_sum += list[i]
        #gv_summax = gv_sum / (len(list))
        #gv_avgs.append(gv_summax)
        #list = gv_min_list
        #gv_sum = 0
        #for i in range(0,len(list)):
        #    gv_sum += list[i]
        #gv_summin = gv_sum / (len(list))

        #calculate averages across all 10 runs for belos operation op*x
        bop_avgs = ['Belos: Operation Prec*x']
        list = bop_avg_list
        bop_sum = 0
        for i in range(0,len(list)):
            bop_sum += list[i]
        bop_sumavg = bop_sum / (len(list))
        bop_avgs.append(bop_sumavg)
        bop_avgs.append(max(list))
        bop_avgs.append(min(list))        
        
        #list = bop_max_list
        #bop_sum = 0
        #for i in range(0,len(list)):
        #    bop_sum += list[i]
        #bop_summax = bop_sum / (len(list))
        #bop_avgs.append(bop_summax)
        #list = bop_min_list
        #bop_sum = 0
        #for i in range(0,len(list)):
        #    bop_sum += list[i]
        #bop_summin = bop_sum / (len(list))

        #calculate averages across all 10 runs for glide io writeall
        gio_avgs = ['Glide IO Writeall']
        list = gio_avg_list
        gio_sum = 0
        for i in range(0,len(list)):
            gio_sum += list[i]
        gio_sumavg = gio_sum / (len(list))
        gio_avgs.append(gio_sumavg)
        gio_avgs.append(max(list))
        gio_avgs.append(min(list))        
        
        #list = gio_max_list
        #gio_sum = 0
        #for i in range(0,len(list)):
        #    gio_sum += list[i]
        #gio_summax = gio_sum / (len(list))
        #gio_avgs.append(gio_summax)
        #list = gio_min_list
        #gio_sum = 0
        #for i in range(0,len(list)):
        #    gio_sum += list[i]
        #gio_summin = gio_sum / (len(list))

    return sg_avgs,gid_avgs,gv_avgs,bop_avgs,gio_avgs

def timing_table_current_run(timing_file,file,flag):

    timing_file.write('<HTML>\n')
    timing_file.write('<BODY BGCOLOR="#CADFE0">\n') 
    timing_file.write('<BODY>\n')
    
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
            timing_file.write('<H4>Cannot Generate Timing Table: Missing at least one of the 10 timing directories and/or the current run. Go to perf_test directory to run ijob_timing_JFNK and/or ijob scripts.</H4>')
            sys.exit(0)
        else:
            #call above definitions to get averages of avg, max, and min for each timer across 10 files
            sg_avgs,gid_avgs,gv_avgs,cf_avgs,bop_avgs,npu_avgs,npv_avgs,gio_avgs = timing_averages(file,flag)
        
            #gather timing data from current run
            file1 = file + '/seacism_timing_stats'
            sg_avg,gid_avg,gv_avg,cf_avg,bop_avg,npu_avg,npv_avg,gio_avg = timing(file1,flag)
            sg_avgs.append(sg_avg)
            gid_avgs.append(gid_avg)
            gv_avgs.append(gv_avg)
            cf_avgs.append(cf_avg)
            bop_avgs.append(bop_avg)
            npu_avgs.append(npu_avg)
            npv_avgs.append(npv_avg)
            gio_avgs.append(gio_avg)
    
            columns = ['  ', 'Avg', 'Max', 'Min', 'Current Run']

            timing_file.write('<TABLE>\n')
            timing_file.write('<TR>')
            timing_file.write('<TABLE BORDER="1" CELLPADDING="6">\n')
            timing_file.write('<TH COLSPAN = "11">\n')
            timing_file.write('<H3><BR>JFNK: Timing Data</H3>\n')
            timing_file.write('</TH>')
            timing_file.write('</TR>')
            for title in columns:
                timing_file.write('<TH>' + str(title) + '</TH>')
    
            #display data for simple glide
            list = sg_avgs
            timing_file.write('<TR ALIGN="CENTER">\n')
            timing_file.write('<TR><TH>' + str(list[0]) + '</TH>')
            timing_file.write('<TD>' + str(list[1]) + '</TD>')
            timing_file.write('<TD>' + str(list[2]) + '</TD>')
            timing_file.write('<TD>' + str(list[3]) + '</TD>')
            run = list[-1]
            max = list[2]
            min = list[3]
            diff = run - max
            diff2 = min - run
            if diff > 0:
                timing_file.write('<TD><font color="red">' + str(list[-1]) + '</font></TD>')
            elif diff2 > 0:
                timing_file.write('<TD><font color="blue">' + str(list[-1]) + '</font></TD>')
            else:
                timing_file.write('<TD>' + str(list[-1]) + '</TD>')
            timing_file.write('</TR>\n')

            #display data for glissade initial diag var solve
            list = gid_avgs
            timing_file.write('<TR ALIGN="CENTER">\n')
            timing_file.write('<TR><TH>' + str(list[0]) + '</TH>')
            timing_file.write('<TD>' + str(list[1]) + '</TD>')
            timing_file.write('<TD>' + str(list[2]) + '</TD>')
            timing_file.write('<TD>' + str(list[3]) + '</TD>')
            run = list[-1]
            max = list[2]
            min = list[3]
            diff = run - max
            diff2 = min - run
            if diff > 0:
                timing_file.write('<TD><font color="red">' + str(list[-1]) + '</font></TD>')
            elif diff2 > 0:
                timing_file.write('<TD><font color="blue">' + str(list[-1]) + '</font></TD>')
            else:
                timing_file.write('<TD>' + str(list[-1]) + '</TD>')
            timing_file.write('</TR>\n')

            #display data for glam velo driver
            list = gv_avgs
            timing_file.write('<TR ALIGN="CENTER">\n')
            timing_file.write('<TR><TH>' + str(list[0]) + '</TH>')
            timing_file.write('<TD>' + str(list[1]) + '</TD>')
            timing_file.write('<TD>' + str(list[2]) + '</TD>')
            timing_file.write('<TD>' + str(list[3]) + '</TD>')
            run = list[-1]
            max = list[2]
            min = list[3]
            diff = run - max
            diff2 = min - run
            if diff > 0:
                timing_file.write('<TD><font color="red">' + str(list[-1]) + '</font></TD>')
            elif diff2 > 0:
                timing_file.write('<TD><font color="blue">' + str(list[-1]) + '</font></TD>')
            else:
                timing_file.write('<TD>' + str(list[-1]) + '</TD>')
            timing_file.write('</TR>\n')
        
            #display data for calc f
            list = cf_avgs
            timing_file.write('<TR ALIGN="CENTER">\n')
            timing_file.write('<TR><TH>' + str(list[0]) + '</TH>')
            timing_file.write('<TD>' + str(list[1]) + '</TD>')
            timing_file.write('<TD>' + str(list[2]) + '</TD>')
            timing_file.write('<TD>' + str(list[3]) + '</TD>')
            run = list[-1]
            max = list[2]
            min = list[3]
            diff = run - max
            diff2 = min - run
            if diff > 0:
                timing_file.write('<TD><font color="red">' + str(list[-1]) + '</font></TD>')
            elif diff2 > 0:
                timing_file.write('<TD><font color="blue">' + str(list[-1]) + '</font></TD>')
            else:
                timing_file.write('<TD>' + str(list[-1]) + '</TD>')
            timing_file.write('</TR>\n')

            #display data for belos: operation prec*x
            list = bop_avgs
            timing_file.write('<TR ALIGN="CENTER">\n')
            timing_file.write('<TR><TH>' + str(list[0]) + '</TH>')
            timing_file.write('<TD>' + str(list[1]) + '</TD>')
            timing_file.write('<TD>' + str(list[2]) + '</TD>')
            timing_file.write('<TD>' + str(list[3]) + '</TD>')
            run = list[-1]
            max = list[2]
            min = list[3]
            diff = run - max
            diff2 = min - run
            if diff > 0:
                timing_file.write('<TD><font color="red">' + str(list[-1]) + '</font></TD>')
            elif diff2 > 0:
                timing_file.write('<TD><font color="blue">' + str(list[-1]) + '</font></TD>')
            else:
                timing_file.write('<TD>' + str(list[-1]) + '</TD>')
            timing_file.write('</TR>\n')

            #display data for nox precond u
            list = npu_avgs
            timing_file.write('<TR ALIGN="CENTER">\n')
            timing_file.write('<TR><TH>' + str(list[0]) + '</TH>')
            timing_file.write('<TD>' + str(list[1]) + '</TD>')
            timing_file.write('<TD>' + str(list[2]) + '</TD>')
            timing_file.write('<TD>' + str(list[3]) + '</TD>')
            run = list[-1]
            max = list[2]
            min = list[3]
            diff = run - max
            diff2 = min - run
            if diff > 0:
                timing_file.write('<TD><font color="red">' + str(list[-1]) + '</font></TD>')
            elif diff2 > 0:
                timing_file.write('<TD><font color="blue">' + str(list[-1]) + '</font></TD>')
            else:
                timing_file.write('<TD>' + str(list[-1]) + '</TD>')
            timing_file.write('</TR>\n')

            #display data for nox precond v
            list = npv_avgs
            timing_file.write('<TR ALIGN="CENTER">\n')
            timing_file.write('<TR><TH>' + str(list[0]) + '</TH>')
            timing_file.write('<TD>' + str(list[1]) + '</TD>')
            timing_file.write('<TD>' + str(list[2]) + '</TD>')
            timing_file.write('<TD>' + str(list[3]) + '</TD>')
            run = list[-1]
            max = list[2]
            min = list[3]
            diff = run - max
            diff2 = min - run
            if diff > 0:
                timing_file.write('<TD><font color="red">' + str(list[-1]) + '</font></TD>')
            elif diff2 > 0:
                timing_file.write('<TD><font color="blue">' + str(list[-1]) + '</font></TD>')
            else:
                timing_file.write('<TD>' + str(list[-1]) + '</TD>')
            timing_file.write('</TR>\n')

            #display data for glide io writeall
            list = gio_avgs
            timing_file.write('<TR ALIGN="CENTER">\n')
            timing_file.write('<TR><TH>' + str(list[0]) + '</TH>')
            timing_file.write('<TD>' + str(list[1]) + '</TD>')
            timing_file.write('<TD>' + str(list[2]) + '</TD>')
            timing_file.write('<TD>' + str(list[3]) + '</TD>')
            run = list[-1]
            max = list[2]
            min = list[3]
            diff = run - max
            diff2 = min - run
            if diff > 0:
                timing_file.write('<TD><font color="red">' + str(list[-1]) + '</font></TD>')
            elif diff2 > 0:
                timing_file.write('<TD><font color="blue">' + str(list[-1]) + '</font></TD>')
            else:
                timing_file.write('<TD>' + str(list[-1]) + '</TD>')
            timing_file.write('</TR>\n')

            timing_file.write('</TABLE>\n')
            timing_file.write('<H4><font color="blue">Less than the Min</font></H4>')
            timing_file.write('<H4><font color="red">Greater than the Max</font></H4>')
        
            timing_file.write('<BR>\n')
            timing_file.write('<BR>\n')
            timing_file.write('<BR>\n')

#collect data from all PIC timing files
    if flag == 1:
        
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
            timing_file.write('<H4>Cannot Generate Timing Table: Missing at least one of the 10 timing directories and/or the current run. Go to perf_test directory to run ijob_timing_PIC and/or ijob scripts.</H4>')
        else:
        
            #call above definitions to get averages of avg, max, and min for each timer across 10 files
            sg_avgs,gid_avgs,gv_avgs,bop_avgs,gio_avgs = timing_averages(file,flag)
        
            #gather timing data from current run
            file1 = file + '/seacism_timing_stats'
            sg_avg,gid_avg,gv_avg,bop_avg,gio_avg = timing(file1,flag)
            sg_avgs.append(sg_avg)
            gid_avgs.append(gid_avg)
            gv_avgs.append(gv_avg)
            bop_avgs.append(bop_avg)
            gio_avgs.append(gio_avg)
    
            columns = ['  ', 'Avg', 'Max', 'Min', 'Current Run']

            timing_file.write('<TABLE>\n')
            timing_file.write('<TR>')
            timing_file.write('<TABLE BORDER="1" CELLPADDING="6">\n')
            timing_file.write('<TH COLSPAN = "11">\n')
            timing_file.write('<H3><BR>PIC: Timing Data</H3>\n')
            timing_file.write('</TH>')
            timing_file.write('</TR>')
            for title in columns:
                timing_file.write('<TH>' + str(title) + '</TH>')
    
            #display data for simple glide
            list = sg_avgs
            timing_file.write('<TR ALIGN="CENTER">\n')
            timing_file.write('<TR><TH>' + str(list[0]) + '</TH>')
            timing_file.write('<TD>' + str(list[1]) + '</TD>')
            timing_file.write('<TD>' + str(list[2]) + '</TD>')
            timing_file.write('<TD>' + str(list[3]) + '</TD>')
            run = list[-1]
            max = list[2]
            min = list[3]
            diff = run - max
            diff2 = min - run
            if diff > 0:
                timing_file.write('<TD><font color="red">' + str(list[-1]) + '</font></TD>')
            elif diff2 > 0:
                timing_file.write('<TD><font color="blue">' + str(list[-1]) + '</font></TD>')
            else:
                timing_file.write('<TD>' + str(list[-1]) + '</TD>')
            timing_file.write('</TR>\n')

            #display data for glissade initial diag var solve
            list = gid_avgs
            timing_file.write('<TR ALIGN="CENTER">\n')
            timing_file.write('<TR><TH>' + str(list[0]) + '</TH>')
            timing_file.write('<TD>' + str(list[1]) + '</TD>')
            timing_file.write('<TD>' + str(list[2]) + '</TD>')
            timing_file.write('<TD>' + str(list[3]) + '</TD>')
            run = list[-1]
            max = list[2]
            min = list[3]
            diff = run - max
            diff2 = min - run
            if diff > 0:
                timing_file.write('<TD><font color="red">' + str(list[-1]) + '</font></TD>')
            elif diff2 > 0:
                timing_file.write('<TD><font color="blue">' + str(list[-1]) + '</font></TD>')
            else:
                timing_file.write('<TD>' + str(list[-1]) + '</TD>')
            timing_file.write('</TR>\n')

            #display data for glam velo driver
            list = gv_avgs
            timing_file.write('<TR ALIGN="CENTER">\n')
            timing_file.write('<TR><TH>' + str(list[0]) + '</TH>')
            timing_file.write('<TD>' + str(list[1]) + '</TD>')
            timing_file.write('<TD>' + str(list[2]) + '</TD>')
            timing_file.write('<TD>' + str(list[3]) + '</TD>')
            run = list[-1]
            max = list[2]
            min = list[3]
            diff = run - max
            diff2 = min - run
            if diff > 0:
                timing_file.write('<TD><font color="red">' + str(list[-1]) + '</font></TD>')
            elif diff2 > 0:
                timing_file.write('<TD><font color="blue">' + str(list[-1]) + '</font></TD>')
            else:
                timing_file.write('<TD>' + str(list[-1]) + '</TD>')
            timing_file.write('</TR>\n')

            #display data for belos: operation prec*x
            list = bop_avgs
            timing_file.write('<TR ALIGN="CENTER">\n')
            timing_file.write('<TR><TH>' + str(list[0]) + '</TH>')
            timing_file.write('<TD>' + str(list[1]) + '</TD>')
            timing_file.write('<TD>' + str(list[2]) + '</TD>')
            timing_file.write('<TD>' + str(list[3]) + '</TD>')
            run = list[-1]
            max = list[2]
            min = list[3]
            diff = run - max
            diff2 = min - run
            if diff > 0:
                timing_file.write('<TD><font color="red">' + str(list[-1]) + '</font></TD>')
            elif diff2 > 0:
                timing_file.write('<TD><font color="blue">' + str(list[-1]) + '</font></TD>')
            else:
                timing_file.write('<TD>' + str(list[-1]) + '</TD>')
            timing_file.write('</TR>\n')

            #display data for glide io writeall
            list = gio_avgs
            timing_file.write('<TR ALIGN="CENTER">\n')
            timing_file.write('<TR><TH>' + str(list[0]) + '</TH>')
            timing_file.write('<TD>' + str(list[1]) + '</TD>')
            timing_file.write('<TD>' + str(list[2]) + '</TD>')
            timing_file.write('<TD>' + str(list[3]) + '</TD>')
            run = list[-1]
            max = list[2]
            min = list[3]
            diff = run - max
            diff2 = min - run
            if diff > 0:
                timing_file.write('<TD><font color="red">' + str(list[-1]) + '</font></TD>')
            elif diff2 > 0:
                timing_file.write('<TD><font color="blue">' + str(list[-1]) + '</font></TD>')
            else:
                timing_file.write('<TD>' + str(list[-1]) + '</TD>')
            timing_file.write('</TR>\n')
            
            timing_file.write('</TABLE>\n')
            timing_file.write('<H4><font color="blue">Less than the Min</font></H4>')
            timing_file.write('<H4><font color="red">Greater than the Max</font></H4>')
        
        timing_file.write('</BODY>\n')
        timing_file.write('</HTML>\n')

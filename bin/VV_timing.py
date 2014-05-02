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
            if "initial_diag_var_solve" in line:
                gid_walltotal = float(line.split()[4])
                gid_processes = float(line.split()[1])
                gid_avg = gid_walltotal / gid_processes
            if "_velo_driver" in line:
                whichdriver = line.split("_")[0]
                gv_walltotal = float(line.split()[4])
                gv_processes = float(line.split()[1])
                gv_avg = gv_walltotal / gv_processes
            if "glide_io_writeall" in line:
                gio_walltotal = float(line.split()[4])
                gio_processes = float(line.split()[1])
                gio_avg = gio_walltotal / gio_processes

        return sg_avg,gid_avg,gv_avg,gio_avg,whichdriver
    
# definition to collect the averages from 10 timing runs and relay information to livv
def timing_averages(file,flag):

    sg_avg_list = []
    gid_avg_list = []
    gv_avg_list = []
    gio_avg_list = []
    wd_list = []

#collect data from all JFNK timing files
    if flag == 0:
        for i in range(1,10):
            file1 = file + str(i) + "/seacism_timing_stats"
            sg_avg,gid_avg,gv_avg,gio_avg,whichdriver = timing(file1,flag)
            sg_avg_list.append(sg_avg)
            gid_avg_list.append(gid_avg)
            gv_avg_list.append(gv_avg)
            gio_avg_list.append(gio_avg)
            wd_list.append(whichdriver)

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

        #calculate averages across all 10 runs for initial diag var solver
        gid_avgs = ['Initial Diag Var Solver']
        list = gid_avg_list
        gid_sum = 0
        for i in range(0,len(list)):
            gid_sum += list[i]
        gid_sumavg = gid_sum / (len(list))
        gid_avgs.append(gid_sumavg)
        gid_avgs.append(max(list))
        gid_avgs.append(min(list))        

        #calculate averages across all 10 runs for velo driver
        gv_avgs = ['Velo Driver']
        list = gv_avg_list
        gv_sum = 0
        for i in range(0,len(list)):
            gv_sum += list[i]
        gv_sumavg = gv_sum / (len(list))
        gv_avgs.append(gv_sumavg)
        gv_avgs.append(max(list))
        gv_avgs.append(min(list))        

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
        
        return sg_avgs,gid_avgs,gv_avgs,gio_avgs,wd_list


def timing_table_current_run(timing_file,file,current,flag):

    timing_file.write('<HTML>\n')
    timing_file.write('<BODY BGCOLOR="#CADFE0">\n') 
    timing_file.write('<BODY>\n')
    
    if flag == 0:
        #call above definitions to get averages of avg, max, and min for each timer across 10 files
        sg_avgs,gid_avgs,gv_avgs,gio_avgs,wd_list = timing_averages(file,flag)

        #gather timing data from current run
        file1 = current + '/seacism_timing_stats'
        sg_avg,gid_avg,gv_avg,gio_avg,wdc_list = timing(file1,flag)
        sg_avgs.append(sg_avg)
        gid_avgs.append(gid_avg)
        gv_avgs.append(gv_avg)
        gio_avgs.append(gio_avg)
    
        columns = ['  ', 'Avg', 'Max', 'Min', 'Current Run']

        timing_file.write('<TABLE>\n')
        timing_file.write('<TR>')
        timing_file.write('<TABLE BORDER="1" CELLPADDING="6">\n')
        timing_file.write('<TH COLSPAN = "5">\n')
        timing_file.write('<H3><BR>Timing Data</H3>\n')
        timing_file.write('</TH>')
        timing_file.write('</TR>')
        timing_file.write('<TH>'   '</TH>')
        timing_file.write('<TH COLSPAN = "3">' + wd_list[1] + '</TH>')
        timing_file.write('<TH COLSPAN = "1">' + wdc_list + '</TH>')
        timing_file.write('<TR>')
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
            timing_file.write('<TD><font color="#4CC417">' + str(list[-1]) + '</font></TD>')
        else:
            timing_file.write('<TD>' + str(list[-1]) + '</TD>')
        timing_file.write('</TR>\n')

        #display data for initial diag var solve
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
            timing_file.write('<TD><font color="#4CC417">' + str(list[-1]) + '</font></TD>')
        else:
            timing_file.write('<TD>' + str(list[-1]) + '</TD>')
        timing_file.write('</TR>\n')

        #display data for velo driver
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
            timing_file.write('<TD><font color="#4CC417">' + str(list[-1]) + '</font></TD>')
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
            timing_file.write('<TD><font color="#4CC417">' + str(list[-1]) + '</font></TD>')
        else:
            timing_file.write('<TD>' + str(list[-1]) + '</TD>')
        timing_file.write('</TR>\n')

        timing_file.write('</TABLE>\n')
        timing_file.write('<H4><font color="#4CC417">Less than the Min</font></H4>')
        timing_file.write('<H4><font color="red">Greater than the Max</font></H4>')
        
        timing_file.write('<BR>\n')
        timing_file.write('<BR>\n')
        timing_file.write('<BR>\n')
        
    timing_file.write('</BODY>\n')
    timing_file.write('</HTML>\n')

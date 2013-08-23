#!/usr/bin/env

import sys
import os
from optparse import OptionParser
import subprocess
import collections
import VV_outprocess
import VV_utilities
import VV_checks

# routine for ISMIP HOM A 80km
def a80details(solver_file,job_path):  # using data, fill the web page with info

        failedt_list = []

	solver_file.write('<HTML>\n')
	solver_file.write('<H3>ISMIP HOM A 80km Iteration Count Details:</H3>')
	solver_file.write('<H4>Eventually published in plot form</H4>')
	solver_file.write('<BR> \n')
# JFNK gnu 1 proc

# Failure checking
        failedt1 = VV_checks.failcheck(job_path, '/ismip-hom-a/80km/data/ishom.a.80km.out.1')
        failedt_list.append(failedt1)

        solver_file.write('<H4>New Run: ishom.a.80km.out.1</H4>')
	procttl_ih1d, nonlist_ih1d, avg2_ih1d, out_flag_ih1d, ndiha1_name, ldiha1_name = VV_outprocess.jobprocess(job_path + '/ismip-hom-a/80km/data/ishom.a.80km.out.1', 'imhoma1')

	solver_file.write("Number of Processors = " + str(procttl_ih1d[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_ih1d)

# print this to an array that ncl can use for plotting
#                print item
	solver_file.write('<BR>\n')
	if out_flag_ih1d == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_ih1d)
# print this to an array that ncl can use for plotting
#                print item
	solver_file.write('<BR> \n')

	solver_file.write('<H4>Benchmark Run: ishom.a.80km.out.1</H4>')
	procttl_ih1b, nonlist_ih1b, avg2_ih1b, out_flag_ih1b, ndiha1b_name, ldiha1b_name = VV_outprocess.jobprocess(job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.out.1', 'imhoma1b')

	solver_file.write("Number of Processors = " + str(procttl_ih1b[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_ih1b)
	solver_file.write('<BR>\n')
	if out_flag_ih1b == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_ih1b)
	solver_file.write('<BR> \n')

# JFNK gnu 2 proc
	
#Failure checking
        failedt2 = VV_checks.failcheck(job_path, '/ismip-hom-a/80km/data/ishom.a.80km.out.2')
        failedt_list.append(failedt2)

        solver_file.write('<H4>New Run: ishom.a.80km.out.2</H4>')
	procttl_ih2d, nonlist_ih2d, avg2_ih2d, out_flag_ih2d, ndiha2_name, ldiha2_name = VV_outprocess.jobprocess(job_path + '/ismip-hom-a/80km/data/ishom.a.80km.out.2','imhoma2')

	solver_file.write("Number of Processors = " + str(procttl_ih2d[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_ih2d)
	solver_file.write('<BR>\n')
	if out_flag_ih2d == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) THAT FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_ih2d)
	solver_file.write('<BR> \n')

	solver_file.write('<H4>Benchmark Run: ishom.a.80km.out.2</H4>')
	procttl_ih2b, nonlist_ih2b, avg2_ih2b, out_flag_ih2b, ndiha2b_name, ldiha2b_name = VV_outprocess.jobprocess(job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.out.2','imhoma2b')

	solver_file.write("Number of Processors = " + str(procttl_ih2b[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_ih2b)
	solver_file.write('<BR>\n')
	if out_flag_ih2b == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) THAT FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_ih2b)
	solver_file.write('<BR> \n')

# JFNK gnu 4 proc
	
#Failure checking
        failedt3 = VV_checks.failcheck(job_path, '/ismip-hom-a/80km/data/ishom.a.80km.out.4')
        failedt_list.append(failedt3)

        solver_file.write('<H4>New Run: ishom.a.80km.out.4</H4>')
	procttl_ih4d, nonlist_ih4d, avg2_ih4d, out_flag_ih4d, ndiha4_name, ldiha4_name = VV_outprocess.jobprocess(job_path + '/ismip-hom-a/80km/data/ishom.a.80km.out.4','imhoma4')

	solver_file.write("Number of Processors = " + str(procttl_ih4d[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_ih4d)
	solver_file.write('<BR>\n')
	if out_flag_ih4d == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_ih4d)
	solver_file.write('<BR> \n')

	solver_file.write('<H4>Benchmark Run: ishom.a.80km.out.4</H4>')
	procttl_ih4b, nonlist_ih4b, avg2_ih4b, out_flag_ih4b, ndiha4b_name, ldiha4b_name = VV_outprocess.jobprocess(job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.out.4','imhoma4b')

	solver_file.write("Number of Processors = " + str(procttl_ih4b[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_ih4b)
	solver_file.write('<BR>\n')
	if out_flag_ih4b == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_ih4b)
	solver_file.write('<BR> \n')

	solver_file.write('</HTML>\n')
	solver_file.close()

        if 1 in failedt_list:
            failedt = 1
        else:
            failedt = 0

        return failedt

# routine for ISMIP HOM A 20km
def a20details(solver_file,job_path):  # using data, fill the web page with info

        failedt_list = []

	solver_file.write('<HTML>\n')
	solver_file.write('<H3>ISMIP HOM A 20km Iteration Count Details:</H3>')
	solver_file.write('<H4>Eventually published in plot form</H4>')
	solver_file.write('<BR> \n')
# JFNK gnu 1 proc

# Failure checking
        failedt1 = VV_checks.failcheck(job_path, '/ismip-hom-a/20km/data/ishom.a.20km.out.1')
        failedt_list.append(failedt1)

        solver_file.write('<H4>New Run: ishom.a.20km.out.1</H4>')
	procttl_ih1d, nonlist_ih1d, avg2_ih1d, out_flag_ih1d, ndiha1_name, ldiha1_name = VV_outprocess.jobprocess(job_path + '/ismip-hom-a/20km/data/ishom.a.20km.out.1', 'imhoma1')

	solver_file.write("Number of Processors = " + str(procttl_ih1d[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_ih1d)

# print this to an array that ncl can use for plotting
#                print item
	solver_file.write('<BR>\n')
	if out_flag_ih1d == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_ih1d)
# print this to an array that ncl can use for plotting
#                print item
	solver_file.write('<BR> \n')

	solver_file.write('<H4>Benchmark Run: ishom.a.20km.out.1</H4>')
	procttl_ih1b, nonlist_ih1b, avg2_ih1b, out_flag_ih1b, ndiha1b_name, ldiha1b_name = VV_outprocess.jobprocess(job_path + '/bench/ismip-hom-a/20km/data/ishom.a.20km.out.1', 'imhoma1b')

	solver_file.write("Number of Processors = " + str(procttl_ih1b[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_ih1b)
	solver_file.write('<BR>\n')
	if out_flag_ih1b == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_ih1b)
	solver_file.write('<BR> \n')

# JFNK gnu 2 proc
	
#Failure checking
        failedt2 = VV_checks.failcheck(job_path, '/ismip-hom-a/20km/data/ishom.a.20km.out.2')
        failedt_list.append(failedt2)

        solver_file.write('<H4>New Run: ishom.a.20km.out.2</H4>')
	procttl_ih2d, nonlist_ih2d, avg2_ih2d, out_flag_ih2d, ndiha2_name, ldiha2_name = VV_outprocess.jobprocess(job_path + '/ismip-hom-a/20km/data/ishom.a.20km.out.2','imhoma2')

	solver_file.write("Number of Processors = " + str(procttl_ih2d[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_ih2d)
	solver_file.write('<BR>\n')
	if out_flag_ih2d == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) THAT FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_ih2d)
	solver_file.write('<BR> \n')

	solver_file.write('<H4>Benchmark Run: ishom.a.20km.out.2</H4>')
	procttl_ih2b, nonlist_ih2b, avg2_ih2b, out_flag_ih2b, ndiha2b_name, ldiha2b_name = VV_outprocess.jobprocess(job_path + '/bench/ismip-hom-a/20km/data/ishom.a.20km.out.2','imhoma2b')

	solver_file.write("Number of Processors = " + str(procttl_ih2b[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_ih2b)
	solver_file.write('<BR>\n')
	if out_flag_ih2b == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) THAT FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_ih2b)
	solver_file.write('<BR> \n')

# JFNK gnu 4 proc
	
#Failure checking
        failedt3 = VV_checks.failcheck(job_path, '/ismip-hom-a/20km/data/ishom.a.20km.out.4')
        failedt_list.append(failedt3)

        solver_file.write('<H4>New Run: ishom.a.20km.out.4</H4>')
	procttl_ih4d, nonlist_ih4d, avg2_ih4d, out_flag_ih4d, ndiha4_name, ldiha4_name = VV_outprocess.jobprocess(job_path + '/ismip-hom-a/20km/data/ishom.a.20km.out.4','imhoma4')

	solver_file.write("Number of Processors = " + str(procttl_ih4d[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_ih4d)
	solver_file.write('<BR>\n')
	if out_flag_ih4d == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_ih4d)
	solver_file.write('<BR> \n')

	solver_file.write('<H4>Benchmark Run: ishom.a.20km.out.4</H4>')
	procttl_ih4b, nonlist_ih4b, avg2_ih4b, out_flag_ih4b, ndiha4b_name, ldiha4b_name = VV_outprocess.jobprocess(job_path + '/bench/ismip-hom-a/20km/data/ishom.a.20km.out.4','imhoma4b')

	solver_file.write("Number of Processors = " + str(procttl_ih4b[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_ih4b)
	solver_file.write('<BR>\n')
	if out_flag_ih4b == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_ih4b)
	solver_file.write('<BR> \n')

	solver_file.write('</HTML>\n')
	solver_file.close()

        if 1 in failedt_list:
            failedt = 1
        else:
            failedt = 0

        return failedt


# routine for ISMIP HOM C 80km
def c80details(solver_file,job_path):  # using data, fill the web page with info

        failedt_list = []

	solver_file.write('<HTML>\n')
	solver_file.write('<H3>ISMIP HOM C Iteration Count Details:</H3>')
	solver_file.write('<H4>Eventually published in plot form</H4>')
	solver_file.write('<BR> \n')
# JFNK gnu 1 proc
	
#Failure checking
        failedt1 = VV_checks.failcheck(job_path, '/ismip-hom-c/80km/data/ishom.c.80km.out.1')
        failedt_list.append(failedt1)

        solver_file.write('<H4>New Run: ishom.c.80km.out.1</H4>')
	procttl_ih1d, nonlist_ih1d, avg2_ih1d, out_flag_ih1d, ndihc1_name, ldihc1_name = VV_outprocess.jobprocess(job_path + '/ismip-hom-c/80km/data/ishom.c.80km.out.1','imhomc1')

	solver_file.write("Number of Processors = " + str(procttl_ih1d[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_ih1d)

# print this to an array that ncl can use for plotting
#                print item
	solver_file.write('<BR>\n')
	if out_flag_ih1d == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_ih1d)

# print this to an array that ncl can use for plotting
#                print item
	solver_file.write('<BR> \n')

	solver_file.write('<H4>Benchmark Run: ishom.c.80km.out.1</H4>')
	procttl_ih1b, nonlist_ih1b, avg2_ih1b, out_flag_ih1b, ndihc1b_name, ldihc1b_name = VV_outprocess.jobprocess(job_path + '/bench/ismip-hom-c/80km/data/ishom.c.80km.out.1','imhomc1b')

	solver_file.write("Number of Processors = " + str(procttl_ih1b[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_ih1b)
	solver_file.write('<BR>\n')
	if out_flag_ih1b == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_ih1b)
	solver_file.write('<BR> \n')

# JFNK gnu 2 proc
	
#Failure checking
        failedt2 = VV_checks.failcheck(job_path, '/ismip-hom-c/80km/data/ishom.c.80km.out.2')
        failedt_list.append(failedt2)

        solver_file.write('<H4>New Run: ishom.c.80km.out.2</H4>')
	procttl_ih2d, nonlist_ih2d, avg2_ih2d, out_flag_ih2d, ndihc2_name, ldihc2_name = VV_outprocess.jobprocess(job_path + '/ismip-hom-c/80km/data/ishom.c.80km.out.2','imhom2')

	solver_file.write("Number of Processors = " + str(procttl_ih2d[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_ih2d)
	solver_file.write('<BR>\n')
	if out_flag_ih2d == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) THAT FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_ih2d)
	solver_file.write('<BR> \n')

	solver_file.write('<H4>Benchmark Run: ishom.c.80km.out.2</H4>')
	procttl_ih2b, nonlist_ih2b, avg2_ih2b, out_flag_ih2b, ndihc2b_name, ldihc2b_name = VV_outprocess.jobprocess(job_path + '/bench/ismip-hom-c/80km/data/ishom.c.80km.out.2','imhom2b')

	solver_file.write("Number of Processors = " + str(procttl_ih2b[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_ih2b)
	solver_file.write('<BR>\n')
	if out_flag_ih2b == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) THAT FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_ih2b)
	solver_file.write('<BR> \n')

# JFNK gnu 4 proc

#Failure checking
        failedt3 = VV_checks.failcheck(job_path, '/ismip-hom-c/80km/data/ishom.c.80km.out.4')
        failedt_list.append(failedt3)

        solver_file.write('<H4>New Run: ishom.c.80km.out.4</H4>')
	procttl_ih4d, nonlist_ih4d, avg2_ih4d, out_flag_ih4d, ndihc4_name, ldihc4_name = VV_outprocess.jobprocess(job_path + '/ismip-hom-c/80km/data/ishom.c.80km.out.4','imhomc4')

	solver_file.write("Number of Processors = " + str(procttl_ih4d[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_ih4d)
	solver_file.write('<BR>\n')
	if out_flag_ih4d == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_ih4d)
	solver_file.write('<BR> \n')

	solver_file.write('<H4>Benchmark Run: ishom.c.80km.out.4</H4>')
	procttl_ih4b, nonlist_ih4b, avg2_ih4b, out_flag_ih4b, ndihc4b_name, ldihc4b_name = VV_outprocess.jobprocess(job_path + '/bench/ismip-hom-c/80km/data/ishom.c.80km.out.4','imhomc4b')

	solver_file.write("Number of Processors = " + str(procttl_ih4b[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_ih4b)
	solver_file.write('<BR>\n')
	if out_flag_ih4b == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_ih4b)
	solver_file.write('<BR> \n')

	solver_file.write('</HTML>\n')
	solver_file.close()

        if 1 in failedt_list:
            failedt = 1
        else:
            failedt = 0

        return failedt

def a80plot(plot_file,job_path,ncl_path,html_path,script_path):  # using data, fill the web page with info

        plot_file.write('<HTML>\n')
        plot_file.write('<H3>ISMIP HOM A 80km Plot Details:</H3>')

# formulate ismip a 80 uvel plot
        ishoma80u_plotfile=''+ ncl_path + '/ismipa80u.ncl'
        stockout ='STOCKout = addfile(\"'+ job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.out.nc\", \"r\")'
        stockPIC ='STOCKPIC = addfile(\"'+ job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc\", \"r\")'
        stockJFNK ='STOCKJFNK = addfile(\"'+ job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc\", \"r\")'
        VARout  ='VARout = addfile(\"' + job_path + '/ismip-hom-a/80km/data/ishom.a.80km.out.nc\", \"r\")'
        VARPIC  ='VARPIC = addfile(\"' + job_path + '/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc\", \"r\")'
        VARJFNK  ='VARJFNK = addfile(\"' + job_path + '/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc\", \"r\")'
        png  = 'PNG = "' + ncl_path + '/ismipa80u"'
        plot_ishoma80u = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" + png + "' " + ishoma80u_plotfile + " >> plot_details.out"
            

#TODO create an iteration plot and have that also in the html file 
        try:
                output = subprocess.call(plot_ishoma80u, shell=True)
                print "creating ismip hom a 80km uvel plots"
        except:
                print "error creating ncl ismip hom a 80km uvel plots"
                raise

# delete old ismipa80 uvel pic in www file

        if (html_path + '/ismipa80u.png'):
                ismipa80uvelmove = "rm -f " + html_path + '/ismipa80u.png'
                try:
                        output = subprocess.call(ismipa80uvelmove, shell=True)
                except:
                        print "error removing old ismip a 80km uvel png file from www directory"
                        sys.exit(1)
                        raise

# transferring ismipau pic to www file

        if (ncl_path + '/ismipa80u.png'): 
                ishoma80upic = "mv -f " + ncl_path + "/ismipa80u.png" + " " + html_path + "/"
                try:
                        output = subprocess.call(ishoma80upic, shell=True)
                except:
                        print "error moving ismip hom au 80km png file to www directory"
                        sys.exit(1)
                        raise

# formulate ismip a 80 vvel plot
        ishoma80v_plotfile=''+ ncl_path + '/ismipa80v.ncl'
        stockout ='STOCKout = addfile(\"'+ job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.out.nc\", \"r\")'
        stockPIC ='STOCKPIC = addfile(\"'+ job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc\", \"r\")'
        stockJFNK ='STOCKJFNK = addfile(\"'+ job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc\", \"r\")'
        VARout  ='VARout = addfile(\"' + job_path + '/ismip-hom-a/80km/data/ishom.a.80km.out.nc\", \"r\")'
        VARPIC  ='VARPIC = addfile(\"' + job_path + '/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc\", \"r\")'
        VARJFNK  ='VARJFNK = addfile(\"' + job_path + '/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc\", \"r\")'
        png  = 'PNG = "' + ncl_path + '/ismipa80v"'
        plot_ishoma80v = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" + png + "' " + ishoma80v_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
        try:
                output = subprocess.call(plot_ishoma80v, shell=True)
                print "creating ismip hom a 80km vvel plots"
        except:
                print "error creating ncl ismip hom a 80km vvel plots"
                raise

# delete old ismipa80 vvel pic in www file

        if (html_path + '/ismipa80v.png'):
                ismipa80vvelmove = "rm -f " + html_path + '/ismipa80v.png'
                try:
                        output = subprocess.call(ismipa80vvelmove, shell=True)
                except:
                        print "error removing old ismip a 80km vvel png file from www directory"
                        sys.exit(1)
                        raise

# transferring ismipav pic to www file

        if (ncl_path + '/ismipa80v.png'): 
                ishoma80vpic = "mv -f " + ncl_path + "/ismipa80v.png" + " " + html_path + "/"
                try:
                        output = subprocess.call(ishoma80vpic, shell=True)
                except:
                        print "error moving ismip hom av 80km png file to www directory"
                        sys.exit(1)
                        raise

# formulate ismip a 80 velocity norm plot
#        ishoma80vel_plotfile=''+ ncl_path + '/ismipa80vel.ncl'
#        stockPIC ='STOCKPIC = addfile(\"'+ job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc\", \"r\")'
#        stockJFNK ='STOCKJFNK = addfile(\"'+ job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc\", \"r\")'
#        VARPIC  ='VARPIC = addfile(\"' + job_path + '/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc\", \"r\")'
#        VARJFNK  ='VARJFNK = addfile(\"' + job_path + '/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc\", \"r\")'
#        png  = 'PNG = "' + ncl_path + '/ismipa80vel"'
#        plot_ishoma80vel = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" + png + "' " + ishoma80vel_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
#        try:
#                output = subprocess.call(plot_ishoma80vel, shell=True)
#                print "creating ismip hom a 80km velocity norm plots"
#        except:
#                print "error creating ncl ismip hom a 80km vel norm plots"
#                raise

# delete old ismipa80 velnorm pic in www file

#        if (html_path + '/ismipa80vel.png'):
#                ismipa80velmove = "rm -f " + html_path + '/ismipa80vel.png'
#                try:
#                        output = subprocess.call(ismipa80velmove, shell=True)
#                except:
#                        print "error removing old ismip a 80km vel norm png file from www directory"
#                        sys.exit(1)
#                        raise

# transferring ismip a 80km velocity norm pic to www file

#        if (ncl_path + '/ismipa80vel.png'): 
#                ishoma80velpic = "mv -f " + ncl_path + "/ismipa80vel.png" + " " + html_path + "/"
#                try:
#                        output = subprocess.call(ishoma80velpic, shell=True)
#                except:
#                        print "error moving ismip hom a 80km velocity png file to www directory"
#                        sys.exit(1)
#                        raise

# formulate ismip a 80 thickness norm plot
        ishoma80thk_plotfile=''+ ncl_path + '/ismipa80thk.ncl'
        stockPIC ='STOCKPIC = addfile(\"'+ job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc\", \"r\")'
        stockJFNK ='STOCKJFNK = addfile(\"'+ job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc\", \"r\")'
        VARPIC  ='VARPIC = addfile(\"' + job_path + '/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc\", \"r\")'
        VARJFNK  ='VARJFNK = addfile(\"' + job_path + '/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc\", \"r\")'
        png  = 'PNG = "' + ncl_path + '/ismipa80thk"'
        plot_ishoma80thk = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" + png + "' " + ishoma80thk_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
        try:
                output = subprocess.call(plot_ishoma80thk, shell=True)
                print "creating ismip hom a 80km thickness plots"
        except:
                print "error creating ncl ismip hom a 80km thickness plots"
                raise

# delete old ismipa80 thk pic in www file

        if (html_path + '/ismipa80thk.png'):
                ismipa80thkmove = "rm -f " + html_path + '/ismipa80thk.png'
                try:
                        output = subprocess.call(ismipa80thkmove, shell=True)
                except:
                        print "error removing old ismip a 80km thickness png file from www directory"
                        sys.exit(1)
                        raise

# transferring ismip a 80km thickness norm pic to www file

        if (ncl_path + '/ismipa80thk.png'): 
                ishoma80thkpic = "mv -f " + ncl_path + "/ismipa80thk.png" + " " + html_path + "/"
                try:
                        output = subprocess.call(ishoma80thkpic, shell=True)
                except:
                        print "error moving ismip hom a thickness 80km png file to www directory"
                        sys.exit(1)
                        raise

# remove plot_details.out
#        if (script_path + '/plot_details.out'):
#                cleantrash = "rm -f " + script_path + "/plot_details.out"
#                try:
#                        output = subprocess.call(cleantrash, shell=True)
#                except:
#                        print "error removing plot_details.out"
#                        sys.exit(1)
#                        raise

        plot_file.write('<HTML>\n')
        plot_file.write('<TITLE>ISMIP HOM A 80km </TITLE>\n')
        plot_file.write('<TABLE>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<H4>Difference from benchmark run for U Velocity, V Velocity, Velocity Norm, and Thickness</H4>\n')
        plot_file.write('<BR>\n')
        plot_file.write('<OBJECT data="ismipa80u.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 80km Plots">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<OBJECT data="ismipa80v.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 80km Plots">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<OBJECT data="ismipa80vel.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 80km Plots">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<OBJECT data="ismipa80thk.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 80km Plots">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<BR>\n')
        plot_file.write('</TABLE>\n')
        plot_file.write('</HTML>\n')
        plot_file.close()

def a20plot(plot_file,job_path,ncl_path,html_path,script_path):  # using data, fill the web page with info

        plot_file.write('<HTML>\n')
        plot_file.write('<H3>ISMIP HOM A 20km Plot Details:</H3>')

# formulate ismip a 20 uvel plot
        ishoma20u_plotfile=''+ ncl_path + '/ismipa20u.ncl'
        stockout ='STOCKout = addfile(\"'+ job_path + '/bench/ismip-hom-a/20km/data/ishom.a.20km.out.nc\", \"r\")'
        stockPIC ='STOCKPIC = addfile(\"'+ job_path + '/bench/ismip-hom-a/20km/data/ishom.a.20km.PIC.out.nc\", \"r\")'
        stockJFNK ='STOCKJFNK = addfile(\"'+ job_path + '/bench/ismip-hom-a/20km/data/ishom.a.20km.JFNK.out.nc\", \"r\")'
        VARout  ='VARout = addfile(\"' + job_path + '/ismip-hom-a/20km/data/ishom.a.20km.out.nc\", \"r\")'
        VARPIC  ='VARPIC = addfile(\"' + job_path + '/ismip-hom-a/20km/data/ishom.a.20km.PIC.out.nc\", \"r\")'
        VARJFNK  ='VARJFNK = addfile(\"' + job_path + '/ismip-hom-a/20km/data/ishom.a.20km.JFNK.out.nc\", \"r\")'
        png  = 'PNG = "' + ncl_path + '/ismipa20u"'
        plot_ishoma20u = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" + png + "' " + ishoma20u_plotfile + " >> plot_details.out"
            

#TODO create an iteration plot and have that also in the html file 
        try:
                output = subprocess.call(plot_ishoma20u, shell=True)
                print "creating ismip hom a 20km uvel plots"
        except:
                print "error creating ncl ismip hom a 20km uvel plots"
                raise

# delete old ismipa20 uvel pic in www file

        if (html_path + '/ismipa20u.png'):
                ismipa20uvelmove = "rm -f " + html_path + '/ismipa20u.png'
                try:
                        output = subprocess.call(ismipa20uvelmove, shell=True)
                except:
                        print "error removing old ismip a 20km uvel png file from www directory"
                        sys.exit(1)
                        raise

# transferring ismipa20u pic to www file

        if (ncl_path + '/ismipa20u.png'): 
                ishoma20upic = "mv -f " + ncl_path + "/ismipa20u.png" + " " + html_path + "/"
                try:
                        output = subprocess.call(ishoma20upic, shell=True)
                except:
                        print "error moving ismip hom au 20km png file to www directory"
                        sys.exit(1)
                        raise

# formulate ismip a 20 vvel plot
        ishoma20v_plotfile=''+ ncl_path + '/ismipa20v.ncl'
        stockout ='STOCKout = addfile(\"'+ job_path + '/bench/ismip-hom-a/20km/data/ishom.a.20km.out.nc\", \"r\")'
        stockPIC ='STOCKPIC = addfile(\"'+ job_path + '/bench/ismip-hom-a/20km/data/ishom.a.20km.PIC.out.nc\", \"r\")'
        stockJFNK ='STOCKJFNK = addfile(\"'+ job_path + '/bench/ismip-hom-a/20km/data/ishom.a.20km.JFNK.out.nc\", \"r\")'
        VARout  ='VARout = addfile(\"' + job_path + '/ismip-hom-a/20km/data/ishom.a.20km.out.nc\", \"r\")'
        VARPIC  ='VARPIC = addfile(\"' + job_path + '/ismip-hom-a/20km/data/ishom.a.20km.PIC.out.nc\", \"r\")'
        VARJFNK  ='VARJFNK = addfile(\"' + job_path + '/ismip-hom-a/20km/data/ishom.a.20km.JFNK.out.nc\", \"r\")'
        png  = 'PNG = "' + ncl_path + '/ismipa20v"'
        plot_ishoma20v = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" + png + "' " + ishoma20v_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
        try:
                output = subprocess.call(plot_ishoma20v, shell=True)
                print "creating ismip hom a 20km vvel plots"
        except:
                print "error creating ncl ismip hom a 20km vvel plots"
                raise

# delete old ismipa20 vvel pic in www file

        if (html_path + '/ismipa20v.png'):
                ismipa20vvelmove = "rm -f " + html_path + '/ismipa20v.png'
                try:
                        output = subprocess.call(ismipa20vvelmove, shell=True)
                except:
                        print "error removing old ismip a 20km vvel png file from www directory"
                        sys.exit(1)
                        raise

# transferring ismipa20v pic to www file

        if (ncl_path + '/ismipa20v.png'): 
                ishoma20vpic = "mv -f " + ncl_path + "/ismipa20v.png" + " " + html_path + "/"
                try:
                        output = subprocess.call(ishoma20vpic, shell=True)
                except:
                        print "error moving ismip hom av 20km png file to www directory"
                        sys.exit(1)
                        raise

# formulate ismip a 20 velocity norm plot
#        ishoma20vel_plotfile=''+ ncl_path + '/ismipa20vel.ncl'
#        stockPIC ='STOCKPIC = addfile(\"'+ job_path + '/bench/ismip-hom-a/20km/data/ishom.a.20km.PIC.out.nc\", \"r\")'
#        stockJFNK ='STOCKJFNK = addfile(\"'+ job_path + '/bench/ismip-hom-a/20km/data/ishom.a.20km.JFNK.out.nc\", \"r\")'
#        VARPIC  ='VARPIC = addfile(\"' + job_path + '/ismip-hom-a/20km/data/ishom.a.20km.PIC.out.nc\", \"r\")'
#        VARJFNK  ='VARJFNK = addfile(\"' + job_path + '/ismip-hom-a/20km/data/ishom.a.20km.JFNK.out.nc\", \"r\")'
#        png  = 'PNG = "' + ncl_path + '/ismipa20vel"'
#        plot_ishoma20vel = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" + png + "' " + ishoma20vel_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
#        try:
#                output = subprocess.call(plot_ishoma20vel, shell=True)
#                print "creating ismip hom a 20km velocity norm plots"
#        except:
#                print "error creating ncl ismip hom a 20km vel norm plots"
#                raise

# delete old ismipa20 velnorm pic in www file

#        if (html_path + '/ismipa20vel.png'):
#                ismipa20velmove = "rm -f " + html_path + '/ismipa20vel.png'
#                try:
#                        output = subprocess.call(ismipa20velmove, shell=True)
#                except:
#                        print "error removing old ismip a 20km vel norm png file from www directory"
#                        sys.exit(1)
#                        raise

# transferring ismip a 20km velocity norm pic to www file

#        if (ncl_path + '/ismipa20vel.png'): 
#                ishoma20velpic = "mv -f " + ncl_path + "/ismipa20vel.png" + " " + html_path + "/"
#                try:
#                        output = subprocess.call(ishoma20velpic, shell=True)
#                except:
#                        print "error moving ismip hom a velocity 20km png file to www directory"
#                        sys.exit(1)
#                        raise

# formulate ismip a 20 thickness norm plot
        ishoma20thk_plotfile=''+ ncl_path + '/ismipa20thk.ncl'
        stockPIC ='STOCKPIC = addfile(\"'+ job_path + '/bench/ismip-hom-a/20km/data/ishom.a.20km.PIC.out.nc\", \"r\")'
        stockJFNK ='STOCKJFNK = addfile(\"'+ job_path + '/bench/ismip-hom-a/20km/data/ishom.a.20km.JFNK.out.nc\", \"r\")'
        VARPIC  ='VARPIC = addfile(\"' + job_path + '/ismip-hom-a/20km/data/ishom.a.20km.PIC.out.nc\", \"r\")'
        VARJFNK  ='VARJFNK = addfile(\"' + job_path + '/ismip-hom-a/20km/data/ishom.a.20km.JFNK.out.nc\", \"r\")'
        png  = 'PNG = "' + ncl_path + '/ismipa20thk"'
        plot_ishoma20thk = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" + png + "' " + ishoma20thk_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
        try:
                output = subprocess.call(plot_ishoma20thk, shell=True)
                print "creating ismip hom a 20km thickness plots"
        except:
                print "error creating ncl ismip hom a 20km thickness plots"
                raise

# delete old ismipa20 thk pic in www file

        if (html_path + '/ismipa20thk.png'):
                ismipa20thkmove = "rm -f " + html_path + '/ismipa20thk.png'
                try:
                        output = subprocess.call(ismipa20thkmove, shell=True)
                except:
                        print "error removing old ismip a 20km thickness png file from www directory"
                        sys.exit(1)
                        raise

# transferring ismip a 20km thickness norm pic to www file

        if (ncl_path + '/ismipa20thk.png'): 
                ishoma20thkpic = "mv -f " + ncl_path + "/ismipa20thk.png" + " " + html_path + "/"
                try:
                        output = subprocess.call(ishoma20thkpic, shell=True)
                except:
                        print "error moving ismip hom a 20km thickness png file to www directory"
                        sys.exit(1)
                        raise

# remove plot_details.out
#        if (script_path + '/plot_details.out'):
#                cleantrash = "rm -f " + script_path + "/plot_details.out"
#                try:
#                        output = subprocess.call(cleantrash, shell=True)
#                except:
#                        print "error removing plot_details.out"
#                        sys.exit(1)
#                        raise

        plot_file.write('<HTML>\n')
        plot_file.write('<TITLE>ISMIP HOM A 20km </TITLE>\n')
        plot_file.write('<TABLE>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<H4>Difference from benchmark run for U Velocity, V Velocity, Velocity Norm, and Thickness</H4>\n')
        plot_file.write('<BR>\n')
        plot_file.write('<OBJECT data="ismipa20u.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 20km Plots">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<OBJECT data="ismipa20v.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 20km Plots">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<OBJECT data="ismipa20vel.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 20km Plots">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<OBJECT data="ismipa20thk.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 20km Plots">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<BR>\n')
        plot_file.write('</TABLE>\n')
        plot_file.write('</HTML>\n')
        plot_file.close()


def c80plot(plot_file,job_path,ncl_path,html_path,script_path):  # using data, fill the web page with info

        plot_file.write('<HTML>\n')
        plot_file.write('<H3>ISMIP HOM C 80km Plot Details:</H3>')
        
# formulate ismip c 80 uvel plot
        ishomcu_plotfile=''+ ncl_path + '/ismipc80u.ncl'
        stockout ='STOCKout = addfile(\"'+ job_path + '/bench/ismip-hom-c/80km/data/ishom.c.80km.out.nc\", \"r\")'
        stockPIC ='STOCKPIC = addfile(\"'+ job_path + '/bench/ismip-hom-c/80km/data/ishom.c.80km.PIC.out.nc\", \"r\")'
        stockJFNK ='STOCKJFNK = addfile(\"'+ job_path + '/bench/ismip-hom-c/80km/data/ishom.c.80km.JFNK.out.nc\", \"r\")'
        VARout  ='VARout = addfile(\"' + job_path + '/ismip-hom-c/80km/data/ishom.c.80km.out.nc\", \"r\")'
        VARPIC  ='VARPIC = addfile(\"' + job_path + '/ismip-hom-c/80km/data/ishom.c.80km.PIC.out.nc\", \"r\")'
        VARJFNK  ='VARJFNK = addfile(\"' + job_path + '/ismip-hom-c/80km/data/ishom.c.80km.JFNK.out.nc\", \"r\")'
        png  = 'PNG = "' + ncl_path + '/ismipcu"'
        plot_ishomcu = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" + png + "' " + ishomcu_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
        try:
                output = subprocess.call(plot_ishomcu, shell=True)
                print "creating ismip hom c uvel plots"
        except:
                print "error creating ncl ismip hom c uvel plots"
                raise

# delete old ismipc80 uvel pic in www file

        if (html_path + '/ismipcu.png'):
                ismipcuvelmove = "rm -f " + html_path + '/ismipcu.png'
                try:
                        output = subprocess.call(ismipcuvelmove, shell=True)
                except:
                        print "error removing old ismip c uvel png file from www directory"
                        sys.exit(1)
                        raise

# transferring ismipcu pic to www file

        if (ncl_path + '/ismipcu.png'): 
                ishomcupic = "mv -f " + ncl_path + "/ismipcu.png" + " " + html_path + "/"
                try:
                        output = subprocess.call(ishomcupic, shell=True)
                except:
                        print "error moving ismip hom cu 80km png file to www directory"
                        sys.exit(1)
                        raise

# formulate ismip c 80 vvel plot
        ishomcv_plotfile=''+ ncl_path + '/ismipc80v.ncl'
        stockout ='STOCKout = addfile(\"'+ job_path + '/bench/ismip-hom-c/80km/data/ishom.c.80km.out.nc\", \"r\")'
        stockPIC ='STOCKPIC = addfile(\"'+ job_path + '/bench/ismip-hom-c/80km/data/ishom.c.80km.PIC.out.nc\", \"r\")'
        stockJFNK ='STOCKJFNK = addfile(\"'+ job_path + '/bench/ismip-hom-c/80km/data/ishom.c.80km.JFNK.out.nc\", \"r\")'
        VARout  ='VARout = addfile(\"' + job_path + '/ismip-hom-c/80km/data/ishom.c.80km.out.nc\", \"r\")'
        VARPIC  ='VARPIC = addfile(\"' + job_path + '/ismip-hom-c/80km/data/ishom.c.80km.PIC.out.nc\", \"r\")'
        VARJFNK  ='VARJFNK = addfile(\"' + job_path + '/ismip-hom-c/80km/data/ishom.c.80km.JFNK.out.nc\", \"r\")'
        png  = 'PNG = "' + ncl_path + '/ismipcv"'
        plot_ishomcv = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" + png + "' " + ishomcv_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
        try:
                output = subprocess.call(plot_ishomcv, shell=True)
                print "creating ismip hom c vvel plots"
        except:
                print "error creating ncl ismip hom c vvel plots"
                raise

# delete old ismipc80 vvel pic in www file

        if (html_path + '/ismipcv.png'):
                ismipcvvelmove = "rm -f " + html_path + '/ismipcv.png'
                try:
                        output = subprocess.call(ismipcvvelmove, shell=True)
                except:
                        print "error removing old ismip c vvel png file from www directory"
                        sys.exit(1)
                        raise

# transferring ismipcv pic to www file

        if (ncl_path + '/ismipcv.png'): 
                ishomcvpic = "mv -f " + ncl_path + "/ismipcv.png" + " " + html_path + "/"
                try:
                        output = subprocess.call(ishomcvpic, shell=True)
                except:
                        print "error moving ismip hom cv 80km png file to www directory"
                        sys.exit(1)
                        raise

# formulate ismip c 80 velocity norm plot
        ishomcvel_plotfile=''+ ncl_path + '/ismipc80vel.ncl'
        stockPIC ='STOCKPIC = addfile(\"'+ job_path + '/bench/ismip-hom-c/80km/data/ishom.c.80km.PIC.out.nc\", \"r\")'
        stockJFNK ='STOCKJFNK = addfile(\"'+ job_path + '/bench/ismip-hom-c/80km/data/ishom.c.80km.JFNK.out.nc\", \"r\")'
        VARPIC  ='VARPIC = addfile(\"' + job_path + '/ismip-hom-c/80km/data/ishom.c.80km.PIC.out.nc\", \"r\")'
        VARJFNK  ='VARJFNK = addfile(\"' + job_path + '/ismip-hom-c/80km/data/ishom.c.80km.JFNK.out.nc\", \"r\")'
        png  = 'PNG = "' + ncl_path + '/ismipcvel"'
        plot_ishomcvel = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" + png + "' " + ishomcvel_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
        try:
                output = subprocess.call(plot_ishomcvel, shell=True)
                print "creating ismip hom c velocity norm plots"
        except:
                print "error creating ncl ismip hom c vel norm plots"
                raise

# delete old ismipc80 vel norm pic in www file

        if (html_path + '/ismipcvel.png'):
                ismipcvelmove = "rm -f " + html_path + '/ismipcvel.png'
                try:
                        output = subprocess.call(ismipcvelmove, shell=True)
                except:
                        print "error removing old ismip c vel norm png file from www directory"
                        sys.exit(1)
                        raise

# transferring ismip c velocity norm pic to www file

        if (ncl_path + '/ismipcvel.png'): 
                ishomcvelpic = "mv -f " + ncl_path + "/ismipcvel.png" + " " + html_path + "/"
                try:
                        output = subprocess.call(ishomcvelpic, shell=True)
                except:
                        print "error moving ismip hom c velocity 80km png file to www directory"
                        sys.exit(1)
                        raise

# formulate ismip c 80 thickness norm plot
        ishomcthk_plotfile=''+ ncl_path + '/ismipc80thk.ncl'
        stockPIC ='STOCKPIC = addfile(\"'+ job_path + '/bench/ismip-hom-c/80km/data/ishom.c.80km.PIC.out.nc\", \"r\")'
        stockJFNK ='STOCKJFNK = addfile(\"'+ job_path + '/bench/ismip-hom-c/80km/data/ishom.c.80km.JFNK.out.nc\", \"r\")'
        VARPIC  ='VARPIC = addfile(\"' + job_path + '/ismip-hom-c/80km/data/ishom.c.80km.PIC.out.nc\", \"r\")'
        VARJFNK  ='VARJFNK = addfile(\"' + job_path + '/ismip-hom-c/80km/data/ishom.c.80km.JFNK.out.nc\", \"r\")'
        png  = 'PNG = "' + ncl_path + '/ismipcthk"'
        plot_ishomcthk = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" + png + "' " + ishomcthk_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
        try:
                output = subprocess.call(plot_ishomcthk, shell=True)
                print "creating ismip hom c thickness plots"
        except:
                print "error creating ncl ismip hom c thickness plots"
                raise

# delete old ismipc80 thk pic in www file

        if (html_path + '/ismipcthk.png'):
                ismipcthkmove = "rm -f " + html_path + '/ismipcthk.png'
                try:
                        output = subprocess.call(ismipcthkmove, shell=True)
                except:
                        print "error removing old ismip c thk png file from www directory"
                        sys.exit(1)
                        raise

# transferring ismip c thickness norm pic to www file

        if (ncl_path + '/ismipcthk.png'): 
                ishomcthkpic = "mv -f " + ncl_path + "/ismipcthk.png" + " " + html_path + "/"
                try:
                        output = subprocess.call(ishomcthkpic, shell=True)
                except:
                        print "error moving ismip hom c thickness 80km png file to www directory"
                        sys.exit(1)

# remove plot_details.out
#        if (script_path + '/plot_details.out'):
#                cleantrash = "rm -f " + script_path + "/plot_details.out"
#                try:
#                        output = subprocess.call(cleantrash, shell=True)
#                except:
#                        print "error removing plot_details.out"
#                        sys.exit(1)
#                        raise

        plot_file.write('<HTML>\n')
        plot_file.write('<TITLE>ISMIP HOM C 80km </TITLE>\n')
        plot_file.write('<TABLE>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<H4>Difference from benchmark run for U Velocity, V Velocity, Velocity Norm, and Thickness</H4>\n')
        plot_file.write('<BR>\n')
        plot_file.write('<OBJECT data="ismipcu.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM C 80km Plots">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<OBJECT data="ismipcv.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM C 80km Plots">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<OBJECT data="ismipcvel.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM C 80km Plots">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<OBJECT data="ismipcthk.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM C 80km Plots">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<BR>\n')
        plot_file.write('</TABLE>\n')
        plot_file.write('</HTML>\n')
        plot_file.close()



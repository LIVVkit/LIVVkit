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

        noplot = 0    

        tmpath = job_path + '/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc'
        if VV_utilities.emptycheck(tmpath) == 0:
                noplot = 1

        if noplot == 0:

            plot_file.write('<HTML>\n')
            plot_file.write('<H3>ISMIP HOM A 80km Plot Details:</H3>')

# formulate ismip a 80 uvel plot
            ishomau_plotfile=''+ ncl_path + '/ismipa80u.ncl'
            stockout ='STOCKout = addfile(\"'+ job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.out.nc\", \"r\")'
            stockPIC ='STOCKPIC = addfile(\"'+ job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc\", \"r\")'
            stockJFNK ='STOCKJFNK = addfile(\"'+ job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc\", \"r\")'
            VARout  ='VARout = addfile(\"' + job_path + '/ismip-hom-a/80km/data/ishom.a.80km.out.nc\", \"r\")'
            VARPIC  ='VARPIC = addfile(\"' + job_path + '/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc\", \"r\")'
            VARJFNK  ='VARJFNK = addfile(\"' + job_path + '/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc\", \"r\")'
            png  = 'PNG = "' + ncl_path + '/ismipau"'
            plot_ishomau = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" + png + "' " + ishomau_plotfile + " >& plot_details.out"
            

#TODO create an iteration plot and have that also in the html file 
            try:
                    output = subprocess.call(plot_ishomau, shell=True)
                    print "creating ismip hom a uvel plots"
            except:
                    print "error creating ncl ismip hom a uvel plots"
                    raise

# delete old ismipa80 uvel pic in www file

            if (html_path + '/ismipau.png'):
                    ismipauvelmove = "rm -f " + html_path + '/ismipau.png'
                    try:
                            output = subprocess.call(ismipauvelmove, shell=True)
                    except:
                            print "error removing old ismip a uvel png file from www directory"
                            sys.exit(1)
                            raise

# transferring ismipau pic to www file

            if (ncl_path + '/ismipau.png'): 
                    ishomaupic = "mv -f " + ncl_path + "/ismipau.png" + " " + html_path + "/"
                    try:
                            output = subprocess.call(ishomaupic, shell=True)
                    except:
                            print "error moving ismip hom au 80km png file to www directory"
                            sys.exit(1)
                            raise

# formulate ismip a 80 vvel plot
            ishomav_plotfile=''+ ncl_path + '/ismipa80v.ncl'
            stockout ='STOCKout = addfile(\"'+ job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.out.nc\", \"r\")'
            stockPIC ='STOCKPIC = addfile(\"'+ job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc\", \"r\")'
            stockJFNK ='STOCKJFNK = addfile(\"'+ job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc\", \"r\")'
            VARout  ='VARout = addfile(\"' + job_path + '/ismip-hom-a/80km/data/ishom.a.80km.out.nc\", \"r\")'
            VARPIC  ='VARPIC = addfile(\"' + job_path + '/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc\", \"r\")'
            VARJFNK  ='VARJFNK = addfile(\"' + job_path + '/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc\", \"r\")'
            png  = 'PNG = "' + ncl_path + '/ismipav"'
            plot_ishomav = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" + png + "' " + ishomav_plotfile + " >& plot_details.out"

#TODO create an iteration plot and have that also in the html file 
            try:
                    output = subprocess.call(plot_ishomav, shell=True)
                    print "creating ismip hom a vvel plots"
            except:
                    print "error creating ncl ismip hom a vvel plots"
                    raise

# delete old ismipa80 vvel pic in www file

            if (html_path + '/ismipav.png'):
                    ismipavvelmove = "rm -f " + html_path + '/ismipav.png'
                    try:
                            output = subprocess.call(ismipavvelmove, shell=True)
                    except:
                            print "error removing old ismip a vvel png file from www directory"
                            sys.exit(1)
                            raise

# transferring ismipav pic to www file

            if (ncl_path + '/ismipav.png'): 
                    ishomavpic = "mv -f " + ncl_path + "/ismipav.png" + " " + html_path + "/"
                    try:
                            output = subprocess.call(ishomavpic, shell=True)
                    except:
                            print "error moving ismip hom av 80km png file to www directory"
                            sys.exit(1)
                            raise

# formulate ismip a 80 velocity norm plot
            ishomavel_plotfile=''+ ncl_path + '/ismipa80vel.ncl'
            stockPIC ='STOCKPIC = addfile(\"'+ job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc\", \"r\")'
            stockJFNK ='STOCKJFNK = addfile(\"'+ job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc\", \"r\")'
            VARPIC  ='VARPIC = addfile(\"' + job_path + '/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc\", \"r\")'
            VARJFNK  ='VARJFNK = addfile(\"' + job_path + '/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc\", \"r\")'
            png  = 'PNG = "' + ncl_path + '/ismipavel"'
            plot_ishomavel = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" + png + "' " + ishomavel_plotfile + " >& plot_details.out"

#TODO create an iteration plot and have that also in the html file 
            try:
                    output = subprocess.call(plot_ishomavel, shell=True)
                    print "creating ismip hom a velocity norm plots"
            except:
                    print "error creating ncl ismip hom a vel norm plots"
                    raise

# delete old ismipa80 velnorm pic in www file

            if (html_path + '/ismipavel.png'):
                    ismipavelmove = "rm -f " + html_path + '/ismipavel.png'
                    try:
                            output = subprocess.call(ismipavelmove, shell=True)
                    except:
                            print "error removing old ismip a vel norm png file from www directory"
                            sys.exit(1)
                            raise

# transferring ismip a velocity norm pic to www file

            if (ncl_path + '/ismipavel.png'): 
                    ishomavelpic = "mv -f " + ncl_path + "/ismipavel.png" + " " + html_path + "/"
                    try:
                            output = subprocess.call(ishomavelpic, shell=True)
                    except:
                            print "error moving ismip hom a velocity 80km png file to www directory"
                            sys.exit(1)
                            raise

# formulate ismip a 80 thickness norm plot
            ishomathk_plotfile=''+ ncl_path + '/ismipa80thk.ncl'
            stockPIC ='STOCKPIC = addfile(\"'+ job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc\", \"r\")'
            stockJFNK ='STOCKJFNK = addfile(\"'+ job_path + '/bench/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc\", \"r\")'
            VARPIC  ='VARPIC = addfile(\"' + job_path + '/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc\", \"r\")'
            VARJFNK  ='VARJFNK = addfile(\"' + job_path + '/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc\", \"r\")'
            png  = 'PNG = "' + ncl_path + '/ismipathk"'
            plot_ishomathk = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" + png + "' " + ishomathk_plotfile + " >& plot_details.out"

#TODO create an iteration plot and have that also in the html file 
            try:
                    output = subprocess.call(plot_ishomathk, shell=True)
                    print "creating ismip hom a thickness plots"
            except:
                    print "error creating ncl ismip hom a thickness plots"
                    raise

# delete old ismipa80 thk pic in www file

            if (html_path + '/ismipathk.png'):
                    ismipathkmove = "rm -f " + html_path + '/ismipathk.png'
                    try:
                            output = subprocess.call(ismipathkmove, shell=True)
                    except:
                            print "error removing old ismip a thickness png file from www directory"
                            sys.exit(1)
                            raise

# transferring ismip a thickness norm pic to www file

            if (ncl_path + '/ismipathk.png'): 
                    ishomathkpic = "mv -f " + ncl_path + "/ismipathk.png" + " " + html_path + "/"
                    try:
                            output = subprocess.call(ishomathkpic, shell=True)
                    except:
                            print "error moving ismip hom a thickness 80km png file to www directory"
                            sys.exit(1)
                            raise

# remove plot_details.out
#            if (script_path + '/plot_details.out'):
#                    cleantrash = "rm -f " + script_path + "/plot_details.out"
#                    try:
#                            output = subprocess.call(cleantrash, shell=True)
#                    except:
#                            print "error removing plot_details.out"
#                            sys.exit(1)
#                            raise

        plot_file.write('<HTML>\n')
        plot_file.write('<TITLE>ISMIP HOM A 80km </TITLE>\n')
        plot_file.write('<TABLE>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<H4>Difference from benchmark run for U Velocity, V Velocity, Velocity Norm, and Thickness</H4>\n')
        plot_file.write('<BR>\n')
        plot_file.write('<OBJECT data="ismipau.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 80km Plots">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<OBJECT data="ismipav.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 80km Plots">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<OBJECT data="ismipavel.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 80km Plots">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<OBJECT data="ismipathk.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 80km Plots">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<BR>\n')
        plot_file.write('</TABLE>\n')
        plot_file.write('</HTML>\n')
        plot_file.close()

def c80plot(plot_file,job_path,ncl_path,html_path,script_path):  # using data, fill the web page with info

        noplot = 0    

        tmpath = job_path + '/ismip-hom-c/80km/data/ishom.c.80km.JFNK.out.nc'
        if VV_utilities.emptycheck(tmpath) == 0:
                noplot = 1
     #           return

        if noplot == 0:
        
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
            plot_ishomcu = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" + png + "' " + ishomcu_plotfile + " >& plot_details.out"

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
            plot_ishomcv = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" + png + "' " + ishomcv_plotfile + " >& plot_details.out"

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
            plot_ishomcvel = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" + png + "' " + ishomcvel_plotfile + " >& plot_details.out"

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
            plot_ishomcthk = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" + png + "' " + ishomcthk_plotfile + " >& plot_details.out"

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
#            if (script_path + '/plot_details.out'):
#                    cleantrash = "rm -f " + script_path + "/plot_details.out"
#                    try:
#                            output = subprocess.call(cleantrash, shell=True)
#                    except:
#                            print "error removing plot_details.out"
#                            sys.exit(1)
#                            raise

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



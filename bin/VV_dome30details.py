#!/usr/bin/env

import sys
import os
from optparse import OptionParser
import subprocess
import collections
import VV_outprocess
import VV_utilities
import VV_checks

# nomenclature for solver iteration values (1) d=dome, (2) d=diagnostic or e=evolving, (3) 30= size, 
# (4) 1,4,9,15 = processor count (5) b = bench if benchmark

failedt_list = []

def ddetails(solver_file,job_path,ncl_path,data_path,target_html):  # using data, fill the web page with info
        
        failedt_list = []
	solver_file.write('<HTML>\n')
	solver_file.write('<H3>Diagnostic Dome 30 Iteration Count Details:</H3>')
	solver_file.write('<BR> \n')

# JFNK gnu 1 proc

# failure checkin
        failedt1 = VV_checks.failcheck(job_path, '/dome30/diagnostic/data/gnu.JFNK.1proc')
        failedt_list.append(failedt1)

	solver_file.write('<H4>New Run: gnu.JFNK.1proc</H4>')
	procttl_dd301, nonlist_dd301,avg2_dd301,out_flag_dd301,ndd301_name,ldd301_name = VV_outprocess.jobprocess(job_path + '/dome30/diagnostic/data/gnu.JFNK.1proc', 'domed301')
	solver_file.write("Number of Processors = " + str(procttl_dd301[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
        VV_utilities.format(solver_file, nonlist_dd301)
	solver_file.write('<BR>\n')
	
        if out_flag_dd301 == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
        VV_utilities.format(solver_file, avg2_dd301)
	solver_file.write('<BR> \n')

	solver_file.write('<H4>Benchmark Run: gnu.JFNK.1proc</H4>')
	procttl_dd301b, nonlist_dd301b,avg2_dd301b,out_flag_dd301b,ndd301b_name,ldd301b_name = VV_outprocess.jobprocess(job_path + '/bench/dome30/diagnostic/data/gnu.JFNK.1proc', 'domed301b')

	solver_file.write("Number of Processors = " + str(procttl_dd301b[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_dd301b)
        solver_file.write('<BR>\n')
	
        if out_flag_dd301b == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_dd301b)
        solver_file.write('<BR> \n')

# JFNK gnu 4 proc

# Failure checking
        failedt2 = VV_checks.failcheck(job_path, '/dome30/diagnostic/data/gnu.JFNK.4proc')
        failedt_list.append(failedt2)
	solver_file.write('<H4>New Run: gnu.JFNK.4proc</H4>')
	procttl_dd304, nonlist_dd304,avg2_dd304,out_flag_dd304,ndd304_name,ldd304_name = VV_outprocess.jobprocess(job_path + '/dome30/diagnostic/data/gnu.JFNK.4proc','domed304')

	solver_file.write("Number of Processors = " + str(procttl_dd304[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_dd304)
        solver_file.write('<BR>\n')
	
        if out_flag_dd304 == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) THAT FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_dd304)
        solver_file.write('<BR> \n')

	solver_file.write('<H4>Benchmark Run: gnu.JFNK.4proc</H4>')
	procttl_dd304b, nonlist_dd304b,avg2_dd304b,out_flag_dd304b,ndd304b_name,ldd304b_name = VV_outprocess.jobprocess(job_path + '/bench/dome30/diagnostic/data/gnu.JFNK.4proc','domed304b')

	solver_file.write("Number of Processors = " + str(procttl_dd304b[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_dd304b)
        solver_file.write('<BR>\n')
	
        if out_flag_dd304b == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) THAT FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_dd304b)
        solver_file.write('<BR> \n')

        if 1 in failedt_list:
            failedt = 1
        else:
            failedt = 0

        return failedt

def edetails(solver_file,job_path,ncl_path,data_path,target_html):  # using data, fill the web page with info

	solver_file.write('<HTML>\n')
	solver_file.write('<H3>Evolving Dome 30 Iteration Count Details:</H3>')

	solver_file.write('<BR> \n')
# JFNK gnu 9 proc

# Failure checking
        failedt1 = VV_checks.failcheck(job_path, '/dome30/evolving/data/gnu.JFNK.9proc')
        failedt_list.append(failedt1)

#	print job_path + '/dome30/evolving/data/gnu.JFNK.1proc'
	procttl_de309, nonlist_de309,avg2_de309,out_flag_de309,nde309_name,lde309_name = VV_outprocess.jobprocess(job_path + '/dome30/evolving/data/gnu.JFNK.9proc', 'domee309')

	procttl_de309b, nonlist_de309b,avg2_de309b,out_flag_de309b,nde309b_name,lde309b_name = VV_outprocess.jobprocess(job_path + '/bench/dome30/evolving/data/gnu.JFNK.9proc', 'domee309b')

        solver_file.write('<TR>\n')
        solver_file.write('<BR>\n')

# JFNK gnu 9 proc
	solver_file.write('<H4>New Run: gnu.JFNK.9proc</H4>')

	solver_file.write("Number of Processors = " + str(procttl_de309[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_de309)
        solver_file.write('<BR>\n')
	
        if out_flag_de309 == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_de309)
        solver_file.write('<BR> \n')

	solver_file.write('<H4>Benchmark Run: gnu.JFNK.9proc</H4>')

	solver_file.write("Number of Processors = " + str(procttl_de309b[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_de309b)
        solver_file.write('<BR>\n')
	
        if out_flag_de309b == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_de309b)
        solver_file.write('<BR> \n')

# JFNK gnu 15 proc

# Failure checking
        failedt2 = VV_checks.failcheck(job_path, '/dome30/evolving/data/gnu.JFNK.15proc')
        failedt_list.append(failedt2)

        solver_file.write('<H4>New Run: gnu.JFNK.15proc</H4>')
	procttl_de3015, nonlist_de3015,avg2_de3015,out_flag_de3015,nde3015_name,lde3015_name = VV_outprocess.jobprocess(job_path + '/dome30/evolving/data/gnu.JFNK.15proc', 'domee3015')

	solver_file.write("Number of Processors = " + str(procttl_de3015[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_de3015)
        solver_file.write('<BR>\n')

	if out_flag_de3015 == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_de3015)
        solver_file.write('<BR> \n')

	solver_file.write('<H4>Benchmark Run: gnu.JFNK.15proc</H4>')
	procttl_de3015b, nonlist_de3015b,avg2_de3015b,out_flag_de3015b,nde3015b_name,lde3015b_name = VV_outprocess.jobprocess(job_path + '/bench/dome30/evolving/data/gnu.JFNK.15proc', 'domee3015b')

	solver_file.write("Number of Processors = " + str(procttl_de3015b[-1]) + "<BR>\n")
	solver_file.write("Number of Nonlinear Iterations = ")
	VV_utilities.format(solver_file, nonlist_de3015b)
        solver_file.write('<BR>\n')

	if out_flag_de3015b == 1:
		solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
	solver_file.write("Average Number of Linear Iterations per Time-Step = ")
	VV_utilities.format(solver_file, avg2_de3015b)
        solver_file.write('<BR> <BR>\n')

	solver_file.write('</HTML>\n')
	solver_file.close()

        if 1 in failedt_list:
            failedt = 1
        else:
            failedt = 0

	return failedt

def dplot(plot_file,job_path,ncl_path,html_path,script_path):  # using data, fill the web page with info

	plot_file.write('<HTML>\n')
	plot_file.write('<H3>Diagnostic Dome 30 Plot Details:</H3>')
	
# creating dome 30d velocity plot
        dome30dvel_plotfile=''+ ncl_path + '/dome30dvel.ncl'
	stockout='STOCKout = addfile(\"'+ job_path + '/bench/dome30/diagnostic/data/dome.out.nc\", \"r\")'
	stock1='STOCK1 = addfile(\"'+ job_path + '/bench/dome30/diagnostic/data/dome.1.nc\", \"r\")'
	stock4='STOCK4 = addfile(\"'+ job_path + '/bench/dome30/diagnostic/data/dome.4.nc\", \"r\")'
	VARout='VARout = addfile(\"'+ job_path + '/dome30/diagnostic/data/dome.out.nc\", \"r\")'
	VAR1  ='VAR1 = addfile(\"' + job_path + '/dome30/diagnostic/data/dome.1.nc\", \"r\")'
	VAR4  ='VAR4 = addfile(\"' + job_path + '/dome30/diagnostic/data/dome.4.nc\", \"r\")'
	png  = 'PNG = "' + ncl_path + '/dome30dvel"'
        plot_dome30dvel = "ncl '" + stockout + "'  '" + stock1 + "'  '" + stock4 + "'  '" + VARout + "'  '" + VAR1 + "' '" + VAR4 + \
                           "' '" + png + "' " + dome30dvel_plotfile 
        try:
                output = subprocess.call(plot_dome30dvel, shell=True)
                print "creating diagnotic dome 30 velocity plots"
        except:
                print "error creating ncl diagnostic dome30 velocity plots"
                raise

# delete old dome30 pic in www file

        if (html_path + '/dome30dvel.png'):
            dome30dvelmove = "rm -f " + html_path + '/dome30dvel.png'
            try:
                    output = subprocess.call(dome30dvelmove, shell=True)
            except:
                    print "error removing old diagnostic dome30 velocity png file from www directory"
                    sys.exit(1)
                    raise

# transferring new dome30 pic to www file

        if (ncl_path + '/dome30dvel.png'):
        	dome30dvelpic = "mv -f " + ncl_path + "/dome30dvel.png" + " " + html_path + "/"
        	try:
                	output = subprocess.call(dome30dvelpic, shell=True)
        	except:
                	print "error moving diagnostic dome30 velocity png file to www directory"
                        sys.exit(1)
                	raise

# creating dome 30d thickness plot
	dome30dthk_plotfile=''+ ncl_path + '/dome30dthk.ncl'
	stockout='STOCKout = addfile(\"'+ job_path + '/bench/dome30/diagnostic/data/dome.out.nc\", \"r\")'
	stock1='STOCK1 = addfile(\"'+ job_path + '/bench/dome30/diagnostic/data/dome.1.nc\", \"r\")'
	stock4='STOCK4 = addfile(\"'+ job_path + '/bench/dome30/diagnostic/data/dome.4.nc\", \"r\")'
	VARout='VARout = addfile(\"'+ job_path + '/dome30/diagnostic/data/dome.out.nc\", \"r\")'
	VAR1  ='VAR1 = addfile(\"' + job_path + '/dome30/diagnostic/data/dome.1.nc\", \"r\")'
	VAR4  ='VAR4 = addfile(\"' + job_path + '/dome30/diagnostic/data/dome.4.nc\", \"r\")'
	png  = 'PNG = "' + ncl_path + '/dome30dthk"'
        plot_dome30dthk = "ncl '" + stockout + "'  '" + stock1 + "'  '" + stock4 + "'  '" + VARout + "'  '" + VAR1 + "' '" + VAR4 + \
                           "' '" + png + "' " + dome30dthk_plotfile 
        try:
                output = subprocess.call(plot_dome30dthk, shell=True)
                print "creating diagnostic dome30 thickness plots"
        except:
                print "error creating ncl diagnostic dome30 thickness plots"
                raise

# delete old dome30 pic in www file

        if (html_path + '/dome30dthk.png'):
            dome30dthkmove = "rm -f " + html_path + '/dome30dthk.png'
            try:
                    output = subprocess.call(dome30dthkmove, shell=True)
            except:
                    print "error removing old diagnostic dome30 thickness png file from www directory"
                    sys.exit(1)
                    raise

# transferring dome30 pic to www file

        if (ncl_path + '/dome30dthk.png'):
        	dome30dthkpic = "mv -f " + ncl_path + "/dome30dthk.png" + " " + html_path + "/"
        	try:
                	output = subprocess.call(dome30dthkpic, shell=True)
        	except:
                	print "error moving diagnostic dome30 thickness png file to www directory"
                        sys.exit(1)
                	raise

# remove plot_details.out
        if (script_path + '/plot_details.out'):
                cleantrash = "rm -f " + script_path + "/plot_details.out"
                try:
                        output = subprocess.call(cleantrash, shell=True)
                except:
                        print "error removing plot_details.out"
                        sys.exit(1)
                        raise

        plot_file.write('<HTML>\n')
        plot_file.write('<TITLE>Diagnostic Dome 30 </TITLE>\n')
        plot_file.write('<TABLE>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<H4>Difference from Benchmark for 1 and 4 Processors, Velocity Norm and Thickness </H4>\n')
        plot_file.write('<OBJECT data="dome30dvel.png" type="image/png" width="1100" height="800" hspace=5 align=left alt="Dome 30 Plots">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<OBJECT data="dome30dthk.png" type="image/png" width="1100" height="800" hspace=5 align=left alt="Dome 30 Plots">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<BR>\n')
        plot_file.write('</TABLE>\n')
	plot_file.write('</HTML>\n')
	plot_file.close()

def eplot(plot_file,job_path,ncl_path,html_path,script_path):  # using data, fill the web page with info

	plot_file.write('<HTML>\n')
	plot_file.write('<H3>Evolving Dome 30 Plot Details:</H3>')

        
# creating dome 30e velocity plot
        dome30evel_plotfile=''+ ncl_path + '/dome30evel.ncl'
#	stockout='STOCKout = addfile(\"'+ job_path + '/bench/dome30/evolving/data/dome.out.nc\", \"r\")'
	stock9='STOCK9 = addfile(\"'+ job_path + '/bench/dome30/evolving/data/dome.9.nc\", \"r\")'
	stock15='STOCK15 = addfile(\"'+ job_path + '/bench/dome30/evolving/data/dome.15.nc\", \"r\")'
#	VARout='VARout = addfile(\"'+ job_path + '/dome30/evolving/data/dome.out.nc\", \"r\")'
	VAR9  ='VAR9 = addfile(\"' + job_path + '/dome30/evolving/data/dome.9.nc\", \"r\")'
	VAR15  ='VAR15 = addfile(\"' + job_path + '/dome30/evolving/data/dome.15.nc\", \"r\")'
	png  = 'PNG = "' + ncl_path + '/dome30evel"'
#        plot_dome30evel = "ncl '" + stockout + "'  '" + stock9 + "'  '" + stock15 + "'  '" + VARout + "'  '" + VAR9 + "' '" + VAR15 + \
#                           "' '" + png + "' " + dome30evel_plotfile + " >& plot_details.out" 
        plot_dome30evel = "ncl '" + stock9 + "'  '" + stock15 + "'  '" + VAR9 + "' '" + VAR15 + \
                           "' '" + png + "' " + dome30evel_plotfile 
        try:
                output = subprocess.call(plot_dome30evel, shell=True)
                print "creating evolving dome30 velocity plots"
        except:
                print "error creating ncl evolving dome30 velocity plots"
                raise

# delete old dome30 pic in www file

        if (html_path + '/dome30evel.png'):
            dome30evelmove = "rm -f " + html_path + '/dome30evel.png'
            try:
                    output = subprocess.call(dome30evelmove, shell=True)
            except:
                    print "error removing old evolving dome30 velocity png file from www directory"
                    sys.exit(1)
                    raise

# transferring dome30 pic to www file

        if (ncl_path + '/dome30evel.png'):
        	dome30evelpic = "mv -f " + ncl_path + "/dome30evel.png" + " " + html_path + "/"
        	try:
                	output = subprocess.call(dome30evelpic, shell=True)
        	except:
                	print "error moving evolving dome30 velocity png file to www directory"
                        sys.exit(1)
                	raise

# creating dome 30e thickness plot
        dome30ethk_plotfile=''+ ncl_path + '/dome30ethk.ncl'
#	stockout='STOCKout = addfile(\"'+ job_path + '/bench/dome30/evolving/data/dome.out.nc\", \"r\")'
	stock9='STOCK9 = addfile(\"'+ job_path + '/bench/dome30/evolving/data/dome.9.nc\", \"r\")'
	stock15='STOCK15 = addfile(\"'+ job_path + '/bench/dome30/evolving/data/dome.15.nc\", \"r\")'
#	VARout='VARout = addfile(\"'+ job_path + '/dome30/evolving/data/dome.out.nc\", \"r\")'
	VAR9  ='VAR9 = addfile(\"' + job_path + '/dome30/evolving/data/dome.9.nc\", \"r\")'
	VAR15  ='VAR15 = addfile(\"' + job_path + '/dome30/evolving/data/dome.15.nc\", \"r\")'
	png  = 'PNG = "' + ncl_path + '/dome30ethk"'
#        plot_dome30ethk = "ncl '" + stockout + "'  '" + stock9 + "'  '" + stock15 + "'  '" + VARout + "'  '" + VAR9 + "' '" + VAR15 + \
#                           "' '" + png + "' " + dome30ethk_plotfile + " >& plot_details.out"
        plot_dome30ethk = "ncl '" + stock9 + "'  '" + stock15 + "'  '" + VAR9 + "' '" + VAR15 + \
                           "' '" + png + "' " + dome30ethk_plotfile
        try:
                output = subprocess.call(plot_dome30ethk, shell=True)
                print "creating evolving dome30 thickness plots"
        except:
                print "error creating ncl evolving dome30 thickness plots"
                raise

# delete old dome30 pic in www file

        if (html_path + '/dome30ethk.png'):
            dome30ethkmove = "rm -f " + html_path + '/dome30ethk.png'
            try:
                    output = subprocess.call(dome30ethkmove, shell=True)
            except:
                    print "error removing old evolving dome30 thickness png file from www directory"
                    sys.exit(1)
                    raise

# transferring dome30 pic to www file

        if (ncl_path + '/dome30ethk.png'):
        	dome30ethkpic = "mv -f " + ncl_path + "/dome30ethk.png" + " " + html_path + "/"
        	try:
                	output = subprocess.call(dome30ethkpic, shell=True)
        	except:
                	print "error moving evolving dome30 thickness png file to www directory"
                        sys.exit(1)
                	raise

# remove plot_details.out
        if (script_path + '/plot_details.out'):
                cleantrash = "rm -f " + script_path + "/plot_details.out"
                try:
                        output = subprocess.call(cleantrash, shell=True)
                except:
                        print "error removing plot_details.out"
                        sys.exit(1)
                        raise

        plot_file.write('<HTML>\n')
        plot_file.write('<TITLE>Evolving Dome 30 </TITLE>\n')
        plot_file.write('<TABLE>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<H4>Difference from Benchmark for 9 and 15 Processors, Velocity Norm and Thickness </H4>\n')
        plot_file.write('<OBJECT data="dome30evel.png" type="image/png" width="1100" height="800" hspace=5 align=left alt="Evolving Dome 30 Velocity and Thickness Plots">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<OBJECT data="dome30ethk.png" type="image/png" width="1100" height="800" hspace=5 align=left alt="Evolving Dome 30 Velocity and Thickness Plots">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<BR>\n')
        plot_file.write('</TABLE>\n')
	plot_file.write('</HTML>\n')
	plot_file.close()


#!/usr/bin/env

import sys
import os
from optparse import OptionParser
import subprocess
import collections
import VV_outprocess
import VV_utilities
import VV_checks

def circdetails(solver_file,job_path):  # using data, fill the web page with info

        failedt_list = []
	solver_file.write('<HTML>\n')
	solver_file.write('<H3>Circular Shelf Iteration Count Details:</H3>')
	solver_file.write('<H4>Eventually published in plot form</H4>')
	solver_file.write('<BR> \n')

# JFNK 2 proc

# Failure checking
        failedt1 = VV_checks.failcheck(job_path, '/circular-shelf/data/circular-shelf.out')
        failedt_list.append(failedt1)

        solver_file.write('<H4>New Run: circular-shelf.out</H4>')
        procttl_circd, nonlist_circd, avg2_circd, out_flag_circd, ndcirc_name, ldcirc_name = VV_outprocess.jobprocess(job_path + '/circular-shelf/data/circular-shelf.out','circ')

        solver_file.write("Number of Processors = " + str(procttl_circd[-1]) + "<BR>\n")
        solver_file.write("Number of Nonlinear Iterations = ")
        VV_utilities.format(solver_file, nonlist_circd)
        solver_file.write('<BR>\n')
        if out_flag_circd == 1:
                solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
        solver_file.write("Average Number of Linear Iterations per Time-Step = ")
        VV_utilities.format(solver_file, avg2_circd)
        solver_file.write('<BR> \n')

        solver_file.write('<H4>Benchmark Run: circular-shelf.out</H4>')
        procttl_circb, nonlist_circb, avg2_circb, out_flag_circb, ndcircb_name, ldcircb_name = VV_outprocess.jobprocess(job_path + '/bench/circular-shelf/data/circular-shelf.out','circb')

        solver_file.write("Number of Processors = " + str(procttl_circb[-1]) + "<BR>\n")
        solver_file.write("Number of Nonlinear Iterations = ")
        VV_utilities.format(solver_file, nonlist_circb)
        solver_file.write('<BR>\n')
        if out_flag_circb == 1:
                solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
        solver_file.write("Average Number of Linear Iterations per Time-Step = ")
        VV_utilities.format(solver_file, avg2_circb)
        solver_file.write('<BR> \n')

        if 1 in failedt_list:
            failedt = 1
        else:
            failedt = 0

        return failedt
# TODO have jobprocess grab picard solver info as well

def confdetails(solver_file,job_path):  # using data, fill the web page with info

        failedt_list = []

	solver_file.write('<HTML>\n')
	solver_file.write('<H3>Confined Shelf Iteration Count Details:</H3>')
	solver_file.write('<H4>Eventually published in plot form</H4>')
	solver_file.write('<BR> \n')

# JFNK 2 proc
        
# Failure checking
        failedt1 = VV_checks.failcheck(job_path, '/confined-shelf/data/confined-shelf.out')
        failedt_list.append(failedt1)

        solver_file.write('<H4>New Run: confined-shelf.out</H4>')
        procttl_confd, nonlist_confd, avg2_confd, out_flag_confd, ndconf_name, ldconf_name = VV_outprocess.jobprocess(job_path + '/confined-shelf/data/confined-shelf.out', 'conf')

        solver_file.write("Number of Processors = " + str(procttl_confd[-1]) + "<BR>\n")
        solver_file.write("Number of Nonlinear Iterations = ")
        VV_utilities.format(solver_file, nonlist_confd)
        solver_file.write('<BR>\n')
        if out_flag_confd == 1:
                solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
        solver_file.write("Average Number of Linear Iterations per Time-Step = ")
        VV_utilities.format(solver_file, avg2_confd)
        solver_file.write('<BR> \n')

        solver_file.write('<H4>Benchmark Run: confined-shelf.out</H4>')
        procttl_confb, nonlist_confb, avg2_confb, out_flag_confb, ndconfb_name, ldconfb_name = VV_outprocess.jobprocess(job_path + '/bench/confined-shelf/data/confined-shelf.out','confb')

        solver_file.write("Number of Processors = " + str(procttl_confb[-1]) + "<BR>\n")
        solver_file.write("Number of Nonlinear Iterations = ")
        VV_utilities.format(solver_file, nonlist_confb)
        solver_file.write('<BR>\n')
        if out_flag_confb == 1:
                solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
        solver_file.write("Average Number of Linear Iterations per Time-Step = ")
        VV_utilities.format(solver_file, avg2_confb)
        solver_file.write('<BR> \n')

	solver_file.write('</HTML>\n')
	solver_file.close()

        if 1 in failedt_list:
            failedt = 1
        else:
            failedt = 0
        
        return failedt

def circplot(plot_file,job_path,ncl_path,html_path,script_path):  # using data, fill the web page with info

	plot_file.write('<HTML>\n')
	plot_file.write('<H3>Circular Shelf Plot Details:</H3>')

# creating circular shelf velocity plot 
        circvel_plotfile=''+ ncl_path + '/circshelfvel.ncl'
	stockPIC='STOCKPIC = addfile(\"'+ job_path + '/bench/circular-shelf/data/circular-shelf.gnu.PIC.nc\", \"r\")'
	stockJFNK='STOCKJFNK = addfile(\"'+ job_path + '/bench/circular-shelf/data/circular-shelf.gnu.JFNK.nc\", \"r\")'
	VARPIC  ='VARPIC = addfile(\"' + job_path + '/circular-shelf/data/circular-shelf.gnu.PIC.nc\", \"r\")'
	VARJFNK  ='VARJFNK = addfile(\"' + job_path + '/circular-shelf/data/circular-shelf.gnu.JFNK.nc\", \"r\")'
	png  = 'PNG = "' + ncl_path + '/circshelfvel.png"'
        plot_circvel = "ncl '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARPIC + "' '" + VARJFNK + "' '" + png + "' " + circvel_plotfile + " >& plot_details.out"

#TODO create an iteration plot and have that also in the html file 
        try:
                output = subprocess.call(plot_circvel, shell=True)
                print "creating circular shelf velocity plots"
        except:
                print "error creating ncl circular shelf velocity plot"
                raise

# delete old circvel pic in www file

        if (html_path + '/circshelfvel.png'):
                circvelmove = "rm -f " + html_path + '/circshelfvel.png'
                try:
                        output = subprocess.call(circvelmove, shell=True)
                except:
                        print "error removing old circular shelf velocity png file from www directory"
                        sys.exit(1)
                        raise

# transferring circvel pic to www file

        if (ncl_path + '/circshelfvel.png'):
        	circvelpic = "mv -f " + ncl_path + "/circshelfvel.png" + " " + html_path + "/"
        	try:
                	output = subprocess.call(circvelpic, shell=True)
        	except:
                	print "error moving circular velocity shelf png file to www directory"
                        sys.exit(1)
                	raise

# creating circular shelf thickness plot 
        circthk_plotfile=''+ ncl_path + '/circshelfthk.ncl'
	stockPIC='STOCKPIC = addfile(\"'+ job_path + '/bench/circular-shelf/data/circular-shelf.gnu.PIC.nc\", \"r\")'
	stockJFNK='STOCKJFNK = addfile(\"'+ job_path + '/bench/circular-shelf/data/circular-shelf.gnu.JFNK.nc\", \"r\")'
	VARPIC  ='VARPIC = addfile(\"' + job_path + '/circular-shelf/data/circular-shelf.gnu.PIC.nc\", \"r\")'
	VARJFNK  ='VARJFNK = addfile(\"' + job_path + '/circular-shelf/data/circular-shelf.gnu.JFNK.nc\", \"r\")'
	png  = 'PNG = "' + ncl_path + '/circshelfthk.png"'
        plot_circthk = "ncl '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARPIC + "' '" + VARJFNK + "' '" + png + "' " + circthk_plotfile + " >& plot_details.out"

#TODO create an iteration plot and have that also in the html file 
        try:
                output = subprocess.call(plot_circthk, shell=True)
                print "creating circular shelf thickness plots"
        except:
                print "error creating ncl circular shelf thickness plot"
                raise

# delete old circthk pic in www file

        if (html_path + '/circshelfthk.png'):
                circthkmove = "rm -f " + html_path + '/circshelfthk.png'
                try:
                        output = subprocess.call(circthkmove, shell=True)
                except:
                        print "error removing old circular shelf thickness png file from www directory"
                        sys.exit(1)
                        raise

# transferring circthk pic to www file

        if (ncl_path + '/circshelfthk.png'):
        	circthkpic = "mv -f " + ncl_path + "/circshelfthk.png" + " " + html_path + "/"
        	try:
                	output = subprocess.call(circthkpic, shell=True)
        	except:
                	print "error moving circular thickness shelf png file to www directory"
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
        plot_file.write('<TITLE>Circular Shelf </TITLE>\n')
        plot_file.write('<TABLE>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<H4>Difference from Benchmark for Velocity Norm and Thickness</H4>\n')
        plot_file.write('<OBJECT data="circshelfvel.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="Circular Shelf Plots PNG">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<OBJECT data="circshelfthk.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="Circular Shelf Plots PNG">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<BR>\n')
        plot_file.write('</TABLE>\n')
	plot_file.write('</HTML>\n')
	plot_file.close()

def confplot(plot_file,job_path,ncl_path,html_path,script_path):  # using data, fill the web page with info

        plot_file.write('<HTML>\n')
	plot_file.write('<H3>Confined Shelf Plot Details:</H3>')

# creating confined shelf velocity plot 
        confvel_plotfile=''+ ncl_path + '/confshelfvel.ncl'
	stockPIC='STOCKPIC = addfile(\"'+ job_path + '/bench/confined-shelf/data/confined-shelf.gnu.PIC.nc\", \"r\")'
	stockJFNK='STOCKJFNK = addfile(\"'+ job_path + '/bench/confined-shelf/data/confined-shelf.gnu.JFNK.nc\", \"r\")'
	VARPIC  ='VARPIC = addfile(\"' + job_path + '/confined-shelf/data/confined-shelf.gnu.PIC.nc\", \"r\")'
	VARJFNK  ='VARJFNK = addfile(\"' + job_path + '/confined-shelf/data/confined-shelf.gnu.JFNK.nc\", \"r\")'
	png  = 'PNG = "' + ncl_path + '/confshelfvel.png"'
        plot_confvel = "ncl '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARPIC + "' '" + VARJFNK + "' '" + png + "' " + confvel_plotfile + " >& plot_details.out"

#TODO create an iteration plot and have that also in the html file 
        try:
                output = subprocess.call(plot_confvel, shell=True)
                print "creating confined shelf velocity plots"
        except:
                print "error creating ncl confined shelf velocity plot"
                raise

# delete old confvel pic in www file

        if (html_path + '/confshelfvel.png'):
                confvelmove = "rm -f " + html_path + '/confshelfvel.png'
                try:
                        output = subprocess.call(confvelmove, shell=True)
                except:
                        print "error removing old confined shelf velocity png file from www directory"
                        sys.exit(1)
                        raise

# transferring confvel pic to www file

        if (ncl_path + '/confshelfvel.png'):
        	confvelpic = "mv -f " + ncl_path + "/confshelfvel.png" + " " + html_path + "/"
        	try:
                	output = subprocess.call(confvelpic, shell=True)
        	except:
                	print "error moving confined velocity shelf png file to www directory"
                        sys.exit(1)
                	raise

# creating confined shelf thickness plot 
        confthk_plotfile=''+ ncl_path + '/confshelfthk.ncl'
	stockPIC='STOCKPIC = addfile(\"'+ job_path + '/bench/confined-shelf/data/confined-shelf.gnu.PIC.nc\", \"r\")'
	stockJFNK='STOCKJFNK = addfile(\"'+ job_path + '/bench/confined-shelf/data/confined-shelf.gnu.JFNK.nc\", \"r\")'
	VARPIC  ='VARPIC = addfile(\"' + job_path + '/confined-shelf/data/confined-shelf.gnu.PIC.nc\", \"r\")'
	VARJFNK  ='VARJFNK = addfile(\"' + job_path + '/confined-shelf/data/confined-shelf.gnu.JFNK.nc\", \"r\")'
	png  = 'PNG = "' + ncl_path + '/confshelfthk.png"'
        plot_confthk = "ncl '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARPIC + "' '" + VARJFNK + "' '" + png + "' " + confthk_plotfile + " >& plot_details.out"

#TODO create an iteration plot and have that also in the html file 
        try:
                output = subprocess.call(plot_confthk, shell=True)
                print "creating confined shelf thickness plots"
        except:
                print "error creating ncl confined shelf thickness plot"
                raise

# delete old confthk pic in www file

        if (html_path + '/confshelfthk.png'):
                confthkmove = "rm -f " + html_path + '/confshelfthk.png'
                try:
                        output = subprocess.call(confthkmove, shell=True)
                except:
                        print "error removing old confined shelf thickness png file from www directory"
                        sys.exit(1)
                        raise

# transferring circthk pic to www file

        if (ncl_path + '/confshelfthk.png'):
        	confthkpic = "mv -f " + ncl_path + "/confshelfthk.png" + " " + html_path + "/"
        	try:
                	output = subprocess.call(confthkpic, shell=True)
        	except:
                	print "error moving confined thickness shelf png file to www directory"
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
        plot_file.write('<TITLE>Confined Shelf </TITLE>\n')
        plot_file.write('<TABLE>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<H4>Difference from Benchmark for Velocity Norm and Thickness</H4>\n')
        plot_file.write('<OBJECT data="confshelfvel.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="Confined Shelf Plots PNG">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<OBJECT data="confshelfthk.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="Confined Shelf Plots PNG">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<BR>\n')
        plot_file.write('</TABLE>\n')

	plot_file.write('</HTML>\n')
	plot_file.close()

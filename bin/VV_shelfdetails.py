#!/usr/bin/env

import sys
import os
from optparse import OptionParser
import subprocess
import collections
import VV_outprocess
import VV_utilities
import VV_checks

def circdetails(solver_file,reg_test,data_dir):  # using data, fill the web page with info

        failedt_list = []
	solver_file.write('<HTML>\n')
	solver_file.write('<H3>Circular Shelf Iteration Count Details:</H3>')
	solver_file.write('<H4>Eventually published in plot form</H4>')
	solver_file.write('<BR> \n')

# JFNK 2 proc

# Failure checking
        failedt1 = VV_checks.failcheck(reg_test, '/circular-shelf/' + data_dir + '/circular-shelf.out')
        failedt_list.append(failedt1)

        solver_file.write('<H4>New Run: circular-shelf.out</H4>')
        procttl_circd, nonlist_circd, avg2_circd, out_flag_circd, ndcirc_name, ldcirc_name = VV_outprocess.jobprocess(reg_test + '/circular-shelf/' + data_dir + '/circular-shelf.out','circ')

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
        procttl_circb, nonlist_circb, avg2_circb, out_flag_circb, ndcircb_name, ldcircb_name = VV_outprocess.jobprocess(reg_test + '/bench/circular-shelf/' + data_dir + '/circular-shelf.out','circb')

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

def confdetails(solver_file,reg_test,data_dir):  # using data, fill the web page with info

        failedt_list = []

	solver_file.write('<HTML>\n')
	solver_file.write('<H3>Confined Shelf Iteration Count Details:</H3>')
	solver_file.write('<H4>Eventually published in plot form</H4>')
	solver_file.write('<BR> \n')

# JFNK 2 proc
        
# Failure checking
        failedt1 = VV_checks.failcheck(reg_test, '/confined-shelf/' + data_dir + '/confined-shelf.out')
        failedt_list.append(failedt1)

        solver_file.write('<H4>New Run: confined-shelf.out</H4>')
        procttl_confd, nonlist_confd, avg2_confd, out_flag_confd, ndconf_name, ldconf_name = VV_outprocess.jobprocess(reg_test + '/confined-shelf/' + data_dir + '/confined-shelf.out', 'conf')

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
        procttl_confb, nonlist_confb, avg2_confb, out_flag_confb, ndconfb_name, ldconfb_name = VV_outprocess.jobprocess(reg_test + '/bench/confined-shelf/' + data_dir + '/confined-shelf.out','confb')

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

def circplot(plot_file,reg_test,ncl_path,html_path,script_path,data_dir):  # using data, fill the web page with info

	plot_file.write('<HTML>\n')
	plot_file.write('<H3>Circular Shelf Plot Details:</H3>')

# creating circular shelf velocity plot 
        circvel_plotfile=''+ ncl_path + '/circshelfvel.ncl'
	stockPIC='STOCKPIC = addfile(\"'+ reg_test + '/bench/circular-shelf/' + data_dir + '/circular-shelf.gnu.PIC.nc\", \"r\")'
	stockJFNK='STOCKJFNK = addfile(\"'+ reg_test + '/bench/circular-shelf/' + data_dir + '/circular-shelf.gnu.JFNK.nc\", \"r\")'
	VARPIC  ='VARPIC = addfile(\"' + reg_test + '/circular-shelf/' + data_dir + '/circular-shelf.gnu.PIC.nc\", \"r\")'
	VARJFNK  ='VARJFNK = addfile(\"' + reg_test + '/circular-shelf/' + data_dir + '/circular-shelf.gnu.JFNK.nc\", \"r\")'
	png  = 'PNG = "' + ncl_path + '/circshelfvel.png"'
        plot_circvel = "ncl '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARPIC + "' '" + VARJFNK + "' '" + png + "' " + circvel_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
        try:
                subprocess.check_call(plot_circvel, shell=True)
                print "creating circular shelf velocity plots"
        except subprocess.CalledProcessError as e:
                print "There was a CalledProcessError with the error number: ", e.returncode
                print "There was a CalledProcessError when trying to run command: ", e.cmd
                exit(e.returncode)

# delete old circvel pic in www file

        if (html_path + '/circshelfvel.png'):
                circvelmove = "rm -f " + html_path + '/circshelfvel.png'
                try:
                        subprocess.check_call(circvelmove, shell=True)
                except subprocess.CalledProcessError as e:
                        print "There was a CalledProcessError with the error number: ", e.returncode
                        print "There was a CalledProcessError when trying to run command: ", e.cmd
                        exit(e.returncode)

# transferring circvel pic to www file

        if (ncl_path + '/circshelfvel.png'):
        	circvelpic = "mv -f " + ncl_path + "/circshelfvel.png" + " " + html_path + "/"
                try:
                        subprocess.check_call(circvelpic, shell=True)
                except subprocess.CalledProcessError as e:
                        print "There was a CalledProcessError with the error number: ", e.returncode
                        print "There was a CalledProcessError when trying to run command: ", e.cmd
                        exit(e.returncode)

# remove plot_details.out
#        if (script_path + '/plot_details.out'):
#                cleantrash = "rm -f " + script_path + "/plot_details.out"
#                try:
#                        subprocess.check_call(cleantrash, shell=True)
#                except subprocess.CalledProcessError as e:
#                        print "There was a CalledProcessError with the error number: ", e.returncode
#                        print "There was a CalledProcessError when trying to run command: ", e.cmd
#                        exit(e.returncode)

        plot_file.write('<HTML>\n')
        plot_file.write('<TITLE>Circular Shelf </TITLE>\n')
        plot_file.write('<TABLE>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<H4>Difference from Benchmark for Velocity Norm </H4>\n')
        plot_file.write('<OBJECT data="circshelfvel.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="Circular Shelf Plots PNG">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<BR>\n')
        plot_file.write('</TABLE>\n')
	plot_file.write('</HTML>\n')
	plot_file.close()

def confplot(plot_file,reg_test,ncl_path,html_path,script_path,data_dir):  # using data, fill the web page with info

        plot_file.write('<HTML>\n')
	plot_file.write('<H3>Confined Shelf Plot Details:</H3>')

# creating confined shelf velocity plot 
        confvel_plotfile=''+ ncl_path + '/confshelfvel.ncl'
	stockPIC='STOCKPIC = addfile(\"'+ reg_test + '/bench/confined-shelf/' + data_dir + '/confined-shelf.gnu.PIC.nc\", \"r\")'
	stockJFNK='STOCKJFNK = addfile(\"'+ reg_test + '/bench/confined-shelf/' + data_dir + '/confined-shelf.gnu.JFNK.nc\", \"r\")'
	VARPIC  ='VARPIC = addfile(\"' + reg_test + '/confined-shelf/' + data_dir + '/confined-shelf.gnu.PIC.nc\", \"r\")'
	VARJFNK  ='VARJFNK = addfile(\"' + reg_test + '/confined-shelf/' + data_dir + '/confined-shelf.gnu.JFNK.nc\", \"r\")'
	png  = 'PNG = "' + ncl_path + '/confshelfvel.png"'
        plot_confvel = "ncl '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARPIC + "' '" + VARJFNK + "' '" + png + "' " + confvel_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
        try:
                subprocess.check_call(plot_confvel, shell=True)
                print "creating confined shelf velocity plots"
        except subprocess.CalledProcessError as e:
                print "There was a CalledProcessError with the error number: ", e.returncode
                print "There was a CalledProcessError when trying to run command: ", e.cmd
                exit(e.returncode)

# delete old confvel pic in www file

        if (html_path + '/confshelfvel.png'):
                confvelmove = "rm -f " + html_path + '/confshelfvel.png'
                try:
                        subprocess.check_call(confvelmove, shell=True)
                except subprocess.CalledProcessError as e:
                        print "There was a CalledProcessError with the error number: ", e.returncode
                        print "There was a CalledProcessError when trying to run command: ", e.cmd
                        exit(e.returncode)

# transferring confvel pic to www file

        if (ncl_path + '/confshelfvel.png'):
        	confvelpic = "mv -f " + ncl_path + "/confshelfvel.png" + " " + html_path + "/"
                try:
                        subprocess.check_call(confvelpic, shell=True)
                except subprocess.CalledProcessError as e:
                        print "There was a CalledProcessError with the error number: ", e.returncode
                        print "There was a CalledProcessError when trying to run command: ", e.cmd
                        exit(e.returncode)

# remove plot_details.out
#        if (script_path + '/plot_details.out'):
#                cleantrash = "rm -f " + script_path + "/plot_details.out"
#                try:
#                        subprocess.check_call(cleantrash, shell=True)
#                except subprocess.CalledProcessError as e:
#                        print "There was a CalledProcessError with the error number: ", e.returncode
#                        print "There was a CalledProcessError when trying to run command: ", e.cmd
#                        exit(e.returncode)

        plot_file.write('<HTML>\n')
        plot_file.write('<TITLE>Confined Shelf </TITLE>\n')
        plot_file.write('<TABLE>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<H4>Difference from Benchmark for Velocity Norm </H4>\n')
        plot_file.write('<OBJECT data="confshelfvel.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="Confined Shelf Plots PNG">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<BR>\n')
        plot_file.write('</TABLE>\n')
	plot_file.write('</HTML>\n')
	plot_file.close()

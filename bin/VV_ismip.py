#!/usr/bin/env

import sys
import os
from optparse import OptionParser
import subprocess
import collections
import VV_outprocess
import VV_utilities
import VV_checks

def a80details(solver_file,reg_test,data_dir):  # using data, fill the web page with info

    failedt_list = []

    solver_file.write('<HTML>\n')
    solver_file.write('<BODY BGCOLOR="#CADFE0">\n')
    solver_file.write('<H3>ISMIP HOM A 80km Iteration Count Details:</H3>')
    solver_file.write('<BR> \n')
# JFNK gnu 1 proc

# Failure checking
    failedt1 = VV_checks.failcheck(reg_test, '/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.out.1')
    failedt_list.append(failedt1)

    procttl_ih1d, nonlist_ih1d, avg2_ih1d, out_flag_ih1d, ndiha1_name, ldiha1_name = \
        VV_outprocess.jobprocess(reg_test + '/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.out.1', 'imhoma1')    

    solver_file.write('<H4>New Run: ishom.a.80km.out.1</H4>')
    solver_file.write("Number of Processors = " + str(procttl_ih1d[-1]) + "<BR>\n")
    solver_file.write("Number of Nonlinear Iterations = ")
    VV_utilities.format(solver_file, nonlist_ih1d)
    solver_file.write('<BR>\n')
    
    if out_flag_ih1d == 1:
        solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
    solver_file.write("Average Number of Linear Iterations per Time-Step = ")
    VV_utilities.format(solver_file, avg2_ih1d)
    solver_file.write('<BR> \n')

    solver_file.write('<H4>Benchmark Run: ishom.a.80km.out.1</H4>')
    procttl_ih1b, nonlist_ih1b, avg2_ih1b, out_flag_ih1b, ndiha1b_name, ldiha1b_name = \
        VV_outprocess.jobprocess(reg_test + '/bench/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.out.1', 'imhoma1b')

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
                                              
# Failure checking
    failedt2 = VV_checks.failcheck(reg_test, '/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.out.2')
    failedt_list.append(failedt2)

    procttl_ih2d, nonlist_ih2d, avg2_ih2d, out_flag_ih2d, ndiha2_name, ldiha2_name = \
        VV_outprocess.jobprocess(reg_test + '/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.out.2','imhoma2')

    solver_file.write('<H4>New Run: ishom.a.80km.out.2</H4>')
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
    procttl_ih2b, nonlist_ih2b, avg2_ih2b, out_flag_ih2b, ndiha2b_name, ldiha2b_name = \
        VV_outprocess.jobprocess(reg_test + '/bench/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.out.2','imhoma2b')

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

# Failure checking
    failedt3 = VV_checks.failcheck(reg_test, '/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.out.4')
    failedt_list.append(failedt3)

    procttl_ih4d, nonlist_ih4d, avg2_ih4d, out_flag_ih4d, ndiha4_name, ldiha4_name = \
        VV_outprocess.jobprocess(reg_test + '/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.out.4','imhoma4')
    
    solver_file.write('<H4>New Run: ishom.a.80km.out.4</H4>')
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
    procttl_ih4b, nonlist_ih4b, avg2_ih4b, out_flag_ih4b, ndiha4b_name, ldiha4b_name = \
        VV_outprocess.jobprocess(reg_test + '/bench/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.out.4','imhoma4b')

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
def a20details(solver_file,reg_test,data_dir):  # using data, fill the web page with info

    failedt_list = []

    solver_file.write('<HTML>\n')
    solver_file.write('<BODY BGCOLOR="#CADFE0">\n')
    solver_file.write('<H3>ISMIP HOM A 20km Iteration Count Details:</H3>')
    solver_file.write('<BR> \n')
# JFNK gnu 1 proc

# Failure checking
    failedt1 = VV_checks.failcheck(reg_test, '/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.out.1')
    failedt_list.append(failedt1)

    procttl_ih1d, nonlist_ih1d, avg2_ih1d, out_flag_ih1d, ndiha1_name, ldiha1_name = \
        VV_outprocess.jobprocess(reg_test + '/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.out.1', 'imhoma1')
    
    solver_file.write('<H4>New Run: ishom.a.20km.out.1</H4>')
    solver_file.write("Number of Processors = " + str(procttl_ih1d[-1]) + "<BR>\n")
    solver_file.write("Number of Nonlinear Iterations = ")
    VV_utilities.format(solver_file, nonlist_ih1d)
    solver_file.write('<BR>\n')
    
    if out_flag_ih1d == 1:
        solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
    solver_file.write("Average Number of Linear Iterations per Time-Step = ")
    VV_utilities.format(solver_file, avg2_ih1d)
    solver_file.write('<BR> \n')

    solver_file.write('<H4>Benchmark Run: ishom.a.20km.out.1</H4>')
    procttl_ih1b, nonlist_ih1b, avg2_ih1b, out_flag_ih1b, ndiha1b_name, ldiha1b_name = \
        VV_outprocess.jobprocess(reg_test + '/bench/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.out.1', 'imhoma1b')

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
    failedt2 = VV_checks.failcheck(reg_test, '/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.out.2')
    failedt_list.append(failedt2)

    procttl_ih2d, nonlist_ih2d, avg2_ih2d, out_flag_ih2d, ndiha2_name, ldiha2_name = \
        VV_outprocess.jobprocess(reg_test + '/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.out.2','imhoma2')
    
    solver_file.write('<H4>New Run: ishom.a.20km.out.2</H4>')
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
    procttl_ih2b, nonlist_ih2b, avg2_ih2b, out_flag_ih2b, ndiha2b_name, ldiha2b_name = \
        VV_outprocess.jobprocess(reg_test + '/bench/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.out.2','imhoma2b')

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
    failedt3 = VV_checks.failcheck(reg_test, '/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.out.4')
    failedt_list.append(failedt3)

    procttl_ih4d, nonlist_ih4d, avg2_ih4d, out_flag_ih4d, ndiha4_name, ldiha4_name = \
        VV_outprocess.jobprocess(reg_test + '/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.out.4','imhoma4')

    solver_file.write('<H4>New Run: ishom.a.20km.out.4</H4>')
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
    procttl_ih4b, nonlist_ih4b, avg2_ih4b, out_flag_ih4b, ndiha4b_name, ldiha4b_name = \
        VV_outprocess.jobprocess(reg_test + '/bench/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.out.4','imhoma4b')

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
def c80details(solver_file,reg_test,data_dir):  # using data, fill the web page with info

    failedt_list = []

    solver_file.write('<HTML>\n')
    solver_file.write('<BODY BGCOLOR="#CADFE0">\n')
    solver_file.write('<H3>ISMIP HOM C 80KM Iteration Count Details:</H3>')
    solver_file.write('<BR> \n')

# JFNK gnu 1 proc

# Failure checking
    failedt1 = VV_checks.failcheck(reg_test, '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.out.1')
    failedt_list.append(failedt1)

    procttl_ih1d, nonlist_ih1d, avg2_ih1d, out_flag_ih1d, ndihc1_name, ldihc1_name = \
        VV_outprocess.jobprocess(reg_test + '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.out.1','imhomc1')
    
    solver_file.write('<H4>New Run: ishom.c.80km.out.1</H4>')
    solver_file.write("Number of Processors = " + str(procttl_ih1d[-1]) + "<BR>\n")
    solver_file.write("Number of Nonlinear Iterations = ")
    VV_utilities.format(solver_file, nonlist_ih1d)
    solver_file.write('<BR>\n')
    
    if out_flag_ih1d == 1:
        solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
    solver_file.write("Average Number of Linear Iterations per Time-Step = ")
    VV_utilities.format(solver_file, avg2_ih1d)
    solver_file.write('<BR> \n')

    solver_file.write('<H4>Benchmark Run: ishom.c.80km.out.1</H4>')
    procttl_ih1b, nonlist_ih1b, avg2_ih1b, out_flag_ih1b, ndihc1b_name, ldihc1b_name = \
        VV_outprocess.jobprocess(reg_test + '/bench/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.out.1','imhomc1b')

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
    failedt2 = VV_checks.failcheck(reg_test, '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.out.2')
    failedt_list.append(failedt2)

    procttl_ih2d, nonlist_ih2d, avg2_ih2d, out_flag_ih2d, ndihc2_name, ldihc2_name = \
        VV_outprocess.jobprocess(reg_test + '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.out.2','imhom2')
    
    solver_file.write('<H4>New Run: ishom.c.80km.out.2</H4>')
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
    procttl_ih2b, nonlist_ih2b, avg2_ih2b, out_flag_ih2b, ndihc2b_name, ldihc2b_name = \
        VV_outprocess.jobprocess(reg_test + '/bench/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.out.2','imhom2b')

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

# Failure checking
    failedt3 = VV_checks.failcheck(reg_test, '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.out.4')
    failedt_list.append(failedt3)

    procttl_ih4d, nonlist_ih4d, avg2_ih4d, out_flag_ih4d, ndihc4_name, ldihc4_name = \
        VV_outprocess.jobprocess(reg_test + '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.out.4','imhomc4')
    
    solver_file.write('<H4>New Run: ishom.c.80km.out.4</H4>')
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
    procttl_ih4b, nonlist_ih4b, avg2_ih4b, out_flag_ih4b, ndihc4b_name, ldihc4b_name = \
        VV_outprocess.jobprocess(reg_test + '/bench/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.out.4','imhomc4b')

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

# routine for ISMIP HOM C 20km
def c20details(solver_file,reg_test,data_dir):  # using data, fill the web page with info

    failedt_list = []

    solver_file.write('<HTML>\n')
    solver_file.write('<BODY BGCOLOR="#CADFE0">\n')
    solver_file.write('<H3>ISMIP HOM C 20KM Iteration Count Details:</H3>')
    solver_file.write('<BR> \n')

# JFNK gnu 1 proc

# Failure checking
    failedt1 = VV_checks.failcheck(reg_test, '/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.out.1')
    failedt_list.append(failedt1)

    procttl_ih1d, nonlist_ih1d, avg2_ih1d, out_flag_ih1d, ndihc1_name, ldihc1_name = \
        VV_outprocess.jobprocess(reg_test + '/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.out.1','imhomc1')
    
    solver_file.write('<H4>New Run: ishom.c.20km.out.1</H4>')
    solver_file.write("Number of Processors = " + str(procttl_ih1d[-1]) + "<BR>\n")
    solver_file.write("Number of Nonlinear Iterations = ")
    VV_utilities.format(solver_file, nonlist_ih1d)
    solver_file.write('<BR>\n')
    
    if out_flag_ih1d == 1:
        solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
    solver_file.write("Average Number of Linear Iterations per Time-Step = ")
    VV_utilities.format(solver_file, avg2_ih1d)
    solver_file.write('<BR> \n')

    solver_file.write('<H4>Benchmark Run: ishom.c.20km.out.1</H4>')
    procttl_ih1b, nonlist_ih1b, avg2_ih1b, out_flag_ih1b, ndihc1b_name, ldihc1b_name = \
        VV_outprocess.jobprocess(reg_test + '/bench/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.out.1','imhomc1b')

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
    failedt2 = VV_checks.failcheck(reg_test, '/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.out.2')
    failedt_list.append(failedt2)

    procttl_ih2d, nonlist_ih2d, avg2_ih2d, out_flag_ih2d, ndihc2_name, ldihc2_name = \
        VV_outprocess.jobprocess(reg_test + '/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.out.2','imhom2')
    
    solver_file.write('<H4>New Run: ishom.c.20km.out.2</H4>')
    solver_file.write("Number of Processors = " + str(procttl_ih2d[-1]) + "<BR>\n")
    solver_file.write("Number of Nonlinear Iterations = ")
    VV_utilities.format(solver_file, nonlist_ih2d)
    solver_file.write('<BR>\n')
    
    if out_flag_ih2d == 1:
        solver_file.write('<FONT COLOR="red">***TIME STEP(S) THAT FAILED TO CONVERGE</FONT> <BR>\n')
    solver_file.write("Average Number of Linear Iterations per Time-Step = ")
    VV_utilities.format(solver_file, avg2_ih2d)
    solver_file.write('<BR> \n')

    solver_file.write('<H4>Benchmark Run: ishom.c.20km.out.2</H4>')
    procttl_ih2b, nonlist_ih2b, avg2_ih2b, out_flag_ih2b, ndihc2b_name, ldihc2b_name = \
        VV_outprocess.jobprocess(reg_test + '/bench/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.out.2','imhom2b')

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

# Failure checking
    failedt3 = VV_checks.failcheck(reg_test, '/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.out.4')
    failedt_list.append(failedt3)

    procttl_ih4d, nonlist_ih4d, avg2_ih4d, out_flag_ih4d, ndihc4_name, ldihc4_name = \
        VV_outprocess.jobprocess(reg_test + '/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.out.4','imhomc4')
    
    solver_file.write('<H4>New Run: ishom.c.20km.out.4</H4>')
    solver_file.write("Number of Processors = " + str(procttl_ih4d[-1]) + "<BR>\n")
    solver_file.write("Number of Nonlinear Iterations = ")
    VV_utilities.format(solver_file, nonlist_ih4d)
    solver_file.write('<BR>\n')
    
    if out_flag_ih4d == 1:
        solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
    solver_file.write("Average Number of Linear Iterations per Time-Step = ")
    VV_utilities.format(solver_file, avg2_ih4d)
    solver_file.write('<BR> \n')

    solver_file.write('<H4>Benchmark Run: ishom.c.20km.out.4</H4>')
    procttl_ih4b, nonlist_ih4b, avg2_ih4b, out_flag_ih4b, ndihc4b_name, ldihc4b_name = \
        VV_outprocess.jobprocess(reg_test + '/bench/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.out.4','imhomc4b')

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

def a80plot(glide_flag,plot_file,reg_test,ncl_path,html_path,script_path,data_dir):  # using data, fill the web page with info

    plot_file.write('<HTML>\n')
    plot_file.write('<BODY BGCOLOR="#CADFE0">\n')
    plot_file.write('<H3>ISMIP HOM A 80km Plot Details:</H3>')

# formulate ismip a 80 uvel plot
    if glide_flag == 1:
        ishoma80u_plotfile = ''+ ncl_path + '/ismip-a/ismipa80u.ncl'
        stockPIC  = 'STOCKPIC = addfile(\"'+ reg_test + '/bench/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.PIC.out.nc\", \"r\")'
        stockJFNK ='STOCKJFNK = addfile(\"'+ reg_test + '/bench/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.JFNK.out.nc\", \"r\")'
        VARPIC    = 'VARPIC = addfile(\"' + reg_test + '/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.PIC.out.nc\", \"r\")'
        VARJFNK   = 'VARJFNK = addfile(\"' + reg_test + '/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.JFNK.out.nc\", \"r\")'
        pngnameu  = 'ismipa80u.png'
        png       = 'PNG = "' + ncl_path + '/' + pngnameu + '"'
        plot_ishoma80u = "ncl '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARPIC + "'  '" + VARJFNK \
                    +"'  '" + png + "' " + ishoma80u_plotfile + " >> plot_details.out"
    else:
        ishoma80u_plotfile = ''+ ncl_path + '/ismip-a/ismipa80ug.ncl'
        stock1  = 'STOCK1 = addfile(\"'+ reg_test + '/bench/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.glissade.1.nc\", \"r\")'
        stock4  = 'STOCK4 = addfile(\"'+ reg_test + '/bench/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.glissade.4.nc\", \"r\")'
        VAR1    = 'VAR1 = addfile(\"' + reg_test + '/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.glissade.1.nc\", \"r\")'
        VAR4    = 'VAR4 = addfile(\"' + reg_test + '/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.glissade.4.nc\", \"r\")'
        pngnameu= 'ismipa80ug.png'
        png     = 'PNG = "' + ncl_path + '/' + pngnameu + '"'
        plot_ishoma80u = "ncl '" + stock1 + "'  '" + stock4 + "'  '" + VAR1 + "'  '" + VAR4 \
                    +"'  '" + png + "' " + ishoma80u_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
    try:
        subprocess.check_call(plot_ishoma80u, shell=True)
        #print "creating ismip hom a 80km uvel plots"
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)

# delete old ismipa80 uvel pic in www file
    if (html_path + '/' + pngnameu):
        ismipa80uvelmove = ["rm", "-f", html_path+"/" + pngnameu]
        try:
            subprocess.check_call(ismipa80uvelmove)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# transferring ismipau pic to www file
    if (ncl_path + '/' + pngnameu):
        ishoma80upic = ["mv", "-f", ncl_path+"/" + pngnameu, html_path+"/"]
        try:
            subprocess.check_call(ishoma80upic)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# formulate ismip a 80 vvel plot
    if glide_flag == 1:
        ishoma80v_plotfile = ''+ ncl_path + '/ismip-a/ismipa80v.ncl'
        stockPIC  = 'STOCKPIC = addfile(\"'+ reg_test + '/bench/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.PIC.out.nc\", \"r\")'
        stockJFNK = 'STOCKJFNK = addfile(\"'+ reg_test + '/bench/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.JFNK.out.nc\", \"r\")'
        VARPIC    = 'VARPIC = addfile(\"' + reg_test + '/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.PIC.out.nc\", \"r\")'
        VARJFNK   = 'VARJFNK = addfile(\"' + reg_test + '/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.JFNK.out.nc\", \"r\")'
        pngnamev  = 'ismipa80v.png'
        png       = 'PNG = "' + ncl_path + '/' + pngnamev + '"'
        plot_ishoma80v = "ncl '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" \
                    + png + "' " + ishoma80v_plotfile + " >> plot_details.out"
    else:
        ishoma80v_plotfile = ''+ ncl_path + '/ismip-a/ismipa80vg.ncl'
        stock1  = 'STOCK1 = addfile(\"'+ reg_test + '/bench/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.glissade.1.nc\", \"r\")'
        stock4  = 'STOCK4 = addfile(\"'+ reg_test + '/bench/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.glissade.4.nc\", \"r\")'
        VAR1    = 'VAR1 = addfile(\"' + reg_test + '/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.glissade.1.nc\", \"r\")'
        VAR4    = 'VAR4 = addfile(\"' + reg_test + '/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.glissade.4.nc\", \"r\")'
        pngnamev= 'ismipa80vg.png'
        png     = 'PNG = "' + ncl_path + '/' + pngnamev + '"'
        plot_ishoma80v = "ncl '" + stock1 + "'  '" + stock4 + "'  '" + VAR1 + "'  '" + VAR4 +"'  '" \
                    + png + "' " + ishoma80v_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
    try:
        subprocess.check_call(plot_ishoma80v, shell=True)
        #print "creating ismip hom a 80km vvel plots"
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)    

# delete old ismipa80 vvel pic in www file
    if (html_path + '/' + pngnamev):
        ismipa80vvelmove = ["rm", "-f", html_path+"/" + pngnamev]
        try:
            subprocess.check_call(ismipa80vvelmove)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)    

# transferring ismipav pic to www file
    if (ncl_path + '/' + pngnamev): 
        ishoma80vpic = ["mv", "-f", ncl_path+"/" + pngnamev, html_path+"/"]
        try:
            subprocess.check_call(ishoma80vpic)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)   

# formulate ismip a 80 velocity norm plot
#    ishoma80vel_plotfile = ''+ ncl_path + '/ismipa80vel.ncl'
#    stockPIC  = 'STOCKPIC = addfile(\"'+ reg_test + '/bench/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc\", \"r\")'
#    stockJFNK = 'STOCKJFNK = addfile(\"'+ reg_test + '/bench/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc\", \"r\")'
#    VARPIC    = 'VARPIC = addfile(\"' + reg_test + '/ismip-hom-a/80km/data/ishom.a.80km.PIC.out.nc\", \"r\")'
#    VARJFNK   = 'VARJFNK = addfile(\"' + reg_test + '/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc\", \"r\")'
#    pngnamevel   = 'ismipa80vel.png'
#    png       = 'PNG = "' + ncl_path + '/' + pngnamevel + '"'
#    plot_ishoma80vel = "ncl '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" \
#                    + png + "' " + ishoma80vel_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
#    try:
#        subprocess.check_call(plot_ishoma80vel, shell=True)
#        print "creating ismip hom a 80km velocity norm plots"
#    except subprocess.CalledProcessError as e:
#        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#            + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#        exit(e.returncode)
#    except OSError as e:
#        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#            + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#        exit(e.errno)     

# delete old ismipa80 velnorm pic in www file
#    if (html_path + '/' + pngnamevel):
#        ismipa80velmove = ["rm", "-f", html_path+"/ + pngnamevel"]
#        try:
#            subprocess.check_call(ismipa80velmove)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)              

# transferring ismip a 80km velocity norm pic to www file
#    if (ncl_path + '/' + pngnamevel): 
#        ishoma80velpic = ["mv", "-f", ncl_path+"/" + pngnamevel, html_path+"/"]
#        try:
#            subprocess.check_call(ishoma80velpic)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)             

# remove plot_details.out
#    if (script_path + '/plot_details.out'):
#        cleantrash = ["rm", "-f", script_path+"/plot_details.out"]
#        try:
#            subprocess.check_call(cleantrash)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)              

    plot_file.write('<HTML>\n')
    plot_file.write('<TITLE>ISMIP HOM A 80km </TITLE>\n')
    plot_file.write('<TABLE>\n')
    plot_file.write('<TR>\n')
    plot_file.write('<H4>Difference from benchmark run for U Velocity, V Velocity, Velocity Norm, and Thickness</H4>\n')
    plot_file.write('<BR>\n')
    plot_file.write('<OBJECT data="' + pngnameu + '" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 80km Plots">\n')
    plot_file.write('</OBJECT>\n')
    plot_file.write('<OBJECT data="' + pngnamev + '" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 80km Plots">\n')
    plot_file.write('</OBJECT>\n')
#   plot_file.write('<OBJECT data="' + pngnamevel + '" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 80km Plots">\n')
#   plot_file.write('</OBJECT>\n')
    plot_file.write('<TR>\n')
    plot_file.write('<BR>\n')
    plot_file.write('</TABLE>\n')
    plot_file.write('</HTML>\n')
    plot_file.close()

def a20plot(glide_flag,plot_file,reg_test,ncl_path,html_path,script_path,data_dir):  # using data, fill the web page with info

    plot_file.write('<HTML>\n')
    plot_file.write('<BODY BGCOLOR="#CADFE0">\n')
    plot_file.write('<H3>ISMIP HOM A 20km Plot Details:</H3>')

# formulate ismip a 20 uvel plot
    if glide_flag == 1:
        ishoma20u_plotfile = ''+ ncl_path + '/ismip-a/ismipa20u.ncl'
        stockPIC  = 'STOCKPIC = addfile(\"'+ reg_test + '/bench/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.PIC.out.nc\", \"r\")'
        stockJFNK = 'STOCKJFNK = addfile(\"'+ reg_test + '/bench/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.JFNK.out.nc\", \"r\")'
        VARPIC    = 'VARPIC = addfile(\"' + reg_test + '/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.PIC.out.nc\", \"r\")'
        VARJFNK   = 'VARJFNK = addfile(\"' + reg_test + '/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.JFNK.out.nc\", \"r\")'
        pngnameu  = 'ismipa20u.png'
        png       = 'PNG = "' + ncl_path + '/' + pngnameu + '"'
        plot_ishoma20u = "ncl '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARPIC + "'  '" + VARJFNK \
                    +"'  '" + png + "' " + ishoma20u_plotfile + " >> plot_details.out"
    else:
        ishoma20u_plotfile = ''+ ncl_path + '/ismip-a/ismipa20ug.ncl'
        stock1  = 'STOCK1 = addfile(\"'+ reg_test + '/bench/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.glissade.1.nc\", \"r\")'
        stock4  = 'STOCK4 = addfile(\"'+ reg_test + '/bench/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.glissade.4.nc\", \"r\")'
        VAR1    = 'VAR1 = addfile(\"' + reg_test + '/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.glissade.1.nc\", \"r\")'
        VAR4    = 'VAR4 = addfile(\"' + reg_test + '/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.glissade.4.nc\", \"r\")'
        pngnameu= 'ismipa20ug.png'
        png     = 'PNG = "' + ncl_path + '/' + pngnameu + '"'
        plot_ishoma20u = "ncl '" + stock1 + "'  '" + stock4 + "'  '" + VAR1 + "'  '" + VAR4 \
                    +"'  '" + png + "' " + ishoma20u_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
    try:
        subprocess.check_call(plot_ishoma20u, shell=True)
        #print "creating ismip hom a 20km uvel plots"
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)

# delete old ismipa20 uvel pic in www file
    if (html_path + '/' + pngnameu):
        ismipa20uvelmove = ["rm", "-f", html_path+"/" + pngnameu]
        try:
            subprocess.check_call(ismipa20uvelmove)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# transferring ismipa20u pic to www file
    if (ncl_path + '/' + pngnameu):
        ishoma20upic = ["mv", "-f", ncl_path+"/" + pngnameu, html_path+"/"]
        try:
            subprocess.check_call(ishoma20upic)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# formulate ismip a 20 vvel plot
    if glide_flag == 1:
        ishoma20v_plotfile = ''+ ncl_path + '/ismip-a/ismipa20v.ncl'
        stockPIC  = 'STOCKPIC = addfile(\"'+ reg_test + '/bench/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.PIC.out.nc\", \"r\")'
        stockJFNK = 'STOCKJFNK = addfile(\"'+ reg_test + '/bench/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.JFNK.out.nc\", \"r\")'
        VARPIC    = 'VARPIC = addfile(\"' + reg_test + '/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.PIC.out.nc\", \"r\")'
        VARJFNK   = 'VARJFNK = addfile(\"' + reg_test + '/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.JFNK.out.nc\", \"r\")'
        pngnamev  = 'ismipa20v.png'
        png       = 'PNG = "' + ncl_path + '/' + pngnamev + '"'
        plot_ishoma20v = "ncl '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARPIC + "'  '" + VARJFNK \
                    + "'  '" + png + "' " + ishoma20v_plotfile + " >> plot_details.out"
    else:
        ishoma20v_plotfile = ''+ ncl_path + '/ismip-a/ismipa20vg.ncl'
        stock1  = 'STOCK1 = addfile(\"'+ reg_test + '/bench/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.glissade.1.nc\", \"r\")'
        stock4  = 'STOCK4 = addfile(\"'+ reg_test + '/bench/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.glissade.4.nc\", \"r\")'
        VAR1    = 'VAR1 = addfile(\"' + reg_test + '/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.glissade.1.nc\", \"r\")'
        VAR4    = 'VAR4 = addfile(\"' + reg_test + '/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.glissade.4.nc\", \"r\")'
        pngnamev= 'ismipa20vg.png'
        png     = 'PNG = "' + ncl_path + '/' + pngnamev + '"'
        plot_ishoma20v = "ncl '" + stock1 + "'  '" + stock4 + "'  '" + VAR1 + "'  '" + VAR4 \
                    + "'  '" + png + "' " + ishoma20v_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
    try:
        subprocess.check_call(plot_ishoma20v, shell=True)
        #print "creating ismip hom a 20km vvel plots"
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)

# delete old ismipa20 vvel pic in www file
    if (html_path + '/' + pngnamev):
        ismipa20vvelmove = ["rm", "-f", html_path+"/" + pngnamev]
        try:
            subprocess.check_call(ismipa20vvelmove)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# transferring ismipa20v pic to www file
    if (ncl_path + '/' + pngnamev):
        ishoma20vpic = ["mv", "-f", ncl_path+"/" + pngnamev, html_path+"/"]
        try:
            subprocess.check_call(ishoma20vpic)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# formulate ismip a 20 velocity norm plot
#    ishoma20vel_plotfile = ''+ ncl_path + '/ismipa20vel.ncl'
#    stockPIC   = 'STOCKPIC = addfile(\"'+ reg_test + '/bench/ismip-hom-a/20km/data/ishom.a.20km.PIC.out.nc\", \"r\")'
#    stockJFNK  = 'STOCKJFNK = addfile(\"'+ reg_test + '/bench/ismip-hom-a/20km/data/ishom.a.20km.JFNK.out.nc\", \"r\")'
#    VARPIC     = 'VARPIC = addfile(\"' + reg_test + '/ismip-hom-a/20km/data/ishom.a.20km.PIC.out.nc\", \"r\")'
#    VARJFNK    = 'VARJFNK = addfile(\"' + reg_test + '/ismip-hom-a/20km/data/ishom.a.20km.JFNK.out.nc\", \"r\")'
#    pngnamevel = 'ismipa20vel.png'
#    png        = 'PNG = "' + ncl_path + '/' + pngnamevel + '"'
#    plot_ishoma20vel = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK \
#                       + "'  '" + png + "' " + ishoma20vel_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
#    try:
#        subprocess.check_call(plot_ishoma20vel, shell=True)
#        print "creating ismip hom a 20km velocity norm plots"
#    except subprocess.CalledProcessError as e:
#        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#               + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#        exit(e.returncode)
#    except OSError as e:
#        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#               + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#        exit(e.errno)              

# delete old ismipa20 velnorm pic in www file
#    if (html_path + '/' + pngnamevel):
#        ismipa20velmove = ["rm", "-f", html_path+"/" + pngnamevel]
#        try:
#            subprocess.check_call(ismipa20velmove)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                   + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                   + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)              

# transferring ismip a 20km velocity norm pic to www file
#    if (ncl_path + '/' + pngnamevel): 
#        ishoma20velpic = ["mv", "-f", ncl_path+"/" + pngnamevel, html_path+"/"]
#        try:
#            subprocess.check_call(ishoma20velpic)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)              

# remove plot_details.out
#    if (script_path + '/plot_details.out'):
#        cleantrash = ["rm", "-f", script_path+"/plot_details.out"]
#        try:
#            subprocess.check_call(cleantrash)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)              

    plot_file.write('<HTML>\n')
    plot_file.write('<TITLE>ISMIP HOM A 20km </TITLE>\n')
    plot_file.write('<TABLE>\n')
    plot_file.write('<TR>\n')
    plot_file.write('<H4>Difference from benchmark run for U Velocity, V Velocity, Velocity Norm, and Thickness</H4>\n')
    plot_file.write('<BR>\n')
    plot_file.write('<OBJECT data="' + pngnameu + '" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 20km Plots">\n')
    plot_file.write('</OBJECT>\n')
    plot_file.write('<OBJECT data="' + pngnamev + '" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 20km Plots">\n')
    plot_file.write('</OBJECT>\n')
#   plot_file.write('<OBJECT data="' + pngnamevel + '" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 20km Plots">\n')
#   plot_file.write('</OBJECT>\n')
    plot_file.write('<TR>\n')
    plot_file.write('<BR>\n')
    plot_file.write('</TABLE>\n')
    plot_file.write('</HTML>\n')
    plot_file.close()

def c80plot(glide_flag,plot_file,reg_test,ncl_path,html_path,script_path,data_dir):  # using data, fill the web page with info

    plot_file.write('<HTML>\n')
    plot_file.write('<BODY BGCOLOR="#CADFE0">\n')
    plot_file.write('<H3>ISMIP HOM C 80km Plot Details:</H3>')

# formulate ismip c 80 uvel plot
    if glide_flag == 1:
        ishomcu_plotfile = ''+ ncl_path + '/ismip-c/ismipc80u.ncl'
        stockPIC  = 'STOCKPIC = addfile(\"'+ reg_test + '/bench/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.PIC.out.nc\", \"r\")'
        stockJFNK = 'STOCKJFNK = addfile(\"'+ reg_test + '/bench/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.JFNK.out.nc\", \"r\")'
        VARPIC    = 'VARPIC = addfile(\"' + reg_test + '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.PIC.out.nc\", \"r\")'
        VARJFNK   = 'VARJFNK = addfile(\"' + reg_test + '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.JFNK.out.nc\", \"r\")'
        pngnameu  = 'ismipcu.png'
        png       = 'PNG = "' + ncl_path + '/' + pngnameu + '"'
        plot_ishomcu = "ncl '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARPIC + "'  '" + VARJFNK \
                + "'  '" + png + "' " + ishomcu_plotfile + " >> plot_details.out"
    else:
        ishomcu_plotfile = ''+ ncl_path + '/ismip-c/ismipc80ug.ncl'
        stock1  = 'STOCK1 = addfile(\"'+ reg_test + '/bench/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.glissade.1.nc\", \"r\")'
        stock4  = 'STOCK4 = addfile(\"'+ reg_test + '/bench/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.glissade.4.nc\", \"r\")'
        VAR1    = 'VAR1 = addfile(\"' + reg_test + '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.glissade.1.nc\", \"r\")'
        VAR4    = 'VAR4 = addfile(\"' + reg_test + '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.glissade.4.nc\", \"r\")'
        pngnameu= 'ismipcug.png'
        png     = 'PNG = "' + ncl_path + '/' + pngnameu + '"'
        plot_ishomcu = "ncl '" + stock1 + "'  '" + stock4 + "'  '" + VAR1 + "'  '" + VAR4 \
                + "'  '" + png + "' " + ishomcu_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
    try:
        subprocess.check_call(plot_ishomcu, shell=True)
        #print "creating ismip hom c uvel plots"
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)

# delete old ismipc80 uvel pic in www file
    if (html_path + '/' + pngnameu):
        ismipcuvelmove = ["rm", "-f", html_path+"/" + pngnameu]
        try:
            subprocess.check_call(ismipcuvelmove)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# transferring ismipcu pic to www file
    if (ncl_path + '/' + pngnameu):
        ishomcupic = ["mv", "-f", ncl_path+"/" + pngnameu, html_path+"/"]
        try:
            subprocess.check_call(ishomcupic)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# formulate ismip c 80 vvel plot
    if glide_flag == 1:
        ishomcv_plotfile = ''+ ncl_path + '/ismip-c/ismipc80v.ncl'
        stockPIC  = 'STOCKPIC = addfile(\"'+ reg_test + '/bench/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.PIC.out.nc\", \"r\")'
        stockJFNK = 'STOCKJFNK = addfile(\"'+ reg_test + '/bench/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.JFNK.out.nc\", \"r\")'
        VARPIC    = 'VARPIC = addfile(\"' + reg_test + '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.PIC.out.nc\", \"r\")'
        VARJFNK   = 'VARJFNK = addfile(\"' + reg_test + '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.JFNK.out.nc\", \"r\")'
        pngnamev  = 'ismipcv.png'
        png       = 'PNG = "' + ncl_path + '/' + pngnamev + '"'
        plot_ishomcv = "ncl '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARPIC + "'  '" + VARJFNK \
                + "'  '" + png + "' " + ishomcv_plotfile + " >> plot_details.out"
    else:
        ishomcv_plotfile = ''+ ncl_path + '/ismip-c/ismipc80vg.ncl'
        stock1  = 'STOCK1 = addfile(\"'+ reg_test + '/bench/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.glissade.1.nc\", \"r\")'
        stock4  = 'STOCK4 = addfile(\"'+ reg_test + '/bench/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.glissade.4.nc\", \"r\")'
        VAR1    = 'VAR1 = addfile(\"' + reg_test + '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.glissade.1.nc\", \"r\")'
        VAR4    = 'VAR4 = addfile(\"' + reg_test + '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.glissade.4.nc\", \"r\")'
        pngnamev= 'ismipcvg.png'
        png     = 'PNG = "' + ncl_path + '/' + pngnamev + '"'
        plot_ishomcv = "ncl '" + stock1 + "'  '" + stock4 + "'  '" + VAR1 + "'  '" + VAR4 \
                + "'  '" + png + "' " + ishomcv_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
    try:
        subprocess.check_call(plot_ishomcv, shell=True)
        #print "creating ismip hom c vvel plots"
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)

# delete old ismipc80 vvel pic in www file
    if (html_path + '/' + pngnamev):
        ismipcvvelmove = ["rm", "-f", html_path+"/" + pngnamev]
        try:
            subprocess.check_call(ismipcvvelmove)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# transferring ismipcv pic to www file
    if (ncl_path + '/' + pngnamev):
        ishomcvpic = ["mv", "-f", ncl_path+"/" + pngnamev, html_path+"/"]
        try:
            subprocess.check_call(ishomcvpic)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# formulate ismip c 80 velocity norm plot
#    if glide_flag == 1:
#        ishomcvel_plotfile = ''+ ncl_path + '/ismip-c/ismipc80vel.ncl'
#        stockPIC    = 'STOCKPIC = addfile(\"'+ reg_test + '/bench/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.PIC.out.nc\", \"r\")'
#        stockJFNK   = 'STOCKJFNK = addfile(\"'+ reg_test + '/bench/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.JFNK.out.nc\", \"r\")'
#        VARPIC      = 'VARPIC = addfile(\"' + reg_test + '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.PIC.out.nc\", \"r\")'
#        VARJFNK     = 'VARJFNK = addfile(\"' + reg_test + '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.JFNK.out.nc\", \"r\")'
#        pngnamevel  = 'ismipcvel.png'
#        png         = 'PNG = "' + ncl_path + '/' + pngnamevel + '"'
#        plot_ishomcvel = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK \
#                    + "'  '" + png + "' " + ishomcvel_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
#    try:
#            subprocess.check_call(plot_ishomcvel, shell=True)
#            #print "creating ismip hom c velocity norm plots"
#    except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#    except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)

# delete old ismipc80 vel norm pic in www file
#    if (html_path + '/' + pngnamevel):
#        ismipcvelmove = ["rm", "-f", html_path+"/" + pngnamevel]
#        try:
#            subprocess.check_call(ismipcvelmove)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)

# transferring ismip c velocity norm pic to www file
#    if (ncl_path + '/' + pngnamevel):
#        ishomcvelpic = ["mv", "-f", ncl_path+"/" + pngnamevel, html_path+"/"]
#        try:
#            subprocess.check_call(ishomcvelpic)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)

# remove plot_details.out
#    if (script_path + '/plot_details.out'):
#        cleantrash = ["rm", "-f", script_path+"/plot_details.out"]
#        try:
#            subprocess.check_call(cleantrash)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                   + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) /
#                   + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)   

    plot_file.write('<HTML>\n')
    plot_file.write('<TITLE>ISMIP HOM C 80km </TITLE>\n')
    plot_file.write('<TABLE>\n')
    plot_file.write('<TR>\n')
    plot_file.write('<H4>Difference from Benchmark run for U Velocity and V Velocity</H4>\n')
    plot_file.write('<BR>\n')
    plot_file.write('<OBJECT data="' + pngnameu + '" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM C 80km Plots">\n')
    plot_file.write('</OBJECT>\n')
    plot_file.write('<OBJECT data="' + pngnamev + '" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM C 80km Plots">\n')
    plot_file.write('</OBJECT>\n')
#    plot_file.write('<OBJECT data="' + pngnamevel + '" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM C 80km Plots">\n')
    plot_file.write('</OBJECT>\n')
    plot_file.write('<TR>\n')
    plot_file.write('<BR>\n')
    plot_file.write('</TABLE>\n')
    plot_file.write('</HTML>\n')
    plot_file.close()

def c20plot(glide_flag,plot_file,reg_test,ncl_path,html_path,script_path,data_dir):  # using data, fill the web page with info

    plot_file.write('<HTML>\n')
    plot_file.write('<BODY BGCOLOR="#CADFE0">\n')
    plot_file.write('<H3>ISMIP HOM C 20km Plot Details:</H3>')

# formulate ismip c 20 uvel plot
    if glide_flag == 1:
        ishomcu_plotfile = ''+ ncl_path + '/ismipc20u.ncl'
        stockPIC  = 'STOCKPIC = addfile(\"'+ reg_test + '/bench/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.PIC.out.nc\", \"r\")'
        stockJFNK = 'STOCKJFNK = addfile(\"'+ reg_test + '/bench/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.JFNK.out.nc\", \"r\")'
        VARPIC    = 'VARPIC = addfile(\"' + reg_test + '/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.PIC.out.nc\", \"r\")'
        VARJFNK   = 'VARJFNK = addfile(\"' + reg_test + '/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.JFNK.out.nc\", \"r\")'
        pngnameu  = 'ismipc2u.png'
        png       = 'PNG = "' + ncl_path + '/' + pngnameu + '"'
        plot_ishomcu = "ncl '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARPIC + "'  '" + VARJFNK \
                + "'  '" + png + "' " + ishomcu_plotfile + " >> plot_details.out"
    else:
        ishomcu_plotfile = ''+ ncl_path + '/ismip-c/ismipc20ug.ncl'
        stock1  = 'STOCK1 = addfile(\"'+ reg_test + '/bench/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.glissade.1.nc\", \"r\")'
        stock4  = 'STOCK4 = addfile(\"'+ reg_test + '/bench/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.glissade.4.nc\", \"r\")'
        VAR1    = 'VAR1 = addfile(\"' + reg_test + '/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.glissade.1.nc\", \"r\")'
        VAR4    = 'VAR4 = addfile(\"' + reg_test + '/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.glissade.4.nc\", \"r\")'
        pngnameu= 'ismipc2ug.png'
        png     = 'PNG = "' + ncl_path + '/' + pngnameu + '"'
        plot_ishomcu = "ncl '" + stock1 + "'  '" + stock4 + "'  '" + VAR1 + "'  '" + VAR4 \
                + "'  '" + png + "' " + ishomcu_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
    try:
        subprocess.check_call(plot_ishomcu, shell=True)
        #print "creating ismip hom c uvel plots"
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)

# delete old ismipc20 uvel pic in www file
    if (html_path + '/' + pngnameu):
        ismipcuvelmove = ["rm", "-f", html_path+"/" + pngnameu]
        try:
            subprocess.check_call(ismipcuvelmove)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# transferring ismipcu pic to www file
    if (ncl_path + '/' + pngnameu):
        ishomcupic = ["mv", "-f", ncl_path+"/" + pngnameu, html_path+"/"]
        try:
            subprocess.check_call(ishomcupic)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# formulate ismip c 20 vvel plot
    if glide_flag == 1:
        ishomcv_plotfile = ''+ ncl_path + '/ismipc20v.ncl'
        stockPIC  = 'STOCKPIC = addfile(\"'+ reg_test + '/bench/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.PIC.out.nc\", \"r\")'
        stockJFNK = 'STOCKJFNK = addfile(\"'+ reg_test + '/bench/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.JFNK.out.nc\", \"r\")'
        VARPIC    = 'VARPIC = addfile(\"' + reg_test + '/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.PIC.out.nc\", \"r\")'
        VARJFNK   = 'VARJFNK = addfile(\"' + reg_test + '/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.JFNK.out.nc\", \"r\")'
        pngnamev  = 'ismipc2v.png'
        png       = 'PNG = "' + ncl_path + '/' + pngnamev + '"'
        plot_ishomcv = "ncl '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARPIC + "'  '" + VARJFNK \
                + "'  '" + png + "' " + ishomcv_plotfile + " >> plot_details.out"
    else:
        ishomcv_plotfile = ''+ ncl_path + '/ismip-c/ismipc20vg.ncl'
        stock1  = 'STOCK1 = addfile(\"'+ reg_test + '/bench/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.glissade.1.nc\", \"r\")'
        stock4  = 'STOCK4 = addfile(\"'+ reg_test + '/bench/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.glissade.4.nc\", \"r\")'
        VAR1    = 'VAR1 = addfile(\"' + reg_test + '/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.glissade.1.nc\", \"r\")'
        VAR4    = 'VAR4 = addfile(\"' + reg_test + '/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.glissade.4.nc\", \"r\")'
        pngnamev= 'ismipc2vg.png'
        png     = 'PNG = "' + ncl_path + '/' + pngnamev + '"'
        plot_ishomcv = "ncl '" + stock1 + "'  '" + stock4 + "'  '" + VAR1 + "'  '" + VAR4 \
                + "'  '" + png + "' " + ishomcv_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
    try:
        subprocess.check_call(plot_ishomcv, shell=True)
        #print "creating ismip hom c vvel plots"
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)

# delete old ismipc20 vvel pic in www file
    if (html_path + '/' + pngnamev):
        ismipcvvelmove = ["rm", "-f", html_path+"/" + pngnamev]
        try:
            subprocess.check_call(ismipcvvelmove)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# transferring ismipcv pic to www file
    if (ncl_path + '/' + pngnamev):
        ishomcvpic = ["mv", "-f", ncl_path+"/" + pngnamev, html_path+"/"]
        try:
            subprocess.check_call(ishomcvpic)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# formulate ismip c 20 velocity norm plot
#    if glide_flag == 1:
#        ishomcvel_plotfile = ''+ ncl_path + '/ismip-c/ismipc20vel.ncl'
#        stockPIC    = 'STOCKPIC = addfile(\"'+ reg_test + '/bench/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.PIC.out.nc\", \"r\")'
#        stockJFNK   = 'STOCKJFNK = addfile(\"'+ reg_test + '/bench/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.JFNK.out.nc\", \"r\")'
#        VARPIC      = 'VARPIC = addfile(\"' + reg_test + '/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.PIC.out.nc\", \"r\")'
#        VARJFNK     = 'VARJFNK = addfile(\"' + reg_test + '/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.JFNK.out.nc\", \"r\")'
#        pngnamevel  = 'ismipcvel.png'
#        png         = 'PNG = "' + ncl_path + '/' + pngnamevel + '"'
#        plot_ishomcvel = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK \
#                    + "'  '" + png + "' " + ishomcvel_plotfile + " >> plot_details.out"

#TODO create an iteration plot and have that also in the html file 
#    try:
#            subprocess.check_call(plot_ishomcvel, shell=True)
#            #print "creating ismip hom c velocity norm plots"
#    except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#    except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)

# delete old ismipc20 vel norm pic in www file
#    if (html_path + '/' + pngnamevel):
#        ismipcvelmove = ["rm", "-f", html_path+"/" + pngnamevel]
#        try:
#            subprocess.check_call(ismipcvelmove)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)

# transferring ismip c velocity norm pic to www file
#    if (ncl_path + '/' + pngnamevel):
#        ishomcvelpic = ["mv", "-f", ncl_path+"/" + pngnamevel, html_path+"/"]
#        try:
#            subprocess.check_call(ishomcvelpic)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)

# remove plot_details.out
#    if (script_path + '/plot_details.out'):
#        cleantrash = ["rm", "-f", script_path+"/plot_details.out"]
#        try:
#            subprocess.check_call(cleantrash)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                   + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) /
#                   + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)   

    plot_file.write('<HTML>\n')
    plot_file.write('<TITLE>ISMIP HOM C 20km </TITLE>\n')
    plot_file.write('<TABLE>\n')
    plot_file.write('<TR>\n')
    plot_file.write('<H4>Difference from Benchmark run for U Velocity and V Velocity</H4>\n')
    plot_file.write('<BR>\n')
    plot_file.write('<OBJECT data="' + pngnameu + '" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM C 20km Plots">\n')
    plot_file.write('</OBJECT>\n')
    plot_file.write('<OBJECT data="' + pngnamev + '" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM C 20km Plots">\n')
    plot_file.write('</OBJECT>\n')
#    plot_file.write('<OBJECT data="' + pngnamevel + '" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM C 20km Plots">\n')
    plot_file.write('</OBJECT>\n')
    plot_file.write('<TR>\n')
    plot_file.write('<BR>\n')
    plot_file.write('</TABLE>\n')
    plot_file.write('</HTML>\n')

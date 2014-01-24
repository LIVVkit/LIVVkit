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
    solver_file.write('<H3>ISMIP HOM C Iteration Count Details:</H3>')
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

def a80plot(plot_file,reg_test,ncl_path,html_path,script_path,data_dir):  # using data, fill the web page with info

    plot_file.write('<HTML>\n')
    plot_file.write('<BODY BGCOLOR="#CADFE0">\n')
    plot_file.write('<H3>ISMIP HOM A 80km Plot Details:</H3>')

# formulate ismip a 80 uvel plot
    ishoma80u_plotfile = ''+ ncl_path + '/ismipa80u.ncl'
    stockPIC  = 'STOCKPIC = addfile(\"'+ reg_test + '/bench/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.PIC.out.nc\", \"r\")'
    stockJFNK ='STOCKJFNK = addfile(\"'+ reg_test + '/bench/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.JFNK.out.nc\", \"r\")'
    VARPIC    = 'VARPIC = addfile(\"' + reg_test + '/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.PIC.out.nc\", \"r\")'
    VARJFNK   = 'VARJFNK = addfile(\"' + reg_test + '/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.JFNK.out.nc\", \"r\")'
    png       = 'PNG = "' + ncl_path + '/ismipa80u"'
    plot_ishoma80u = "ncl '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARPIC + "'  '" + VARJFNK \
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
    if (html_path + '/ismipa80u.png'):
        ismipa80uvelmove = ["rm", "-f", html_path+"/ismipa80u.png"]
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
    if (ncl_path + '/ismipa80u.png'):
        ishoma80upic = ["mv", "-f", ncl_path+"/ismipa80u.png", html_path+"/"]
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
    ishoma80v_plotfile = ''+ ncl_path + '/ismipa80v.ncl'
    stockPIC  = 'STOCKPIC = addfile(\"'+ reg_test + '/bench/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.PIC.out.nc\", \"r\")'
    stockJFNK = 'STOCKJFNK = addfile(\"'+ reg_test + '/bench/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.JFNK.out.nc\", \"r\")'
    VARPIC    = 'VARPIC = addfile(\"' + reg_test + '/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.PIC.out.nc\", \"r\")'
    VARJFNK   = 'VARJFNK = addfile(\"' + reg_test + '/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.JFNK.out.nc\", \"r\")'
    png       = 'PNG = "' + ncl_path + '/ismipa80v"'
    plot_ishoma80v = "ncl '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARPIC + "'  '" + VARJFNK +"'  '" \
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
    if (html_path + '/ismipa80v.png'):
        ismipa80vvelmove = ["rm", "-f", html_path+"/ismipa80v.png"]
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
    if (ncl_path + '/ismipa80v.png'): 
        ishoma80vpic = ["mv", "-f", ncl_path+"/ismipa80v.png", html_path+"/"]
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
#    png  = 'PNG = "' + ncl_path + '/ismipa80vel"'
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
#    if (html_path + '/ismipa80vel.png'):
#        ismipa80velmove = ["rm", "-f", html_path+"/ismipa80vel.png"]
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
#    if (ncl_path + '/ismipa80vel.png'): 
#        ishoma80velpic = ["mv", "-f", ncl_path+"/ismipa80vel.png", html_path+"/"]
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
    plot_file.write('<OBJECT data="ismipa80u.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 80km Plots">\n')
    plot_file.write('</OBJECT>\n')
    plot_file.write('<OBJECT data="ismipa80v.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 80km Plots">\n')
    plot_file.write('</OBJECT>\n')
#   plot_file.write('<OBJECT data="ismipa80vel.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 80km Plots">\n')
#   plot_file.write('</OBJECT>\n')
    plot_file.write('<TR>\n')
    plot_file.write('<BR>\n')
    plot_file.write('</TABLE>\n')
    plot_file.write('</HTML>\n')
    plot_file.close()

def a20plot(plot_file,reg_test,ncl_path,html_path,script_path,data_dir):  # using data, fill the web page with info

    plot_file.write('<HTML>\n')
    plot_file.write('<BODY BGCOLOR="#CADFE0">\n')
    plot_file.write('<H3>ISMIP HOM A 20km Plot Details:</H3>')

# formulate ismip a 20 uvel plot
    ishoma20u_plotfile = ''+ ncl_path + '/ismipa20u.ncl'
    stockPIC  = 'STOCKPIC = addfile(\"'+ reg_test + '/bench/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.PIC.out.nc\", \"r\")'
    stockJFNK = 'STOCKJFNK = addfile(\"'+ reg_test + '/bench/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.JFNK.out.nc\", \"r\")'
    VARPIC    = 'VARPIC = addfile(\"' + reg_test + '/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.PIC.out.nc\", \"r\")'
    VARJFNK   = 'VARJFNK = addfile(\"' + reg_test + '/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.JFNK.out.nc\", \"r\")'
    png       = 'PNG = "' + ncl_path + '/ismipa20u"'
    plot_ishoma20u = "ncl '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARPIC + "'  '" + VARJFNK \
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
    if (html_path + '/ismipa20u.png'):
        ismipa20uvelmove = ["rm", "-f", html_path+"/ismipa20u.png"]
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
    if (ncl_path + '/ismipa20u.png'):
        ishoma20upic = ["mv", "-f", ncl_path+"/ismipa20u.png", html_path+"/"]
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
    ishoma20v_plotfile = ''+ ncl_path + '/ismipa20v.ncl'
    stockPIC  = 'STOCKPIC = addfile(\"'+ reg_test + '/bench/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.PIC.out.nc\", \"r\")'
    stockJFNK = 'STOCKJFNK = addfile(\"'+ reg_test + '/bench/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.JFNK.out.nc\", \"r\")'
    VARPIC    = 'VARPIC = addfile(\"' + reg_test + '/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.PIC.out.nc\", \"r\")'
    VARJFNK   = 'VARJFNK = addfile(\"' + reg_test + '/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.JFNK.out.nc\", \"r\")'
    png       = 'PNG = "' + ncl_path + '/ismipa20v"'
    plot_ishoma20v = "ncl '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARPIC + "'  '" + VARJFNK \
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
    if (html_path + '/ismipa20v.png'):
        ismipa20vvelmove = ["rm", "-f", html_path+"/ismipa20v.png"]
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
    if (ncl_path + '/ismipa20v.png'):
        ishoma20vpic = ["mv", "-f", ncl_path+"/ismipa20v.png", html_path+"/"]
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
#    stockPIC  = 'STOCKPIC = addfile(\"'+ reg_test + '/bench/ismip-hom-a/20km/data/ishom.a.20km.PIC.out.nc\", \"r\")'
#    stockJFNK = 'STOCKJFNK = addfile(\"'+ reg_test + '/bench/ismip-hom-a/20km/data/ishom.a.20km.JFNK.out.nc\", \"r\")'
#    VARPIC    = 'VARPIC = addfile(\"' + reg_test + '/ismip-hom-a/20km/data/ishom.a.20km.PIC.out.nc\", \"r\")'
#    VARJFNK   = 'VARJFNK = addfile(\"' + reg_test + '/ismip-hom-a/20km/data/ishom.a.20km.JFNK.out.nc\", \"r\")'
#    png       = 'PNG = "' + ncl_path + '/ismipa20vel"'
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
#    if (html_path + '/ismipa20vel.png'):
#        ismipa20velmove = ["rm", "-f", html_path+"/ismipa20vel.png"]
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
#    if (ncl_path + '/ismipa20vel.png'): 
#        ishoma20velpic = ["mv", "-f", ncl_path+"/ismipa20vel.png", html_path+"/"]
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
    plot_file.write('<OBJECT data="ismipa20u.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 20km Plots">\n')
    plot_file.write('</OBJECT>\n')
    plot_file.write('<OBJECT data="ismipa20v.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 20km Plots">\n')
    plot_file.write('</OBJECT>\n')
#   plot_file.write('<OBJECT data="ismipa20vel.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM A 20km Plots">\n')
#   plot_file.write('</OBJECT>\n')
    plot_file.write('<TR>\n')
    plot_file.write('<BR>\n')
    plot_file.write('</TABLE>\n')
    plot_file.write('</HTML>\n')
    plot_file.close()

def c80plot(plot_file,reg_test,ncl_path,html_path,script_path,data_dir):  # using data, fill the web page with info

    plot_file.write('<HTML>\n')
    plot_file.write('<BODY BGCOLOR="#CADFE0">\n')
    plot_file.write('<H3>ISMIP HOM C 80km Plot Details:</H3>')

# formulate ismip c 80 uvel plot
    ishomcu_plotfile = ''+ ncl_path + '/ismipc80u.ncl'
    stockPIC  = 'STOCKPIC = addfile(\"'+ reg_test + '/bench/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.PIC.out.nc\", \"r\")'
    stockJFNK = 'STOCKJFNK = addfile(\"'+ reg_test + '/bench/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.JFNK.out.nc\", \"r\")'
    VARPIC    = 'VARPIC = addfile(\"' + reg_test + '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.PIC.out.nc\", \"r\")'
    VARJFNK   = 'VARJFNK = addfile(\"' + reg_test + '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.JFNK.out.nc\", \"r\")'
    png       = 'PNG = "' + ncl_path + '/ismipcu"'
    plot_ishomcu = "ncl '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARPIC + "'  '" + VARJFNK \
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
    if (html_path + '/ismipcu.png'):
        ismipcuvelmove = ["rm", "-f", html_path+"/ismipcu.png"]
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
    if (ncl_path + '/ismipcu.png'):
        ishomcupic = ["mv", "-f", ncl_path+"/ismipcu.png", html_path+"/"]
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
    ishomcv_plotfile = ''+ ncl_path + '/ismipc80v.ncl'
    stockPIC  = 'STOCKPIC = addfile(\"'+ reg_test + '/bench/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.PIC.out.nc\", \"r\")'
    stockJFNK = 'STOCKJFNK = addfile(\"'+ reg_test + '/bench/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.JFNK.out.nc\", \"r\")'
    VARPIC    = 'VARPIC = addfile(\"' + reg_test + '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.PIC.out.nc\", \"r\")'
    VARJFNK   = 'VARJFNK = addfile(\"' + reg_test + '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.JFNK.out.nc\", \"r\")'
    png       = 'PNG = "' + ncl_path + '/ismipcv"'
    plot_ishomcv = "ncl '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARPIC + "'  '" + VARJFNK \
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
    if (html_path + '/ismipcv.png'):
        ismipcvvelmove = ["rm", "-f", html_path+"/ismipcv.png"]
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
    if (ncl_path + '/ismipcv.png'):
        ishomcvpic = ["mv", "-f", ncl_path+"/ismipcv.png", html_path+"/"]
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
    ishomcvel_plotfile = ''+ ncl_path + '/ismipc80vel.ncl'
    stockPIC  = 'STOCKPIC = addfile(\"'+ reg_test + '/bench/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.PIC.out.nc\", \"r\")'
    stockJFNK = 'STOCKJFNK = addfile(\"'+ reg_test + '/bench/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.JFNK.out.nc\", \"r\")'
    VARPIC    = 'VARPIC = addfile(\"' + reg_test + '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.PIC.out.nc\", \"r\")'
    VARJFNK   = 'VARJFNK = addfile(\"' + reg_test + '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.JFNK.out.nc\", \"r\")'
    png       = 'PNG = "' + ncl_path + '/ismipcvel"'
    plot_ishomcvel = "ncl '" + stockout + "'  '" + stockPIC + "'  '" + stockJFNK + "'  '" + VARout + "'  '" + VARPIC + "'  '" + VARJFNK \
                    + "'  '" + png + "' " + ishomcvel_plotfile + " >> plot_details.out"
#TODO create an iteration plot and have that also in the html file 
    try:
            subprocess.check_call(plot_ishomcvel, shell=True)
            #print "creating ismip hom c velocity norm plots"
    except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
    except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# delete old ismipc80 vel norm pic in www file
    if (html_path + '/ismipcvel.png'):
        ismipcvelmove = ["rm", "-f", html_path+"/ismipcvel.png"]
        try:
            subprocess.check_call(ismipcvelmove)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# transferring ismip c velocity norm pic to www file
    if (ncl_path + '/ismipcvel.png'):
        ishomcvelpic = ["mv", "-f", ncl_path+"/ismipcvel.png", html_path+"/"]
        try:
            subprocess.check_call(ishomcvelpic)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

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
    plot_file.write('<H4>Difference from benchmark run for U Velocity, V Velocity, Velocity Norm, and Thickness</H4>\n')
    plot_file.write('<BR>\n')
    plot_file.write('<OBJECT data="ismipcu.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM C 80km Plots">\n')
    plot_file.write('</OBJECT>\n')
    plot_file.write('<OBJECT data="ismipcv.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM C 80km Plots">\n')
    plot_file.write('</OBJECT>\n')
    plot_file.write('<OBJECT data="ismipcvel.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="ISMIP HOM C 80km Plots">\n')
    plot_file.write('</OBJECT>\n')
    plot_file.write('<TR>\n')
    plot_file.write('<BR>\n')
    plot_file.write('</TABLE>\n')
    plot_file.write('</HTML>\n')
    plot_file.close()



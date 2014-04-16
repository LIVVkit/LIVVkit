#!/usr/bin/env

import sys
import os
from optparse import OptionParser
import subprocess
import collections
import VV_outprocess
import VV_utilities
import VV_checks

failedt_list = []

def ddetails(solver_file,reg_test,data_dir): # using data, fill the web page with info

    failedt_list = []
    solver_file.write('<HTML>\n')
    solver_file.write('<BODY BGCOLOR="#CADFE0">\n')
    solver_file.write('<H3>Diagnostic Dome 30 Iteration Count Details:</H3>')
    solver_file.write('<BR> \n')

# JFNK gnu 1 proc

# Failure checking
    failedt1 = VV_checks.failcheck(reg_test, '/dome30/diagnostic/' + data_dir + '/gnu.JFNK.1proc')
    failedt_list.append(failedt1)

    procttl_dd301,nonlist_dd301,avg2_dd301,out_flag_dd301,ndd301_name,ldd301_name,linear_flag = \
        VV_outprocess.jobprocess(reg_test + '/bench/dome30/diagnostic/' + data_dir + '/gnu.JFNK.1proc', 'domed301')

    solver_file.write('<H4>New Run: gnu.JFNK.1proc</H4>')
    solver_file.write("Number of Processors = " + str(procttl_dd301[-1]) + "<BR>\n")
    solver_file.write("Number of Nonlinear Iterations = ")
    VV_utilities.format(solver_file, nonlist_dd301)
    solver_file.write('<BR>\n')

    if out_flag_dd301 == 1:
        solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
    solver_file.write("Average Number of Linear Iterations per Time-Step = ")
    if linear_flag == 1:
        VV_utilities.format(solver_file, avg2_dd301)
    else:
        solver_file.write("Linear Iterations not displayed in the output file ")
    solver_file.write('<BR> \n')

    solver_file.write('<H4>Benchmark Run: gnu.JFNK.1proc</H4>')
    procttl_dd301b,nonlist_dd301b,avg2_dd301b,out_flag_dd301b,ndd301b_name,ldd301b_name,linear_flagb = \
        VV_outprocess.jobprocess(reg_test + '/bench/dome30/diagnostic/' + data_dir + '/gnu.JFNK.1proc', 'domed301b')

    solver_file.write("Number of Processors = " + str(procttl_dd301b[-1]) + "<BR>\n")
    solver_file.write("Number of Nonlinear Iterations = ")
    VV_utilities.format(solver_file, nonlist_dd301b)
    solver_file.write('<BR>\n')
    
    if out_flag_dd301b == 1:
        solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
    solver_file.write("Average Number of Linear Iterations per Time-Step = ")
    if linear_flagb == 1:
        VV_utilities.format(solver_file, avg2_dd301b)
    else:
        solver_file.write("Linear Iterations not displayed in the output file ")
    solver_file.write('<BR> \n')
    solver_file.write('<BR>\n')
    solver_file.write('<BR>\n')

# JFNK gnu 4 proc

# Failure checking
    failedt2 = VV_checks.failcheck(reg_test, '/dome30/diagnostic/' + data_dir + '/gnu.JFNK.4proc')
    failedt_list.append(failedt2)
    
    procttl_dd304,nonlist_dd304,avg2_dd304,out_flag_dd304,ndd304_name,ldd304_name,linear_flag = \
        VV_outprocess.jobprocess(reg_test + '/bench/dome30/diagnostic/' + data_dir + '/gnu.JFNK.4proc','domed304')

    solver_file.write('<H4>New Run: gnu.JFNK.4proc</H4>')
    solver_file.write("Number of Processors = " + str(procttl_dd304[-1]) + "<BR>\n")
    solver_file.write("Number of Nonlinear Iterations = ")
    VV_utilities.format(solver_file, nonlist_dd304)
    solver_file.write('<BR>\n')

    if out_flag_dd304 == 1:
        solver_file.write('<FONT COLOR="red">***TIME STEP(S) THAT FAILED TO CONVERGE</FONT> <BR>\n')
    solver_file.write("Average Number of Linear Iterations per Time-Step = ")
    if linear_flag == 1:
        VV_utilities.format(solver_file, avg2_dd304)
    else:
        solver_file.write("Linear Iterations not displayed in the output file ")
    solver_file.write('<BR> \n')

    solver_file.write('<H4>Benchmark Run: gnu.JFNK.4proc</H4>')
    procttl_dd304b,nonlist_dd304b,avg2_dd304b,out_flag_dd304b,ndd304b_name,ldd304b_name,linear_flagb = \
        VV_outprocess.jobprocess(reg_test + '/bench/dome30/diagnostic/' + data_dir + '/gnu.JFNK.4proc','domed304b')

    solver_file.write("Number of Processors = " + str(procttl_dd304b[-1]) + "<BR>\n")
    solver_file.write("Number of Nonlinear Iterations = ")
    VV_utilities.format(solver_file, nonlist_dd304b)
    solver_file.write('<BR>\n')

    if out_flag_dd304b == 1:
        solver_file.write('<FONT COLOR="red">***TIME STEP(S) THAT FAILED TO CONVERGE</FONT> <BR>\n')
    solver_file.write("Average Number of Linear Iterations per Time-Step = ")
    if linear_flagb == 1:
        VV_utilities.format(solver_file, avg2_dd304b)
    else:
        solver_file.write("Linear Iterations not displayed in the output file ")
    solver_file.write('<BR> \n')

    if 1 in failedt_list:
        failedt = 1
    else:
        failedt = 0

    return failedt

def edetails(solver_file,test_suite,reg_test,ncl_path,html_path,data_dir): # using data, fill the web page with info

    solver_file.write('<HTML>\n')
    solver_file.write('<BODY BGCOLOR="#CADFE0">\n')
    solver_file.write('<H3>Evolving Dome 30 Iteration Count Details:</H3>')
    solver_file.write('<BR> \n')

# JFNK gnu 9 proc

# Failure checking
#    failedt1 = VV_checks.failcheck(reg_test, '/dome30/evolving/' + data_dir + '/gnu.JFNK.9proc')
#    failedt_list.append(failedt1)

#    procttl_de309,nonlist_de309,avg2_de309,out_flag_de309,nde309_name,lde309_name,linear_flag = \
#        VV_outprocess.jobprocess(reg_test + '/dome30/evolving/' + data_dir + '/gnu.JFNK.9proc', 'domee309')
    
#    procttl_de309b,nonlist_de309b,avg2_de309b,out_flag_de309b,nde309b_name,lde309b_name,linear_flagb = \
#        VV_outprocess.jobprocess(reg_test + '/bench/dome30/evolving/' + data_dir + '/gnu.JFNK.9proc', 'domee309b')
    
# create iteration plot
#    dome30e_iter = ''+ ncl_path + '/solver_iterations.ncl'
#    nfile   = 'nfile = "' + test_suite + '/livv/data' + nde309_name + '"'
#    lfile   = 'lfile = "' + test_suite + '/livv/data' + lde309_name + '"'
#    nbfile  = 'nbfile = "' + test_suite + '/livv/data' + nde309b_name + '"'
#    lbfile  = 'lbfile = "' + test_suite + '/livv/data' + lde309b_name + '"'
#    png     = 'PNG = "' + ncl_path + '/dome30e9_iter"'
#    name    = 'name = "Dome 30x30, 9 Processors"'
#    iter_dome30e = "ncl '" + nfile + "'  '" + lfile + "'  '" + nbfile + "'  '" + lbfile +\
#                    "' '" + png + "' '" + name + "'  '" + dome30e_iter + "' >> iter_details.out"
#    try:
#        subprocess.check_call(iter_dome30e, shell=True)
#        #print "creating evolving dome 30 iteration plots"
#    except subprocess.CalledProcessError as e:
#        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#        exit(e.returncode)
#    except OSError as e:
#        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#        exit(e.errno)

# delete old dome30 pic in www file
#    if (html_path + '/dome30e9_iter.png'):
#        dome30eitermove = ["rm", "-f", html_path+"/dome30e9_iter.png"]
#        try:
#            subprocess.check_call(dome30eitermove)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)

# transferring new dome30 pic to www file
#    if (ncl_path + '/dome30e9_iter.png'):
#        dome30eiterpic = ["mv", "-f", ncl_path+"/dome30e9_iter.png", html_path+"/"]
#        try:
#            subprocess.check_call(dome30eiterpic)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)

#    solver_file.write('<OBJECT data="dome30e9_iter.png" type="image/png" width="800" height="600" hspace=5 align=center">\n')
#    solver_file.write('</OBJECT>\n')

#    solver_file.write('<H4>New Run: gnu.JFNK.9proc</H4>')
#    solver_file.write("Number of Processors = " + str(procttl_de309[-1]) + "<BR>\n")
#    solver_file.write("Number of Nonlinear Iterations = ")
#    VV_utilities.format(solver_file, nonlist_de309)
#    solver_file.write('<BR>\n')

#    if out_flag_de309 == 1:
#        solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
#    solver_file.write("Average Number of Linear Iterations per Time-Step = ")
#    if linear_flag == 1:   
#       VV_utilities.format(solver_file, avg2_de309)
#   else:
#       solver_file.write("Linear Iterations not displayed in the output file")
#    solver_file.write('<BR> \n')

#    solver_file.write('<H4>Benchmark Run: gnu.JFNK.9proc</H4>')
#    solver_file.write("Number of Processors = " + str(procttl_de309b[-1]) + "<BR>\n")
#    solver_file.write("Number of Nonlinear Iterations = ")
#   if linear_flagb == 1:
#       VV_utilities.format(solver_file, nonlist_de309b)
#   else:
#       solver_file.write("Linear Iterations not displayed in the output file")
#    solver_file.write('<BR>\n')

#    if out_flag_de309b == 1:
#        solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
#    solver_file.write("Average Number of Linear Iterations per Time-Step = ")
#    VV_utilities.format(solver_file, avg2_de309b)
#    solver_file.write('<BR> \n')
#    solver_file.write('<BR> \n')
#    solver_file.write('<BR> \n')

# JFNK gnu 15 proc

# Failure checking
    failedt2 = VV_checks.failcheck(reg_test, '/dome30/evolving/' + data_dir + '/gnu.JFNK.15proc')
    failedt_list.append(failedt2)

    procttl_de3015,nonlist_de3015,avg2_de3015,out_flag_de3015,nde3015_name,lde3015_name,linear_flag = \
        VV_outprocess.jobprocess(reg_test + '/dome30/evolving/' + data_dir + '/gnu.JFNK.15proc', 'domee3015')

    procttl_de3015b,nonlist_de3015b,avg2_de3015b,out_flag_de3015b,nde3015b_name,lde3015b_name,linear_flagb = \
        VV_outprocess.jobprocess(reg_test + '/bench/dome30/evolving/' + data_dir + '/gnu.JFNK.15proc', 'domee3015b')

# create iteration plot
    dome30e_iter = ''+ ncl_path + '/solver_iterations.ncl'
    nfile    = 'nfile = "' + test_suite + '/livv/data' + nde3015_name + '"'
    lfile    = 'lfile = "' + test_suite + '/livv/data' + lde3015_name + '"'
    nbfile   = 'nbfile = "' + test_suite + '/livv/data' + nde3015b_name + '"'
    lbfile   = 'lbfile = "' + test_suite + '/livv/data' + lde3015b_name + '"'
    png      = 'PNG = "' + ncl_path + '/dome30e15_iter"'
    name     = 'name = "Dome 30x30, 15 Processors"'
    iter_dome30e = "ncl '" + nfile + "'  '" + lfile + "'  '" + nbfile + "'  '" + lbfile +\
                    "' '" + png + "' '" + name + "'  '" + dome30e_iter + "' >> iter_details.out"
    try:
        subprocess.check_call(iter_dome30e, shell=True)
        #print "creating evolving dome 30 iteration plots"
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)

# delete old dome30 pic in www file
    if (html_path + '/dome30e15_iter.png'):
        dome30eitermove = ["rm", "-f", html_path+"/dome30e15_iter.png"]
        try:
            subprocess.check_call(dome30eitermove)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# transferring new dome30 pic to www file
    if (ncl_path + '/dome30e15_iter.png'):
        dome30eiterpic = ["mv", "-f", ncl_path+"/dome30e15_iter.png", html_path+"/"]
        try:
            subprocess.check_call(dome30eiterpic)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

    solver_file.write('<OBJECT data="dome30e15_iter.png" type="image/png" width="800" height="600" hspace=5 align=center">\n')
    solver_file.write('</OBJECT>\n')

    solver_file.write('<H4>New Run: gnu.JFNK.15proc</H4>')
    solver_file.write("Number of Processors = " + str(procttl_de3015[-1]) + "<BR>\n")
    solver_file.write("Number of Nonlinear Iterations = ")
    VV_utilities.format(solver_file, nonlist_de3015)
    solver_file.write('<BR>\n')
    
    if out_flag_de3015 == 1:
        solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
    solver_file.write("Average Number of Linear Iterations per Time-Step = ")
    if linear_flag == 1:
        VV_utilities.format(solver_file, avg2_de3015)
    else:
        solver_file.write("Linear Iterations not displayed in the output file ")
    solver_file.write('<BR> \n')

    solver_file.write('<H4>Benchmark Run: gnu.JFNK.15proc</H4>')
    solver_file.write("Number of Processors = " + str(procttl_de3015b[-1]) + "<BR>\n")
    solver_file.write("Number of Nonlinear Iterations = ")
    VV_utilities.format(solver_file, nonlist_de3015b)
    solver_file.write('<BR>\n')
    
    if out_flag_de3015b == 1:
        solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
    solver_file.write("Average Number of Linear Iterations per Time-Step = ")
    if linear_flagb == 1:
        VV_utilities.format(solver_file, avg2_de3015b)
    else:
        solver_file.write("Linear Iterations not displayed in the output file ")
    solver_file.write('<BR> <BR>\n')

    solver_file.write('</HTML>\n')
    solver_file.close()

    if 1 in failedt_list:
        failedt = 1
    else:
        failedt = 0

    return failedt

def dplot(glide_flag,plot_file,reg_test,ncl_path,html_path,script_path,data_dir):  # using data, fill the web page with info 
    
    plot_file.write('<HTML>\n')
    plot_file.write('<BODY BGCOLOR="#CADFE0">\n')
    plot_file.write('<H3>Diagnostic Dome 30 Plot Details:</H3>')

# creating dome 30d velocity plot
    if glide_flag == 1:
        dome30dvel_plotfile = ''+ ncl_path + '/dome30/dome30dvel.ncl'
        stock1      = 'STOCK1 = addfile(\"'+ reg_test + '/bench/dome30/diagnostic/' + data_dir + '/dome.1.nc\", \"r\")'
        stock4      = 'STOCK4 = addfile(\"'+ reg_test + '/bench/dome30/diagnostic/' + data_dir + '/dome.4.nc\", \"r\")'
        VAR1        = 'VAR1 = addfile(\"' + reg_test + '/dome30/diagnostic/' + data_dir + '/dome.1.nc\", \"r\")'
        VAR4        = 'VAR4 = addfile(\"' + reg_test + '/dome30/diagnostic/' + data_dir + '/dome.4.nc\", \"r\")'
        pngnamevel  = 'dome30dvel.png'
        png         = 'PNG = "' + ncl_path + '/' + pngnamevel + '"'
        plot_dome30dvel = "ncl '" + stock1 + "'  '" + stock4 + "'  '" + VAR1 + "' '" + VAR4 + \
                    "' '" + png + "' " + dome30dvel_plotfile + " >> plot_details.out"
    else:
        dome30dvel_plotfile = ''+ ncl_path + '/dome30/dome30dvel.ncl'
        stock1      = 'STOCK1 = addfile(\"'+ reg_test + '/bench/dome30/diagnostic/' + data_dir + '/dome.1.glissade.nc\", \"r\")'
        stock4      = 'STOCK4 = addfile(\"'+ reg_test + '/bench/dome30/diagnostic/' + data_dir + '/dome.4.glissade.nc\", \"r\")'
        VAR1        = 'VAR1 = addfile(\"' + reg_test + '/dome30/diagnostic/' + data_dir + '/dome.1.glissade.nc\", \"r\")'
        VAR4        = 'VAR4 = addfile(\"' + reg_test + '/dome30/diagnostic/' + data_dir + '/dome.4.glissade.nc\", \"r\")'
        pngnamevel  = 'dome30dvelg.png'
        png         = 'PNG = "' + ncl_path + '/' + pngnamevel + '"'
        plot_dome30dvel = "ncl '" + stock1 + "'  '" + stock4 + "'  '" + VAR1 + "' '" + VAR4 + \
                    "' '" + png + "' " + dome30dvel_plotfile + " >> plot_details.out"
    try:
        subprocess.check_call(plot_dome30dvel, shell=True)
        #print "creating diagnostic dome 30 velocity plots"
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)

# delete old dome30 pic in www file

    if (html_path + '/' + pngnamevel):
        dome30dvelmove = ["rm", "-f", html_path+'/'+pngnamevel]
        try:
            subprocess.check_call(dome30dvelmove)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# transferring new dome30 pic to www file

    if (ncl_path + '/' + pngnamevel):
        dome30dvelpic = ["mv", "-f", ncl_path+"/"+pngnamevel, html_path+"/"]
        try:
            subprocess.check_call(dome30dvelpic)
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
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].t    b_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].t    b_lineno))
#            exit(e.errno)

    plot_file.write('<HTML>\n')
    plot_file.write('<TITLE>Diagnostic Dome 30 </TITLE>\n')
    plot_file.write('<TABLE>\n')
    plot_file.write('<TR>\n')
    plot_file.write('<H4>Difference from Benchmark for 1 and 4 Processors, Velocity Norm </H4>\n')
    plot_file.write('<OBJECT data="' + pngnamevel + '" type="image/png" width="1100" height="800" hspace=5 align=left alt="Dome 30 Plots">\n')
    plot_file.write('</OBJECT>\n')
    plot_file.write('<TR>\n')
    plot_file.write('<BR>\n')
    plot_file.write('</TABLE>\n')
    plot_file.write('</HTML>\n')
    plot_file.close()

def eplot(glide_flag,plot_file,reg_test,ncl_path,html_path,script_path,data_dir):  # using data, fill the web page with info

    plot_file.write('<HTML>\n')
    plot_file.write('<BODY BGCOLOR="#CADFE0">\n')
    plot_file.write('<H3>Evolving Dome 30 Plot Details:</H3>')

# creating dome 30e velocity plot
    if glide_flag == 1:
        dome30evel_plotfile = ''+ ncl_path + '/dome30/dome30evel.ncl'
        stock9      = 'STOCK9 = addfile(\"'+ reg_test + '/bench/dome30/evolving/' + data_dir + '/dome.9.nc\", \"r\")'
        stock15     = 'STOCK15 = addfile(\"'+ reg_test + '/bench/dome30/evolving/' + data_dir + '/dome.15.nc\", \"r\")'
        VAR9        = 'VAR9 = addfile(\"' + reg_test + '/dome30/evolving/' + data_dir + '/dome.9.nc\", \"r\")'
        VAR15       = 'VAR15 = addfile(\"' + reg_test + '/dome30/evolving/' + data_dir + '/dome.15.nc\", \"r\")'
        pngnamevel  = 'dome30evel.png'
        png         = 'PNG = "' + ncl_path + '/' + pngnamevel + '"'
        plot_dome30evel = "ncl '" + stock9 + "'  '" + stock15 + "'  '" + VAR9 + "' '" + VAR15 + \
                    "' '" + png + "' " + dome30evel_plotfile + " >> plot_details.out"
    else:
        dome30evel_plotfile = ''+ ncl_path + '/dome30/dome30evel.ncl'
        stock9      = 'STOCK9 = addfile(\"'+ reg_test + '/bench/dome30/evolving/' + data_dir + '/dome.9.glissade.nc\", \"r\")'
        stock15     = 'STOCK15 = addfile(\"'+ reg_test + '/bench/dome30/evolving/' + data_dir + '/dome.15.glissade.nc\", \"r\")'
        VAR9        = 'VAR9 = addfile(\"' + reg_test + '/dome30/evolving/' + data_dir + '/dome.9.glissade.nc\", \"r\")'
        VAR15       = 'VAR15 = addfile(\"' + reg_test + '/dome30/evolving/' + data_dir + '/dome.15.glissade.nc\", \"r\")'
        pngnamevel  = 'dome30evelg.png'
        png         = 'PNG = "' + ncl_path + '/' + pngnamevel + '"'
        plot_dome30evel = "ncl '" + stock9 + "'  '" + stock15 + "'  '" + VAR9 + "' '" + VAR15 + \
                    "' '" + png + "' " + dome30evel_plotfile + " >> plot_details.out"

    try:
        subprocess.check_call(plot_dome30evel, shell=True)
        #print "creating evolving dome 30 velocity plots"
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)
        
# delete old dome30 pic in www file

    if (html_path + '/' + pngnamevel):
        dome30evelmove = ["rm", "-f", html_path+"/" + pngnamevel]
        try:
            subprocess.check_call(dome30evelmove)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# transferring dome30 pic to www file

    if (ncl_path + '/' + pngnamevel):
        dome30evelpic = ["mv", "-f", ncl_path+"/" + pngnamevel, html_path+"/"]
        try:
            subprocess.check_call(dome30evelpic)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# creating dome 30e thickness plot
    if glide_flag == 1:
        dome30ethk_plotfile = ''+ ncl_path + '/dome30/dome30ethk.ncl'
        stock9      = 'STOCK9 = addfile(\"'+ reg_test + '/bench/dome30/evolving/' + data_dir + '/dome.9.nc\", \"r\")'
        stock15     = 'STOCK15 = addfile(\"'+ reg_test + '/bench/dome30/evolving/' + data_dir + '/dome.15.nc\", \"r\")'
        VAR9        = 'VAR9 = addfile(\"' + reg_test + '/dome30/evolving/' + data_dir + '/dome.9.nc\", \"r\")'
        VAR15       = 'VAR15 = addfile(\"' + reg_test + '/dome30/evolving/' + data_dir + '/dome.15.nc\", \"r\")'
        pngnamethk  = 'dome30ethk.png'
        png         = 'PNG = "' + ncl_path + '/' + pngnamethk + '"'
        plot_dome30ethk = "ncl '" + stock9 + "'  '" + stock15 + "'  '" + VAR9 + "' '" + VAR15 + \
                    "' '" + png + "' " + dome30ethk_plotfile + " >> plot_details.out"
    else:
        dome30ethk_plotfile = ''+ ncl_path + '/dome30/dome30ethk.ncl'
        stock9      = 'STOCK9 = addfile(\"'+ reg_test + '/bench/dome30/evolving/' + data_dir + '/dome.9.glissade.nc\", \"r\")'
        stock15     = 'STOCK15 = addfile(\"'+ reg_test + '/bench/dome30/evolving/' + data_dir + '/dome.15.glissade.nc\", \"r\")'
        VAR9        = 'VAR9 = addfile(\"' + reg_test + '/dome30/evolving/' + data_dir + '/dome.9.glissade.nc\", \"r\")'
        VAR15       = 'VAR15 = addfile(\"' + reg_test + '/dome30/evolving/' + data_dir + '/dome.15.glissade.nc\", \"r\")'
        pngnamethk  = 'dome30ethkg.png'
        png         = 'PNG = "' + ncl_path + '/' + pngnamethk + '"'
        plot_dome30ethk = "ncl '" + stock9 + "'  '" + stock15 + "'  '" + VAR9 + "' '" + VAR15 + \
                    "' '" + png + "' " + dome30ethk_plotfile + " >> plot_details.out"
    try:
        subprocess.check_call(plot_dome30ethk, shell=True)
        #print "creating evolving dome 30 thickness plots"
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)

# delete old dome30 pic in www file

    if (html_path + '/' + pngnamethk):
        dome30ethkmove = ["rm", "-f", html_path+"/" + pngnamethk]
        try:
            subprocess.check_call(dome30ethkmove)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# transferring dome30 pic to www file

    if (ncl_path + '/' + pngnamethk):
        dome30ethkpic = ["mv", "-f", ncl_path+"/" + pngnamethk, html_path+"/"]
        try:
            subprocess.check_call(dome30ethkpic)
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
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].t    b_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].t    b_lineno))
#            exit(e.errno)

    plot_file.write('<HTML>\n')
    plot_file.write('<TITLE>Evolving Dome 30 </TITLE>\n')
    plot_file.write('<TABLE>\n')
    plot_file.write('<TR>\n')
    plot_file.write('<H4>Difference from Benchmark for 9 and 15 Processors, Velocity Norm and Thickness </H4>\n')
    plot_file.write('<OBJECT data="' + pngnamevel + '" type="image/png" width="1100" height="800" hspace=5 align=left alt="Evolving Dome 30 Velocity and Thickness Plots    ">\n')
    plot_file.write('</OBJECT>\n')
    plot_file.write('<OBJECT data="' + pngnamethk + '" type="image/png" width="1100" height="800" hspace=5 align=left alt="Evolving Dome 30 Velocity and Thickness Plots    ">\n')
    plot_file.write('</OBJECT>\n')
    plot_file.write('<TR>\n')
    plot_file.write('<BR>\n')
    plot_file.write('</TABLE>\n')
    plot_file.write('</HTML>\n')
    plot_file.close()

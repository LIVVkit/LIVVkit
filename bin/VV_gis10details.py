#!/usr/bin/env

import sys
import os
from optparse import OptionParser
import subprocess
import collections
import VV_outprocess
import VV_utilities
import VV_checks

def details(solver_file,test_suite,reg_test,ncl_path,html_path,data_dir):  # using data, fill the web page with info
        
    failedt_list = []
    solver_file.write('<HTML>\n')
    solver_file.write('<BODY BGCOLOR="#CADFE0">\n')
    solver_file.write('<H3>GIS 10km Iteration Count Details:</H3>')
    solver_file.write('<BR> \n')

# JFNK multiple procs

# Failure checking
    failedt1 = VV_checks.failcheck(reg_test, '/gis_10km/' + data_dir + '/gis_10km.JFNK.trilinos.10.gnu.out')
    failedt_list.append(failedt1)

    procttl_gis10d, nonlist_gis10d, avg2_gis10d, out_flag_gis10d, ndg102_name, ldg102_name = \
        VV_outprocess.jobprocess(reg_test + '/gis_10km/' + data_dir + '/gis_10km.JFNK.trilinos.10.gnu.out','gis10km2')

    procttl_gis10b, nonlist_gis10b, avg2_gis10b, out_flag_gis10b, ndg102b_name, ldg102b_name = \
        VV_outprocess.jobprocess(reg_test + '/bench/gis_10km/'+ data_dir + '/gis_10km.JFNK.trilinos.10.gnu.out','gis10km2b')

# create iteration plots for production simulation
    gis10km_iter = ''+ ncl_path + '/solver_iterations.ncl'
    nfile   = 'nfile = "' + test_suite + '/livv/data' + ndg102_name + '"'
    lfile   = 'lfile = "' + test_suite + '/livv/data' + ldg102_name + '"' 
    nbfile  = 'nbfile = "' + test_suite + '/livv/data/' + ndg102b_name + '"'
    lbfile  = 'lbfile = "' + test_suite + '/livv/data/' + ldg102b_name + '"'
    png     = 'PNG = "' + ncl_path + '/gis10km_iter"'
    name    = 'name = "GIS 10km, 2 Processors"'
    iter_gis10km = "ncl '" + nfile + "'  '" + lfile + "'  '" + nbfile + "'  '" + lbfile + \
                    "' '" + png + "' '" + name + "'  '" + gis10km_iter + "' >> iter_details.out"
    try:                
        subprocess.check_call(iter_gis10km, shell=True)
        #print "creating gis 10km iteration plots"
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno) 

# delete old gis 10km pic in www file
    if (html_path + '/gis10km_iter.png'):
        gis10kmitermove = ["rm", "-f", html_path+"/gis10km_iter.png"]
        try:
            subprocess.check_call(gis10kmitermove)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# transferring new gis 10km pic to www file
    if (ncl_path + '/gis10km_iter.png'):
        gis10kmiterpic = ["mv", "-f", ncl_path+"/gis10km_iter.png", html_path+"/"]
        try:
            subprocess.check_call(gis10kmiterpic)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

    solver_file.write('<OBJECT data="gis10km_iter.png" type="image/png" width="800" height="600" hspace=5 align=center">\n')
    solver_file.write('</OBJECT>\n')

# also present data in list form
    solver_file.write('<H4>New Run: gis_10km.JFNK.trilinos.10.gnu.out</H4>')
    solver_file.write("Number of Processors = " + str(procttl_gis10d[-1]) + "<BR>\n")
    solver_file.write("Number of Nonlinear Iterations = ")
    VV_utilities.format(solver_file, nonlist_gis10d)
    solver_file.write('<BR>\n')
    if out_flag_gis10d == 1:
        solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
    solver_file.write("Average Number of Linear Iterations per Time-Step = ")
    VV_utilities.format(solver_file, avg2_gis10d)
    solver_file.write('<BR> \n')

    solver_file.write('<H4>Benchmark Run: gis_10km.JFNK.trilinos.10.gnu.out</H4>')
    solver_file.write("Number of Processors = " + str(procttl_gis10b[-1]) + "<BR>\n")
    solver_file.write("Number of Nonlinear Iterations = ")
    VV_utilities.format(solver_file, nonlist_gis10b)
    solver_file.write('<BR>\n')
    if out_flag_gis10b == 1:
        solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
    solver_file.write("Average Number of Linear Iterations per Time-Step = ")
    VV_utilities.format(solver_file, avg2_gis10b)
    solver_file.write('<BR> \n')

    solver_file.write('</HTML>\n')
    solver_file.close()

    if 1 in failedt_list:
        failedt = 1
    else:
        failedt = 0

    return failedt

def gis10_plot(plot_file,reg_test,ncl_path,html_path,script_path,data_dir):  # using data, fill the web page with info

    tmpath = reg_test + '/gis_10km/' + data_dir + '/gis_10km.seacism.nc'
    if VV_checks.emptycheck(tmpath) == 0:
        return

        plot_file.write('<HTML>\n')
        plot_file.write('<BODY BGCOLOR="#CADFE0">\n')
        plot_file.write('<H3>GIS 10km Plot Details:</H3>')

# formulate gis10km velocity norm plot            
        gis10kmvel_plotfile = ''+ ncl_path + '/gis10kmvel.ncl'
        stockcism   = 'STOCKcism = addfile(\"'+ reg_test + '/bench/gis_10km/' + data_dir + '/gis_10km.seacism.nc\", \"r\")'
        stockcism10 = 'STOCKcism10 = addfile(\"'+ reg_test + '/bench/gis_10km/' + data_dir + '/gis_10km.seacism.10.nc\", \"r\")'
        VARcism     = 'VARcism = addfile(\"' + reg_test + '/gis_10km/' + data_dir + '/gis_10km.seacism.nc\", \"r\")'
        VARcism10   = 'VARcism10 = addfile(\"' + reg_test + '/gis_10km/' + data_dir + '/gis_10km.seacism.10.nc\", \"r\")'
        png         = 'PNG = "' + ncl_path + '/gis10kmvel"'
        plot_gis10kmvel = "ncl '" + stockcism + "'  '" + stockcism10 + "'  '" + VARcism + "'  '" + VARcism10 \
                        + "' '" + png + "' " + gis10kmvel_plotfile + " >> plot_details.out"

        try:
            subprocess.check_call(plot_gis10kmvel, shell=True)
            #print "creating gis 10km velocity norm plot"
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# delete old gis10km vel pic in www file
        if (html_path + '/gis10kmvel.png'):
            gis10velmove = ["rm", "-f", html_path+"/gis10kmvel.png"]
            try:
                subprocess.check_call(gis10velmove)
            except subprocess.CalledProcessError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                        + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.returncode)
            except OSError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                        + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.errno)

# transferring velocity pic to www file
        if (ncl_path + '/gis10kmvel.png'):
            gispicvel = ["mv", "-f", ncl_path+"/gis10kmvel.png", html_path+"/"]
            try:
                subprocess.check_call(gispicvel)
            except subprocess.CalledProcessError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.returncode)
            except OSError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.errno)

# formulate gis10km thickness plot
        gis10kmthk_plotfile = ''+ ncl_path + '/gis10kmthk.ncl'
        stockcism   = 'STOCKcism = addfile(\"'+ reg_test + '/bench/gis_10km/' + data_dir + '/gis_10km.seacism.nc\", \"r\")'
        stockcism10 = 'STOCKcism10 = addfile(\"'+ reg_test + '/bench/gis_10km/' + data_dir + '/gis_10km.seacism.10.nc\", \"r\")'
        stockcrop   = 'STOCKcrop = addfile(\"'+ reg_test + '/bench/gis_10km/' + data_dir + '/gis_10km.051011.crop.nc\", \"r\")'
        VARcism     = 'VARcism = addfile(\"' + reg_test + '/gis_10km/' + data_dir + '/gis_10km.seacism.nc\", \"r\")'
        VARcism10   = 'VARcism10 = addfile(\"' + reg_test + '/gis_10km/' + data_dir + '/gis_10km.seacism.10.nc\", \"r\")'
        VARcrop     = 'VARcrop = addfile(\"'+ reg_test + '/gis_10km/' + data_dir + '/gis_10km.051011.crop.nc\", \"r\")'
        png         = 'PNG = "' + ncl_path + '/gis10kmthk"'
        plot_gis10kmthk = "ncl '" + stockcism + "'  '" + stockcism10 + "'  '" + stockcrop + "'  '" + VARcism + "'  '" + VARcism10 + "' '" + VARcrop \
                        + "'  '" + png + "' " + gis10kmthk_plotfile + " >> plot_details.out"

        try:
            subprocess.check_call(plot_gis10kmthk, shell=True)
            #print "creating gis 10km thickness plot"
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# delete old gis10km thk pic in www file
        if (html_path + '/gis10kmthk.png'):
            gis10thkmove = ["rm", "-f", html_path+"/gis10kmthk.png"]
            try:
                subprocess.check_call(gis10thkmove)
            except subprocess.CalledProcessError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                        + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.returncode)
            except OSError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                        + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.errno)

# transferring thickness pic to www file
        if (ncl_path + '/gis10kmthk.png'):
            gispicthk = ["mv", "-f", ncl_path+"/gis10kmthk.png", html_path+"/"]
            try:
                subprocess.check_call(gispicthk)
            except subprocess.CalledProcessError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                        + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.returncode)
            except OSError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                        + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.errno)

# remove plot_details.out
#        if (script_path + '/plot_details.out'):
#            cleantrash = ["rm", "-f", script_path+"/plot_details.out"]
#            try:
#                subprocess.check_call(cleantrash)
#            except subprocess.CalledProcessError as e:
#                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                       + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#                exit(e.returncode)
#            except OSError as e:
#                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                       + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#                exit(e.errno) 

        plot_file.write('<HTML>\n')
        plot_file.write('<TITLE>GIS 10km Test Case </TITLE>\n')
        plot_file.write('<TABLE>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<H4>Difference from benchmark for a range of processor counts for a range of variables</H4>\n')
        plot_file.write('<OBJECT data="gis10kmvel.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="GIS 10km Plots PNG">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<OBJECT data="gis10kmthk.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="GIS 10km Plots PNG">\n')
        plot_file.write('</OBJECT>\n')
        plot_file.write('<TR>\n')
        plot_file.write('<BR>\n')
        plot_file.write('</TABLE>\n')
        plot_file.write('</HTML>\n')
        plot_file.close()

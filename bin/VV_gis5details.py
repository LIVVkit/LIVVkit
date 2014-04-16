#!/usr/bin/env

import sys 
import os
from optparse import OptionParser
import subprocess
import collections
import VV_outprocess
import VV_utilities
import VV_checks

def details(solver_file,perf_test,bench_data):  # using data, fill the web page with info
        
    failedt_list = []
    solver_file.write('<HTML>\n')
    solver_file.write('<BODY BGCOLOR="#CADFE0">\n')
    solver_file.write('<H3>GIS 5km Iteration Count Details:</H3>')
    solver_file.write('<BR> \n')
                        
# Failure checking
    failedt1 = VV_checks.failcheck(perf_test, '/gis_5km/data/out.gnu')
    failedt_list.append(failedt1)

    procttl_gis5d,nonlist_gis5d,avg2_gis5d,out_flag_gis5d,ndg102_name,ldg102_name,linear_flag = \
        VV_outprocess.jobprocess(perf_test + '/gis_5km/data/out.gnu','gis5km')
    procttl_gis5b,nonlist_gis5b,avg2_gis5b,out_flag_gis5b,ndg102b_name,ldg102b_name,linear_flagb = \
        VV_outprocess.jobprocess(perf_test + '/bench/gis_5km/'+ bench_data + '/out.gnu','gis5kmb')

# create iteration plots for proudction simulation
#    data_script=ncl_path + "/solver_gis5.ncl" 
#    plot_gis5_data = "ncl 'nfile=\"" + data_path + "" + ndg102_name + "\"'" + ' ' + \
#                     "'lfile=\"" + data_path + "" + ldg102_name + "\"'" + ' ' + \
#                     "'nbfile=\"" + data_path + "" + ndg102b_name + "\"'" + ' ' + \
#                     "'lbfile=\"" + data_path + "" + ldg102b_name + "\"'" + ' ' + \
#                     "'PNG=\"" + ncl_path + "/gis5km_iter\"'" + ' ' + \
#                    data_script + ' ' + "1> /dev/null"
#    try:
#        output = subprocess.call(plot_gis5_data)
#    except:
#        print "error formatting iteration plot of gis5km run"
#        raise

#transferring iteration plot to www location
#    if (ncl_path + '/gis5km_iter.png'):
#        iterpic = "mv -f " + ncl_path + "/gis5km_iter.png" + " " + target_html + "/"
#        try:
#            output = subprocess.call(iterpic)
#        except:
#            print "error moving iter png file"
#            raise

#    solver_file.write('<TABLE>\n')
#    solver_file.write('<TR>\n') 
#    solver_file.write('<H4>Iteration Count for Nonlinear and Linear Solver</H4>\n')
#    solver_file.write('<OBJECT data="gis5km_iter.png" type="image/png" width="1300" height="800" hspace=10 align=left alt="Solver Plots">\n')
#    solver_file.write('</OBJECT>\n')
#    solver_file.write('<TR>\n')
#    solver_file.write('<BR>\n')
#    solver_file.write('</TABLE>\n')

# also present data in list form
#    if fatal_flag == 1:
#        solver_file.write('<H4>Fatal Error Found in Output File</H4>\n')

    solver_file.write('<H4>New Run: out.gnu</H4>')
    solver_file.write("Number of Processors = " + str(procttl_gis5d[-1]) + "<BR>\n")
    solver_file.write("Number of Nonlinear Iterations = ")
    VV_utilities.format(solver_file, nonlist_gis5d)
    solver_file.write('<BR>\n')
    if out_flag_gis5d == 1:
        solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
    solver_file.write("Average Number of Linear Iterations per Time-Step = ")
    if linear_flag == 1:
        VV_utilities.format(solver_file, avg2_gis5d)
    else:
        solver_file.write("Linear Iterations not displayed in the output file")
    solver_file.write('<BR> \n')

    solver_file.write('<H4>Benchmark Run: out.gnu</H4>')
    solver_file.write("Number of Processors = " + str(procttl_gis5b[-1]) + "<BR>\n")
    solver_file.write("Number of Nonlinear Iterations = ")
    VV_utilities.format(solver_file, nonlist_gis5b)
    solver_file.write('<BR>\n')
    if out_flag_gis5b == 1:
        solver_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
    solver_file.write("Average Number of Linear Iterations per Time-Step = ")
    if linear_flag == 1:
        VV_utilities.format(solver_file, avg2_gis5b)
    else:
        solver_file.write("Linear Iterations not displayed in the output file")
    solver_file.write('<BR> \n')

    solver_file.write('</HTML>\n')
    solver_file.close()

    if 1 in failedt_list:
        failedt = 1
    else:
        failedt = 0

    return failedt

def gis5_plot(plot_file,perf_test,ncl_path,html_path,script_path,bench_data):  # using data, fill the web page with info

    plot_file.write('<HTML>\n')
    plot_file.write('<H3>GIS 5km Plot Details:</H3>')
                        
# formulate gis5km velocity norm plot            
    gis5kmvel_plotfile = ''+ ncl_path + '/gis5kmvel.ncl'
    stock1 = 'STOCK1 = addfile(\"'+ perf_test + '/bench/gis_5km/' + bench_data + '/gis_5km.ice2sea.1-50.nc\", \"r\")'
    stock2 = 'STOCK2 = addfile(\"'+ perf_test + '/bench/gis_5km/' + bench_data + '/gis_5km.ice2sea.51-100.nc\", \"r\")'
    VAR1   = 'VAR1 = addfile(\"' + perf_test + '/gis_5km/data/gis_5km.ice2sea.1-50.nc\", \"r\")'
    VAR2   = 'VAR2 = addfile(\"' + perf_test + '/gis_5km/data/gis_5km.ice2sea.51-100.nc\", \"r\")'
    png    = 'PNG = "' + ncl_path + '/gis5kmvel"'
    plot_gis5kmvel = "ncl '" + stock1 + "'  '" + stock2 + "'  '" + VAR1 + "'  '" + VAR2 + "'  '" \
                    + png + "' " + gis5kmvel_plotfile + " >> plot_details.out"

    try:                
        subprocess.check_call(plot_gis5kmvel, shell=True)
        print "creating gis 5km velocity norm plot"
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)
        
# delete old gis5km vel pic in www file
    if (html_path + '/gis5kmvel.png'):
        gis5velmove = ["rm", "-f", html_path+"/gis5kmvel.png"]
        try:
            subprocess.check_call(gis5velmove)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# transferring velocity pic to www file
    if (ncl_path + '/gis5kmvel.png'):
        gis5picvel = ["mv", "-f", ncl_path+"/gis5kmvel.png", html_path+"/"]
        try:
            subprocess.check_call(gis5picvel)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# formulate gis5km thickness plot
    gis5kmthk_plotfile = ''+ ncl_path + '/gis5kmthk.ncl'
    stock1 = 'STOCK1 = addfile(\"'+ perf_test + '/bench/gis_5km/' + bench_data + '/gis_5km.ice2sea.1-50.nc\", \"r\")'
    stock2 = 'STOCK2 = addfile(\"'+ perf_test + '/bench/gis_5km/' + bench_data + '/gis_5km.ice2sea.51-100.nc\", \"r\")'
    VAR1   = 'VAR1 = addfile(\"' + perf_test + '/gis_5km/data/gis_5km.ice2sea.1-50.nc\", \"r\")'
    VAR2   = 'VAR2 = addfile(\"' + perf_test + '/gis_5km/data/gis_5km.ice2sea.51-100.nc\", \"r\")'
    png    = 'PNG = "' + ncl_path + '/gis5kmthk"'
    plot_gis5kmthk = "ncl '" + stock1 + "'  '" + stock2 + "'  '" + VAR1 + "'  '" + VAR2 + "'  '" \
                    + png + "' " + gis5kmthk_plotfile + " >> plot_details.out"

    try:
        subprocess.check_call(plot_gis5kmthk, shell=True)
        print "creating gis 5km thickness plot"
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)

# delete old gis5km thk pic in www file
    if (html_path + '/gis5kmthk.png'):
        gis5thkmove = ["rm", "-f", html_path+"/gis5kmthk.png"]
        try:
            subprocess.check_call(gis5thkmove)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# transferring thickness pic to www file
    if (ncl_path + '/gis5kmthk.png'):
        gis5picthk = ["mv", "-f", ncl_path+"/gis5kmthk.png", html_path+"/"]
        try:
            subprocess.check_call(gis5picthk)
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
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)

    plot_file.write('<HTML>\n')
    plot_file.write('<TITLE>GIS 5km Test Case </TITLE>\n')
    plot_file.write('<TABLE>\n')
    plot_file.write('<TR>\n')
    plot_file.write('<H4>Difference from benchmark for Velocity Norm and Thickness</H4>\n')
    plot_file.write('<OBJECT data="gis5kmvel.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="GIS 5km Plots PNG">\n')
    plot_file.write('</OBJECT>\n')
    plot_file.write('<OBJECT data="gis5kmthk.png" type="image/png" width="1100" height="800" hspace=10 align=left alt="GIS 5km Plots PNG">\n')
    plot_file.write('</OBJECT>\n')
    plot_file.write('<TR>\n')
    plot_file.write('<BR>\n')
    plot_file.write('</TABLE>\n')
    plot_file.write('</HTML>\n')
    plot_file.close()

#!/usr/bin/env

import sys
import os
from optparse import OptionParser
import subprocess
import collections
import VV_outprocess
import VV_utilities
from stat import *
import time

def web(valid_file,details_file,figure1_plot,figure2_plot,figure3_plot,figure4_plot,figure5_plot, \
        data_dir,ncl_path,html_path,script_path):

    valid_file.write('<HTML>\n')
    valid_file.write('<TITLE>Validation Plots</TITLE>\n')
    valid_file.write('<BODY BGCOLOR="#CADFE0">\n')
    valid_file.write('<H1>Validation Plots</H1>')
    valid_file.write('<BR>\n')

    valid_file.write('<TH ALIGN=LEFT><A HREF="case_details.html">Case Details</A>\n')
    valid_file.write('<BR>\n')
    valid_file.write('<BR>\n')
    
    
    
    
    
    
    
    valid_file.write('<TH ALIGN=LEFT><A HREF="figure1_plot.html">Figure1 Plot</A>\n')
    valid_file.write('<BR>\n')
   
    figure1_plotfile = '' + ncl_path + '/validation/figure1.ncl'
    pngnamefigure1   = 'figure1.png' 
    png              = 'PNG = "' + ncl_path + '/' + pngnamefigure1 + '"'
    plot_figure1     = "ncl '" + png + "'  " + figure1_plotfile + " >> valid_details.out"
    
    try:
        subprocess.check_call(plot_figure1, shell=True)
        print "creating figure 1 plot"
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)

# delete old figure1 pic in www file
    if (html_path + '/' + pngnamefigure1):
        figure1move = ["rm", "-f", html_path+'/'+pngnamefigure1]
        try:
            subprocess.check_call(figure1move)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# transferring new figure1 pic to www file
    if (ncl_path + '/' + pngnamefigure1):
        figure1pic = ["mv", "-f", ncl_path+"/"+pngnamefigure1, html_path+"/"]
        try:
            subprocess.check_call(figure1pic)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

    figure1_plot.write('<HTML>\n')
    figure1_plot.write('<TITLE>Figure1 Plot </TITLE>\n')
    figure1_plot.write('<TABLE>\n')
    figure1_plot.write('<TR>\n')
    figure1_plot.write('<H4>Figure1 Plot </H4>\n')
    figure1_plot.write('<OBJECT data="' + pngnamefigure1 + '" type="image/png" width="1100" height="800" hspace=5 align=left alt="Figure 1 Plot">\n')
    figure1_plot.write('</OBJECT>\n')
    figure1_plot.write('<TR>\n')
    figure1_plot.write('<BR>\n')
    figure1_plot.write('</TABLE>\n')
    figure1_plot.write('</HTML>\n')
    figure1_plot.close()

    valid_file.write('<BR>\n')
    valid_file.write('<BR>\n')
    valid_file.write('<TH ALIGN=LEFT><A HREF="figure2_plot.html">Figure2 Plot</A>\n')
    valid_file.write('<BR>\n')
   
    figure2_plotfile = '' + ncl_path + '/validation/figure2.ncl'
    pngnamefigure2   = 'figure2.png' 
    png              = 'PNG = "' + ncl_path + '/' + pngnamefigure2 + '"'
    plot_figure2     = "ncl '" + png + "'  " + figure2_plotfile + " >> valid_details.out"
    
    try:
        subprocess.check_call(plot_figure2, shell=True)
        print "creating figure 2 plot"
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)

# delete old figure2 pic in www file
    if (html_path + '/' + pngnamefigure2):
        figure2move = ["rm", "-f", html_path+'/'+pngnamefigure2]
        try:
            subprocess.check_call(figure2move)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# transferring new figure2 pic to www file
    if (ncl_path + '/' + pngnamefigure2):
        figure2pic = ["mv", "-f", ncl_path+"/"+pngnamefigure2, html_path+"/"]
        try:
            subprocess.check_call(figure2pic)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

    figure2_plot.write('<HTML>\n')
    figure2_plot.write('<TITLE>Figure2 Plot </TITLE>\n')
    figure2_plot.write('<TABLE>\n')
    figure2_plot.write('<TR>\n')
    figure2_plot.write('<H4>Figure2 Plot </H4>\n')
    figure2_plot.write('<OBJECT data="' + pngnamefigure2 + '" type="image/png" width="1100" height="800" hspace=5 align=left alt="Figure 2 Plot">\n')
    figure2_plot.write('</OBJECT>\n')
    figure2_plot.write('<TR>\n')
    figure2_plot.write('<BR>\n')
    figure2_plot.write('</TABLE>\n')
    figure2_plot.write('</HTML>\n')
    figure2_plot.close()

    valid_file.write('<BR>\n')
    valid_file.write('<BR>\n')
    valid_file.write('<TH ALIGN=LEFT><A HREF="figure3_plot.html">Figure3 Plot</A>\n')
    valid_file.write('<BR>\n')
   
    figure3_plotfile = '' + ncl_path + '/validation/figure3.ncl'
    pngnamefigure3   = 'figure3.png' 
    png              = 'PNG = "' + ncl_path + '/' + pngnamefigure3 + '"'
    plot_figure3     = "ncl '" + png + "'  " + figure3_plotfile + " >> valid_details.out"
    
    try:
        subprocess.check_call(plot_figure3, shell=True)
        print "creating figure 3 plot"
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)

# delete old figure3 pic in www file
    if (html_path + '/' + pngnamefigure3):
        figure3move = ["rm", "-f", html_path+'/'+pngnamefigure3]
        try:
            subprocess.check_call(figure3move)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# transferring new figure3 pic to www file
    if (ncl_path + '/' + pngnamefigure3):
        figure3pic = ["mv", "-f", ncl_path+"/"+pngnamefigure3, html_path+"/"]
        try:
            subprocess.check_call(figure3pic)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

    figure3_plot.write('<HTML>\n')
    figure3_plot.write('<TITLE>Figure3 Plot </TITLE>\n')
    figure3_plot.write('<TABLE>\n')
    figure3_plot.write('<TR>\n')
    figure3_plot.write('<H4>Figure3 Plot </H4>\n')
    figure3_plot.write('<OBJECT data="' + pngnamefigure3 + '" type="image/png" width="1100" height="800" hspace=5 align=left alt="Figure 3 Plot">\n')
    figure3_plot.write('</OBJECT>\n')
    figure3_plot.write('<TR>\n')
    figure3_plot.write('<BR>\n')
    figure3_plot.write('</TABLE>\n')
    figure3_plot.write('</HTML>\n')
    figure3_plot.close()

    valid_file.write('<BR>\n')
    valid_file.write('<BR>\n')
    valid_file.write('<TH ALIGN=LEFT><A HREF="figure4_plot.html">Figure4 Plot</A>\n')
    valid_file.write('<BR>\n')
   
    figure4_plotfile = '' + ncl_path + '/validation/figure4.ncl'
    pngnamefigure4   = 'figure4.png' 
    png              = 'PNG = "' + ncl_path + '/' + pngnamefigure4 + '"'
    plot_figure4     = "ncl '" + png + "'  " + figure4_plotfile + " >> valid_details.out"
    
    try:
        subprocess.check_call(plot_figure4, shell=True)
        print "creating figure 4 plot"
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)

# delete old figure4 pic in www file
    if (html_path + '/' + pngnamefigure4):
        figure4move = ["rm", "-f", html_path+'/'+pngnamefigure4]
        try:
            subprocess.check_call(figure4move)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# transferring new figure4 pic to www file
    if (ncl_path + '/' + pngnamefigure4):
        figure4pic = ["mv", "-f", ncl_path+"/"+pngnamefigure4, html_path+"/"]
        try:
            subprocess.check_call(figure4pic)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

    figure4_plot.write('<HTML>\n')
    figure4_plot.write('<TITLE>Figure4 Plot </TITLE>\n')
    figure4_plot.write('<TABLE>\n')
    figure4_plot.write('<TR>\n')
    figure4_plot.write('<H4>Figure4 Plot </H4>\n')
    figure4_plot.write('<OBJECT data="' + pngnamefigure4 + '" type="image/png" width="1100" height="800" hspace=5 align=left alt="Figure 4 Plot">\n')
    figure4_plot.write('</OBJECT>\n')
    figure4_plot.write('<TR>\n')
    figure4_plot.write('<BR>\n')
    figure4_plot.write('</TABLE>\n')
    figure4_plot.write('</HTML>\n')
    figure4_plot.close()

    valid_file.write('<BR>\n')
    valid_file.write('<BR>\n')
    valid_file.write('<TH ALIGN=LEFT><A HREF="figure5_plot.html">Figure5 Plot</A>\n')
    valid_file.write('<BR>\n')
   
    figure5_plotfile = '' + ncl_path + '/validation/figure5.ncl'
    pngnamefigure5   = 'figure5.png' 
    png              = 'PNG = "' + ncl_path + '/' + pngnamefigure5 + '"'
    plot_figure5     = "ncl '" + png + "'  " + figure5_plotfile + " >> valid_details.out"
    
    try:
        subprocess.check_call(plot_figure5, shell=True)
        print "creating figure 5 plot"
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)

# delete old figure5 pic in www file
    if (html_path + '/' + pngnamefigure5):
        figure5move = ["rm", "-f", html_path+'/'+pngnamefigure5]
        try:
            subprocess.check_call(figure5move)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

# transferring new figure5 pic to www file
    if (ncl_path + '/' + pngnamefigure5):
        figure5pic = ["mv", "-f", ncl_path+"/"+pngnamefigure5, html_path+"/"]
        try:
            subprocess.check_call(figure5pic)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

    figure5_plot.write('<HTML>\n')
    figure5_plot.write('<TITLE>Figure5 Plot </TITLE>\n')
    figure5_plot.write('<TABLE>\n')
    figure5_plot.write('<TR>\n')
    figure5_plot.write('<H4>Figure5 Plot </H4>\n')
    figure5_plot.write('<OBJECT data="' + pngnamefigure5 + '" type="image/png" width="1100" height="800" hspace=5 align=left alt="Figure 5 Plot">\n')
    figure5_plot.write('</OBJECT>\n')
    figure5_plot.write('<TR>\n')
    figure5_plot.write('<BR>\n')
    figure5_plot.write('</TABLE>\n')
    figure5_plot.write('</HTML>\n')
    figure5_plot.close()

# remove valid_details.out
#    if (script_path + '/valid_details.out'):
#        cleantrash = ["rm", "-f", script_path+"/valid_details.out"]
#        try:
#            subprocess.check_call(cleantrash)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].t    b_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].t    b_lineno))
#            exit(e.errno)

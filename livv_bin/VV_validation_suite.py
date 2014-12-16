#!/usr/bin/env

import sys
import os
from optparse import OptionParser
import subprocess
import collections
import VV_outprocess
from livv_bin import VV_test
import VV_utilities
from stat import *
import time

# Writes a standardized html file with some given options
def web(valid_file,valid_file_cam,valid_file_clm,detiails_file,table,figure1_plot,figure2_plot,figure3_plot, \
	figure4_plot,figure5_plot,data_dir,ncl_path,html_path,script_path):

    valid_file.write('<HTML>\n')
    valid_file.write('<TITLE>Validation of Continental Ice Sheet Simulation</TITLE>\n')
    valid_file.write('<BODY BGCOLOR="#CADFE0">\n')
    valid_file.write('<H1>Validation Plots</H1>')
    valid_file.write('<BR>\n')

    valid_file.write('<TH ALIGN=LEFT><A HREF="case_details.html">Case Details</A>\n')
    valid_file.write('<BR>\n')
    valid_file.write('<BR>\n')
    
    valid_file.write('<TH ALIGN=CENTER><A HREF="table.html">Table</A>\n')
    valid_file.write('<BR>\n')
  

    print "creating table"

    table.write('<HTML>\n')
    table.write('<TITLE>Table with filler values</TITLE>\n')
    table.write('<BODY BGCOLOR="#CADFE0">\n')
    table.write('<TABLE BORDER="1" solid black  WIDTH="90%" ALIGN=CENTER BGCOLOR="#ADD8E6">\n')
    table.write('<TR>\n')
    table.write('<H4 ALIGN=CENTER>Table </H4>\n')
    table.write('<TR ALIGN="CENTER">')
    table.write('<TD>Fluxes</TD>')
    table.write('<TD>CESM mean</TD>')
    table.write('<TD>CESM mean - RACMO2 mean</TD>')
    table.write('<TD>r(gf>2.0)/r(gf>0.99)</TD>')
    table.write('<TD>RMSE(gf>0/20)/RMSE(gf>0.99)</TD>')
    table.write('</TR>')
    table.write('<TR ALIGN="CENTER">')
    table.write('<TD>SW_d</TD>')
    table.write('<TD>268</TD>')
    table.write('<TD>-11</TD>')
    table.write('<TD>0.77/0.54</TD>')
    table.write('<TD>16/17</TD>')
    table.write('</TR>')
    table.write('<TR ALIGN="CENTER">')
    table.write('<TD>SW_net</TD>')
    table.write('<TD>61</TD>')
    table.write('<TD>-3</TD>')
    table.write('<TD>0.76/0.73</TD>')
    table.write('<TD>20/7</TD>')
    table.write('</TR>')
    table.write('<TR ALIGN="CENTER">')
    table.write('<TD>LW_d</TD>')
    table.write('<TD>235</TD>')
    table.write('<TD>+7</TD>')
    table.write('<TD>0.92/0.83</TD>')
    table.write('<TD>14</TD>')
    table.write('</TR>')
    table.write('<TR ALIGN="CENTER">')
    table.write('<TD>LW_net</TD>')
    table.write('<TD>-46</TD>')
    table.write('<TD>+6</TD>')
    table.write('<TD>0.51/0.71</TD>')
    table.write('<TD>9/9</TD>')
    table.write('</TR>')
    table.write('<TR ALIGN="CENTER">')
    table.write('<TD>R_net</TD>')
    table.write('<TD>15</TD>')
    table.write('<TD>+4</TD>')
    table.write('<TD>0.79/0.61</TD>')
    table.write('<TD>21</TD>')
    table.write('</TR>')
    table.write('<TR ALIGN="CENTER">')
    table.write('<TD>SHF</TD>')
    table.write('<TD>7</TD>')
    table.write('<TD>+0.2</TD>')
    table.write('<TD>0.21/0.76</TD>')
    table.write('<TD>10/5</TD>')
    table.write('</TR>')
    table.write('<TR ALIGN="CENTER">')
    table.write('<TD>LHF</TD>')
    table.write('<TD>-8</TD>')
    table.write('<TD>-3</TD>')
    table.write('<TD>0.61/0.65</TD>')
    table.write('<TD>5/4</TD>')
    table.write('</TR>')
    table.write('<TR ALIGN="CENTER">')
    table.write('<TD>GF</TD>')
    table.write('<TD>-1.4</TD>')
    table.write('<TD>-1.2</TD>')
    table.write('<TD>0.09/0.62</TD>')
    table.write('<TD>8/5</TD>')
    table.write('</TR>')


#    table.write('<OBJECT data=' + table_data+ ' type="table" width="1100" height="800" hspace=5 align=left alt="Figure 1 Plot">\n') 
#    table.write('table_data, col_align  = ['center', 'center', 'center','center','center'],col_styles = ['background-color:lightblue;','background-color:lightgreen;','background-color:pink;','background-color:purple;','background-color:yellow;']')
 
    table.write('</OBJECT>\n')
    table.write('<TR>\n')
    table.write('<BR>\n')
    table.write('</TABLE>\n')
    table.write('</HTML>\n')
    table.close()    
    
    
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
        
##############################
# NO MORE BEYOND THIS POINT  #      
##############################

# delete old figure1 pic in www file
#   if (html_path + '/' + pngnamefigure1):
#        figure1move = ["rm", "-f", html_path+'/'+pngnamefigure1]
#        try:
#            subprocess.check_call(figure1move)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)

# transferring new figure1 pic to www file
#    if (ncl_path + '/' + pngnamefigure1):
#        figure1pic = ["mv", "-f", ncl_path+"/"+pngnamefigure1, html_path+"/"]
#        try:
#            subprocess.check_call(figure1pic)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)

#    figure1_plot.write('<HTML>\n')
#    figure1_plot.write('<TITLE>Figure1 Plot </TITLE>\n')
#    figure1_plot.write('<TABLE>\n')
#    figure1_plot.write('<TR>\n')
#    figure1_plot.write('<H4>Figure1 Plot </H4>\n')
#    figure1_plot.write('<OBJECT data="' + pngnamefigure1 + '" type="image/png" width="1100" height="800" hspace=5 align=left alt="Figure 1 Plot">\n')
#    figure1_plot.write('</OBJECT>\n')
#    figure1_plot.write('<TR>\n')
#    figure1_plot.write('<BR>\n')
#    figure1_plot.write('</TABLE>\n')
#    figure1_plot.write('</HTML>\n')
#    figure1_plot.close()

#    valid_file.write('<BR>\n')
#    valid_file.write('<BR>\n')
#    valid_file.write('<TH ALIGN=LEFT><A HREF="figure2_plot.html">Figure2 Plot</A>\n')
#    valid_file.write('<BR>\n')
   
#    figure2_plotfile = '' + ncl_path + '/validation/figure2.ncl'
#    pngnamefigure2   = 'figure2.png' 
#    png              = 'PNG = "' + ncl_path + '/' + pngnamefigure2 + '"'
#    plot_figure2     = "ncl '" + png + "'  " + figure2_plotfile + " >> valid_details.out"
    
#    try:
#        subprocess.check_call(plot_figure2, shell=True)
#        print "creating figure 2 plot"
#    except subprocess.CalledProcessError as e:
#        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#        exit(e.returncode)
#    except OSError as e:
#        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#        exit(e.errno)

# delete old figure2 pic in www file
#    if (html_path + '/' + pngnamefigure2):
#        figure2move = ["rm", "-f", html_path+'/'+pngnamefigure2]
#        try:
#            subprocess.check_call(figure2move)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)

# transferring new figure2 pic to www file
#    if (ncl_path + '/' + pngnamefigure2):
#        figure2pic = ["mv", "-f", ncl_path+"/"+pngnamefigure2, html_path+"/"]
#        try:
#            subprocess.check_call(figure2pic)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)

#    figure2_plot.write('<HTML>\n')
#    figure2_plot.write('<TITLE>Figure2 Plot </TITLE>\n')
#    figure2_plot.write('<TABLE>\n')
#    figure2_plot.write('<TR>\n')
#    figure2_plot.write('<H4>Figure2 Plot </H4>\n')
#    figure2_plot.write('<OBJECT data="' + pngnamefigure2 + '" type="image/png" width="1100" height="800" hspace=5 align=left alt="Figure 2 Plot">\n')
#    figure2_plot.write('</OBJECT>\n')
#    figure2_plot.write('<TR>\n')
#    figure2_plot.write('<BR>\n')
#    figure2_plot.write('</TABLE>\n')
#    figure2_plot.write('</HTML>\n')
#    figure2_plot.close()

#    valid_file.write('<BR>\n')
#    valid_file.write('<BR>\n')
#    valid_file.write('<TH ALIGN=LEFT><A HREF="figure3_plot.html">Figure3 Plot</A>\n')
#    valid_file.write('<BR>\n')
   
#    figure3_plotfile = '' + ncl_path + '/validation/figure3.ncl'
#    pngnamefigure3   = 'figure3.png' 
#    png              = 'PNG = "' + ncl_path + '/' + pngnamefigure3 + '"'
#    plot_figure3     = "ncl '" + png + "'  " + figure3_plotfile + " >> valid_details.out"
    
#    try:
#        subprocess.check_call(plot_figure3, shell=True)
#        print "creating figure 3 plot"
#    except subprocess.CalledProcessError as e:
#        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#        exit(e.returncode)
#    except OSError as e:
#        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#        exit(e.errno)

# delete old figure3 pic in www file
#    if (html_path + '/' + pngnamefigure3):
#        figure3move = ["rm", "-f", html_path+'/'+pngnamefigure3]
#        try:
#            subprocess.check_call(figure3move)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)

# transferring new figure3 pic to www file
#    if (ncl_path + '/' + pngnamefigure3):
#        figure3pic = ["mv", "-f", ncl_path+"/"+pngnamefigure3, html_path+"/"]
#        try:
#            subprocess.check_call(figure3pic)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)

#    figure3_plot.write('<HTML>\n')
#    figure3_plot.write('<TITLE>Figure3 Plot </TITLE>\n')
#    figure3_plot.write('<TABLE>\n')
#    figure3_plot.write('<TR>\n')
#    figure3_plot.write('<H4>Figure3 Plot </H4>\n')
#    figure3_plot.write('<OBJECT data="' + pngnamefigure3 + '" type="image/png" width="1100" height="800" hspace=5 align=left alt="Figure 3 Plot">\n')
#    figure3_plot.write('</OBJECT>\n')
#    figure3_plot.write('<TR>\n')
#    figure3_plot.write('<BR>\n')
#    figure3_plot.write('</TABLE>\n')
#    figure3_plot.write('</HTML>\n')
#    figure3_plot.close()

#    valid_file.write('<BR>\n')
#    valid_file.write('<BR>\n')
#    valid_file.write('<TH ALIGN=LEFT><A HREF="figure4_plot.html">Figure4 Plot</A>\n')
#    valid_file.write('<BR>\n')
   
#    figure4_plotfile = '' + ncl_path + '/validation/figure4.ncl'
#    pngnamefigure4   = 'figure4.png' 
#    png              = 'PNG = "' + ncl_path + '/' + pngnamefigure4 + '"'
#    plot_figure4     = "ncl '" + png + "'  " + figure4_plotfile + " >> valid_details.out"
    
#    try:
#        subprocess.check_call(plot_figure4, shell=True)
#        print "creating figure 4 plot"
#    except subprocess.CalledProcessError as e:
#        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#        exit(e.returncode)
#    except OSError as e:
#        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#        exit(e.errno)

# delete old figure4 pic in www file
#    if (html_path + '/' + pngnamefigure4):
#        figure4move = ["rm", "-f", html_path+'/'+pngnamefigure4]
#        try:
#            subprocess.check_call(figure4move)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)

# transferring new figure4 pic to www file
#    if (ncl_path + '/' + pngnamefigure4):
#        figure4pic = ["mv", "-f", ncl_path+"/"+pngnamefigure4, html_path+"/"]
#        try:
#            subprocess.check_call(figure4pic)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)

#    figure4_plot.write('<HTML>\n')
#    figure4_plot.write('<TITLE>Figure4 Plot </TITLE>\n')
#    figure4_plot.write('<TABLE>\n')
#    figure4_plot.write('<TR>\n')
#    figure4_plot.write('<H4>Figure4 Plot </H4>\n')
#    figure4_plot.write('<OBJECT data="' + pngnamefigure4 + '" type="image/png" width="1100" height="800" hspace=5 align=left alt="Figure 4 Plot">\n')
#    figure4_plot.write('</OBJECT>\n')
#    figure4_plot.write('<TR>\n')
#    figure4_plot.write('<BR>\n')
#    figure4_plot.write('</TABLE>\n')
#    figure4_plot.write('</HTML>\n')
#    figure4_plot.close()

#    valid_file.write('<BR>\n')
#    valid_file.write('<BR>\n')
#    valid_file.write('<TH ALIGN=LEFT><A HREF="figure5_plot.html">Figure5 Plot</A>\n')
#    valid_file.write('<BR>\n')
   
#    figure5_plotfile = '' + ncl_path + '/validation/figure5.ncl'
#    pngnamefigure5   = 'figure5.png' 
#    png              = 'PNG = "' + ncl_path + '/' + pngnamefigure5 + '"'
#    plot_figure5     = "ncl '" + png + "'  " + figure5_plotfile + " >> valid_details.out"
    
#    try:
#        subprocess.check_call(plot_figure5, shell=True)
#        print "creating figure 5 plot"
#    except subprocess.CalledProcessError as e:
#        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#        exit(e.returncode)
#    except OSError as e:
#        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#        exit(e.errno)

# delete old figure5 pic in www file
#    if (html_path + '/' + pngnamefigure5):
#        figure5move = ["rm", "-f", html_path+'/'+pngnamefigure5]
#        try:
#            subprocess.check_call(figure5move)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)

# transferring new figure5 pic to www file
#    if (ncl_path + '/' + pngnamefigure5):
#        figure5pic = ["mv", "-f", ncl_path+"/"+pngnamefigure5, html_path+"/"]
#        try:
#            subprocess.check_call(figure5pic)
#        except subprocess.CalledProcessError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.returncode)
#        except OSError as e:
#            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
#                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
#            exit(e.errno)

#    figure5_plot.write('<HTML>\n')
#    figure5_plot.write('<TITLE>Figure5 Plot </TITLE>\n')
#    figure5_plot.write('<TABLE>\n')
#    figure5_plot.write('<TR>\n')
#    figure5_plot.write('<H4>Figure5 Plot </H4>\n')
#    figure5_plot.write('<OBJECT data="' + pngnamefigure5 + '" type="image/png" width="1100" height="800" hspace=5 align=left alt="Figure 5 Plot">\n')
#    figure5_plot.write('</OBJECT>\n')
#    figure5_plot.write('<TR>\n')
#    figure5_plot.write('<BR>\n')
#    figure5_plot.write('</TABLE>\n')
#    figure5_plot.write('</HTML>\n')
#    figure5_plot.close()

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

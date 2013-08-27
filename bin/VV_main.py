
import sys
import os
import re
from optparse import OptionParser
import subprocess
import collections
import VV_outprocess
import VV_testsuite
import VV_gisproduction

user = os.environ['USER']

#enable use input for filepaths from the command line
usage_string = "%prog [options]"
parser = OptionParser(usage=usage_string)
parser.add_option('-p', '--directory', action='store', type='string', dest='directory_path', \
                  metavar='PATH', help='path where this directory is located')
parser.add_option('-b', '--script', action='store', type='string', dest='script_path', \
                  metavar='PATH', help='path where the livv kit is located')
parser.add_option('-j', '--html', action='store', type='string', dest='html_path', \
                  metavar='PATH', help='path where the html directory is located')
parser.add_option('-l', '--link', action='store', type='string', dest='html_link', \
                  metavar='PATH', help='location of website for viewing set by user')
parser.add_option('-k', '--ncl', action='store', type='string', dest='ncl_path', \
                  metavar='PATH', help='path where the ncl directory is located')
parser.add_option('-r', '--bdata', action='store', type='string', dest='bench_data', \
                  metavar='FILE', help='file where the benchmark data files are stored')
parser.add_option('-d', '--data', action='store', type='string', dest='data_path', \
                  metavar='PATH', help='path where the solver data directory is located')
parser.add_option('-c', '--config', action='store', type='string', dest='config_file', \
                  metavar='FILE', help='the config file python will parse through')
parser.add_option('-t', '--test', action='store', type='string', dest='test_suite', \
                  metavar='TEST', help='path to location of test suite')
parser.add_option('-o', '--output', action='store', type='string', dest='output_file', \
                  metavar='FILE', help='the job output file python will parse through')
parser.add_option('-s', '--stocknc', action='store', type='string', dest='stock_netcdf_file', \
                  metavar='FILE', help='the stock NETCDF file that the ncl script will read')
parser.add_option('-n', '--variablenc', action='store', type='string', dest='variable_netcdf_file', \
                  metavar='FILE', help='the variable NETCDF file that the ncl script will read')
parser.add_option('-i', '--timestamp', action='store', type='string', dest='time_stamp', \
                  metavar='FILE', help='the current time to record in the web output')
parser.add_option('-m', '--comment', action='store', type='string', dest='comment', \
                  metavar='FILE', help='information about the test case for user reference')
parser.add_option('-u', '--username', action='store', type='string', dest='username', \
                  metavar='FILE', help='username used to create subdirectory of web pages of output')
parser.add_option('-g', '--gis_prod', action='store_true', dest='gis_prod', \
                  help='include flag to run the GIS production analysis')
parser.add_option('-x', '--xml', action='store', type='string', dest='xml_path',\
		  metavar='FILE', help='path to xml file that python will parse through')
parser.add_option('-D', '--diagnostic', action='store', type='int', dest='diagnostic_flag', \
                  metavar='FLAG', help='flag to run dome30 diagnostic test')
parser.add_option('-E', '--evolving', action='store', type='int', dest='evolving_flag', \
                  metavar='FLAG', help='flag to run dome30 evolving test')
parser.add_option('-I', '--circular-shelf', action='store', type='int', dest='circular_flag', \
                  metavar='FLAG', help='flag to run circular shelf test')
parser.add_option('-O', '--confined-shelf', action='store', type='int', dest='confined_flag', \
                  metavar='FLAG', help='flag to run confined shelf test')
parser.add_option('-A', '--ismip-hom-A80', action='store', type='int', dest='ismip_hom_a80_flag', \
                  metavar='FLAG', help='flag to run ismip hom a 80km test')
parser.add_option('-B', '--ismip-hom-A20', action='store', type='int', dest='ismip_hom_a20_flag', \
                  metavar='FLAG', help='flag to run ismip hom a 20km test')
parser.add_option('-C', '--ismip-hom-C', action='store', type='int', dest='ismip_hom_c_flag', \
                  metavar='FLAG', help='flag to run ismip hom c test')
parser.add_option('-G', '--gis10km', action='store', type='int', dest='gis_10km_flag', \
                  metavar='FLAG', help='flag to run gis10km test')
#parser.add_option('-a', '--ant_prod', action='store_true', dest='ant_prod', \
#                  help='include flag to run the ANT production analysis')

#parse the command line options and arguments and store in lists
(options, args) = parser.parse_args()

if (options.gis_prod):
	if (options.stock_netcdf_file):
		stock_nc = options.stock_netcdf_file 
	else:
		print "need a benchmark GIS file for production analysis"
	        exit()

	if (options.variable_netcdf_file):
        	variable_nc = options.variable_netcdf_file
	else:
		print "need a production GIS file for analysis"
       		exit()

	if (options.output_file):
		gis_output = options.output_file 
	else:
		print "no GIS output file provided, so no solver statistics will be provided"

else:
        print "not performing GIS production analysis"

if (options.time_stamp):
	time_stamp = options.time_stamp 
else:
	print "no time given for website"
	time_stamp = " "

if (options.comment):
	comment = options.comment
else:
	print "no comments about test case given"
	comment = " "

if (options.username):

	print 'placing HTML files in the ' + options.username + ' subdirectory (check permissions)'
 	target_html = options.html_path

else:

	print 'no username specified, placing HTML files in the main html directory'
	target_html = options.html_path 

#remove html files previously used in specified subdirectory

try:
	os.remove(target_html + '/GIS-main-diag.html')
except OSError as o:
      	if o.errno == 2:
		print "recreating GIS-main-diag.html in " + options.username + " subdirectory"
	else:
		raise
try:
       	os.remove(target_html + '/test_suite.html')
except OSError as o:
	if o.errno == 2:
		print "recreating test suite in " + options.username + " subdirectory"
	else:
		raise
try:
       	os.remove(target_html + '/GIS-con-diag.html')
except OSError as o:
	if o.errno == 2:
		print "recreating GIS-con-diag.html in " + options.username + " subdirectory"
	else:
		raise
try:
       	os.remove(target_html + '/GIS-out-diag.html')
except OSError as o:
	if o.errno == 2:
		print "recreating GIS-out-diag.html in " + options.username + " subdirectory"
	else:
		raise
try:
       	os.remove(target_html + '/GIS-plot-diag.html')
except OSError as o:
	if o.errno == 2:
		print "recreating GIS-plot-diag.html in " + options.username + " subdirectory"
	else:
		raise
try:
        os.remove('plot_details.out')
except OSError as o:
        if o.errno == 2:
                print "clearing plot_details.out"
        else:
                raise

# create production plots for analysis
if options.gis_prod:

	ncl_script=options.ncl_path + "/tri_ncl_script.ncl"

	plot_gis_thk = "ncl 'VAR=addfile(\"" + variable_nc + "\", \"r\")'" + ' ' + \
		    "'STOCK=addfile(\"" + stock_nc + "\",\"r\")'" + ' ' + \
		    "'PNG=\"" + options.ncl_path + "/gis5km_thk\"'" + ' ' + \
                    ncl_script + ' ' + "1> /dev/null"

#print plot_gis_thk

	try:
		output = subprocess.call(plot_gis_thk, shell=True)
	except:
		print "error formatting thickness plot of production run"
		raise

#transferring thickness plot to www location

	if (options.ncl_path + '/gis5km_thk.png'):
        	thkpic = "mv -f " + options.ncl_path + "/gis5km_thk.png" + " " + target_html + "/"
        	try:
                	output = subprocess.call(thkpic, shell=True)
        	except:
                	print "error moving thk png file"
                	raise

#transferring cover picture to www file

if (options.ncl_path + '/alaska_pic.png'):
        alaskapic = "cp -f " + options.ncl_path + "/alaska_pic.png" + " " + target_html + "/"
        try:
                output = subprocess.call(alaskapic, shell=True)
        except:
                print "error moving cover picture"
                raise


#create all the test suite diagnostics pages
if options.test_suite:

        test_file = open(target_html + '/test_suite.html', 'w')
        descript_file = open(target_html + '/test_descript.html', 'w')
# diagnostic dome case
        dome30d_file = open(target_html + '/dome30d_details.html', 'w')
        dome30d_case = open(target_html + '/dome30d_case.html', 'w')
        dome30d_plot = open(target_html + '/dome30d_plot.html', 'w')
        dome30d_xml  = open(target_html + '/dome30d_xml.html', 'w')
# evolving dome case
        dome30e_file = open(target_html + '/dome30e_details.html', 'w')
        dome30e_case = open(target_html + '/dome30e_case.html', 'w')
        dome30e_plot = open(target_html + '/dome30e_plot.html', 'w')
        dome30e_xml  = open(target_html + '/dome30e_xml.html', 'w')
# circular shelf case
        circ_file = open(target_html + '/circ_details.html', 'w')
        circ_case = open(target_html + '/circ_case.html', 'w')
        circ_plot = open(target_html + '/circ_plot.html', 'w')
        circ_xml  = open(target_html + '/circ_xml.html', 'w')
# confined shelf case
        conf_file = open(target_html + '/conf_details.html', 'w')
        conf_case = open(target_html + '/conf_case.html', 'w')
        conf_plot = open(target_html + '/conf_plot.html', 'w')
        conf_xml  = open(target_html + '/conf_xml.html', 'w')
# ismip hom a 80km case
        ishoma80_file = open(target_html + '/ishoma80_details.html', 'w')
        ishoma80_case = open(target_html + '/ishoma80_case.html', 'w')
        ishoma80_plot = open(target_html + '/ishoma80_plot.html', 'w')
        ishoma80_xml  = open(target_html + '/ishoma80_xml.html', 'w')
# ismip hom a 20km case
        ishoma20_file = open(target_html + '/ishoma20_details.html', 'w')
        ishoma20_case = open(target_html + '/ishoma20_case.html', 'w')
        ishoma20_plot = open(target_html + '/ishoma20_plot.html', 'w')
        ishoma20_xml  = open(target_html + '/ishoma20_xml.html', 'w')
# ismip hom c 80km case
        ishomc80_file = open(target_html + '/ishomc80_details.html', 'w')
        ishomc80_case = open(target_html + '/ishomc80_case.html', 'w')
        ishomc80_plot = open(target_html + '/ishomc80_plot.html', 'w')
        ishomc80_xml  = open(target_html + '/ishomc80_xml.html', 'w')
# 10km GIS case
        gis10_file = open(target_html + '/gis10_details.html', 'w')
        gis10_case = open(target_html + '/gis10_case.html', 'w')
        gis10_plot = open(target_html + '/gis10_plot.html', 'w')
        gis10_xml  = open(target_html + '/gis10_xml.html', 'w')

# TODO create a list of the html files of the included cases, then pass through the testsuite.web call

#path to python code to create all the test suite pages and data
        reg_test = options.test_suite + "/reg_test"

        VV_testsuite.web(descript_file,test_file,dome30d_file,dome30d_case,dome30d_plot,dome30d_xml, \
                dome30e_file,dome30e_case,dome30e_plot,dome30e_xml, \
                circ_file,circ_case,circ_plot,circ_xml,conf_file,conf_case,conf_plot,conf_xml, \
                ishoma80_file,ishoma80_case,ishoma80_plot,ishoma80_xml,ishoma20_file,ishoma20_case,ishoma20_plot,ishoma20_xml, \
                ishomc80_file,ishomc80_case,ishomc80_plot,ishomc80_xml,\
                gis10_file,gis10_case,gis10_plot,gis10_xml, \
                reg_test,options.bench_data,options.ncl_path,options.data_path,target_html,options.script_path,\
                options.diagnostic_flag,options.evolving_flag,options.circular_flag,options.confined_flag,\
                options.ismip_hom_a80_flag,options.ismip_hom_a20_flag,options.ismip_hom_c_flag,options.gis_10km_flag)

dictionary = VV_testsuite.bit_list(reg_test,options.bench_data)

#writing the main HTML page

file = open(target_html + '/GIS-main-diag.html', 'w')

file.write('<HTML><HEAD>\n')
file.write('<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">')
file.write('<title>Land Ice Verification and Validation toolkit</title>')
file.write('<link href="style.css" rel="stylesheet" type="text/css">')
file.write('<BODY>\n')
file.write(' <div id="container"> <div id="content">')
#file.write('<BODY bgcolor="white">\n')
file.write('<P>\n')
file.write('<OBJECT data="alaska_pic.png" type="image/png" width="400" height="300" hspace=10 align=left alt="ice sheet pic">\n')
file.write('</OBJECT>\n')
file.write('<FONT color=blue><B>\n')
file.write('Land Ice Validation package  </B></FONT> <BR>\n')
file.write('Performed on ' + options.time_stamp + '<BR>\n')
file.write('Test case run by: ' + options.username + '<BR>\n')
file.write('Details: ' + options.comment + '<BR>\n')
file.write('</P>\n')
file.write('<BR clear=left>\n')
file.write('<BR>\n')
file.write('<HR noshade size=2 size="100%">\n')
file.write('<TH ALIGN=LEFT><A HREF="test_suite.html">Basic Test Suite Diagnostics</A>\n')

if 1 in dictionary.values():
        file.write('<font color="red"> All Cases NOT Bit-for-Bit</font><br>')
else:
        file.write(' All Cases Bit-for-Bit <br>')

file.write('<BR>\n')
file.write('<BR>\n')
if options.gis_prod:
        
        gis_con = open(target_html + '/GIS-con-diag.html', 'w')
        file.write('<TH ALIGN=LEFT><A HREF="GIS-con-diag.html">Production Configure Diagnostics</A>\n')
	configure_path = options.config_file
        VV_gisproduction.conf(gis_con,configure_path) 
        
        file.write('<BR>\n')
        file.write('<BR>\n')
	
        gis_out = open(target_html + '/GIS-out-diag.html', 'w')
	file.write('<TH ALIGN=LEFT><A HREF="GIS-out-diag.html">Production Output Diagnostics</A>\n')
	VV_gisproduction.outfile(gis_out,gis_output,'gis5km')

	file.write('<BR>\n')
	file.write('<BR>\n')
	
	if stock_nc:
		plot_file = open(target_html + '/GIS-plot-diag.html', 'w')
        file.write('<TH ALIGN=LEFT><A HREF="GIS-plot-diag.html">Ice Thickness</A>\n')
	file.write('<BR>\n <BR>\n <BR> \n')

file.write('<h4> For Additional Information: </h4> <p>')
file.write(' Kate Evans <br>')
file.write('Oak Ridge National Laboratory<br>')
file.write('1 Bethel Valley Road <br>')
file.write('Oak Ridge, Tennessee 37831-6015 <br>')
file.write('Email: 4ue@ornl.gov <br> </p>')

file.write('</BODY>\n')
file.write('</HTML>\n')
file.close()

print "LIVV Completed. Go to " + options.html_link + "/GIS-main-diag.html to view results"

# plot production run output for comparison to the benchmark

#		plot_file.write('<HTML>\n')
#      		plot_file.write('<TITLE>Thickness</TITLE>\n')
#                plot_file.write('<H2>Thickness Plot</H2>')
#		plot_file.write('<TABLE>\n')
#		plot_file.write('<TR>\n')
#		plot_file.write('<H4>a) Benchmark Ice Thickness</H4>\n')
#		plot_file.write('<H4>b) Simulation Ice Thickness</H4>\n')
#		plot_file.write('<H4>c) Difference from Benchmark </H4>\n')
#		plot_file.write('<OBJECT data="gis5km_thk.png" type="image/png" width="1300" height="800" hspace=10 align=left alt="Thickness Plots">\n')
#		plot_file.write('</OBJECT>\n')
#		plot_file.write('<TR>\n')
#		plot_file.write('<BR>\n')
#		plot_file.write('</TABLE>\n')
#		plot_file.write('</HTML>\n')
#		plot_file.close()



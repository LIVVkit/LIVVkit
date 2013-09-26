
import sys
import os
import re
from optparse import OptionParser
import subprocess
import collections
import VV_outprocess
import VV_testsuite
import VV_largesuite

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
parser.add_option('-d', '--data', action='store', type='string', dest='data_dir', \
                  metavar='PATH', help='defining which data directory to use for both bench and current run')
parser.add_option('-t', '--test', action='store', type='string', dest='test_suite', \
                  metavar='TEST', help='path to location of test suite')
parser.add_option('-i', '--timestamp', action='store', type='string', dest='time_stamp', \
                  metavar='FILE', help='the current time to record in the web output')
parser.add_option('-m', '--comment', action='store', type='string', dest='comment', \
                  metavar='FILE', help='information about the test case for user reference')
parser.add_option('-u', '--username', action='store', type='string', dest='username', \
                  metavar='FILE', help='username used to create subdirectory of web pages of output')
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
parser.add_option('-F', '--dome500', action='store', type='int', dest='dome500_flag', \
                  metavar='FLAG', help='flag to run dome500 test')
parser.add_option('-H', '--gis5km', action='store', type='int', dest='gis_5km_flag', \
                  metavar='FLAG', help='flag to run gis5km test')
#parser.add_option('-a', '--ant_prod', action='store_true', dest='ant_prod', \
#                  help='include flag to run the ANT production analysis')

#parse the command line options and arguments and store in lists
(options, args) = parser.parse_args()

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

if os.path.isdir(options.html_path) == True:
    
        target_html = options.html_path
else:
        mkdir = ['mkdir ', options.html_path]
        try:
                subprocess.check_call(mkdir)
        except subprocess.CalledProcessError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.returncode)
        except OSError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.errno)
        chmod = ['chmod 755 ', options.html_path]
        try:
                subprocess.check_call(chmod)
        except subprocess.CalledProcessError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.returncode)
        except OSError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.errno)
        
        target_html = options.html_path

if (options.username):

	print 'placing HTML files in the ' + options.username + ' subdirectory (check permissions)'
else:
	print 'no username specified, placing HTML files in the main html directory'

#remove html files previously used in specified subdirectory

try:
	os.remove(target_html + '/livv_kit_main.html')
except OSError as o:
      	if o.errno == 2:
		print "recreating livv_kit_main.html in " + options.username + " subdirectory"
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
       	os.remove(target_html + '/large_test_suite.html')
except OSError as o:
	if o.errno == 2:
		print "recreating large test suite in " + options.username + " subdirectory"
	else:
		raise
try:
        os.remove('plot_details.out')
except OSError as o:
        if o.errno == 2:
                print "clearing plot_details.out"
        else:
                raise

#transferring cover picture to www file

if (options.ncl_path + '/alaska_pic.png'):
        alaskapic = ["cp", "-f", options.ncl_path+ "/alaska_pic.png", target_html+ "/"]
        try:
                subprocess.check_call(alaskapic)
        except subprocess.CalledProcessError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.returncode)
        except OSError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.errno)

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
#circular shelf case
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
                reg_test,options.data_dir,options.ncl_path,target_html,options.script_path,\
                options.diagnostic_flag,options.evolving_flag,options.circular_flag,options.confined_flag,\
                options.ismip_hom_a80_flag,options.ismip_hom_a20_flag,options.ismip_hom_c_flag,options.gis_10km_flag)

        dictionary = VV_testsuite.bit_list(reg_test,options.data_dir,options.diagnostic_flag,options.evolving_flag,options.circular_flag,\
                                options.confined_flag,options.ismip_hom_a80_flag,options.ismip_hom_a20_flag,options.ismip_hom_c_flag,options.gis_10km_flag)

#create all the large test suite diagnostics pages
if options.dome500_flag==1 or options.gis_5km_flag==1:

        large_test_file = open(target_html + '/large_test_suite.html', 'w')
        descript_file = open(target_html + '/large_test_descript.html', 'w')
# dome500 case
        dome500_file = open(target_html + '/dome500_details.html', 'w')
        dome500_case = open(target_html + '/dome500_case.html', 'w')
        dome500_plot = open(target_html + '/dome500_plot.html', 'w')
        dome500_xml  = open(target_html + '/dome500_xml.html', 'w')
# gis 5km case
        gis5km_file = open(target_html + '/gis5km_details.html', 'w')
        gis5km_case = open(target_html + '/gis5km_case.html', 'w')
        gis5km_plot = open(target_html + '/gis5km_plot.html', 'w')
        gis5km_xml  = open(target_html + '/gis5km_xml.html', 'w')

#path to python code to create all the large test suite pages and data
        perf_test = options.test_suite + "/perf_test"

        VV_largesuite.large_tests(descript_file,large_test_file,dome500_file,dome500_case,dome500_plot,dome500_xml, \
                gis5km_file,gis5km_case,gis5km_plot,gis5km_xml, \
                perf_test,options.ncl_path,target_html,options.script_path, \
                options.dome500_flag,options.gis_5km_flag,options.data_dir)

        dictionary_large = VV_largesuite.bit_list(perf_test,options.data_dir)
        
#writing the main HTML page

file = open(target_html + '/livv_kit_main.html', 'w')

file.write('<HTML><HEAD>\n')
file.write('<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">')
file.write('<title>Land Ice Verification and Validation toolkit</title>')
file.write('<link href="style.css" rel="stylesheet" type="text/css">')
file.write('<BODY>\n')
file.write(' <div id="container"> <div id="content">')
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
        file.write('<font color="green"> All Cases Bit-for-Bit</font><br>')

file.write('<BR>\n')
file.write('<BR>\n')
if options.dome500_flag==1 or options.gis_5km_flag==1:

        file.write('<TH ALIGN=LEFT><A HREF="large_test_suite.html">Performance and Analysis Test Suite</A>\n')
        
        if 1 in dictionary_large.values():
                file.write('<font color="red"> All Cases NOT Bit-for-Bit</font><br>')
        else:
                file.write('<font color="green"> All Cases Bit-for-Bit</font><br>')

file.write('<h4> For Additional Information: </h4> <p>')
file.write(' Kate Evans <br>')
file.write('Oak Ridge National Laboratory<br>')
file.write('1 Bethel Valley Road <br>')
file.write('Oak Ridge, Tennessee 37831-6015 <br>')
file.write('Email: 4ue@ornl.gov <br> </p>')

file.write('</BODY>\n')
file.write('</HTML>\n')
file.close()

print "LIVV Completed. Go to " + options.html_link + "/livv_kit_main.html to view results"


#!/usr/bin/env

import sys
import os
from optparse import OptionParser
import subprocess
import collections
import VV_checks
import time
import VV_utilities
import VV_gis5details
#import VV_dome500details

#bit-for-bit check for each test case
def bit_list(perf_test,bench_data):
    dictionary = {}
#dome500 case
    data_file_path = perf_test + '/dome500/data'
    bench_file_path = perf_test + '/bench/dome500/' + bench_data
    flag = VV_checks.bit4bit(data_file_path,bench_file_path)
    dictionary['dome500'] = flag
#gis 5km case
    data_file_path = perf_test + '/gis_5km/data'
    bench_file_path = perf_test + '/bench/gis_5km/' + bench_data
    flag = VV_checks.bit4bit(data_file_path,bench_file_path)
    dictionary['gis5km'] = flag

    return dictionary


def large_tests(descript_file,large_test_file,dome500_file,dome500_case,dome500_plot,dome500_xml, \
            gis5km_file,gis5km_case,gis5km_plot,gis5km_xml, \
            perf_test,ncl_path,html_path,script_path, \
            dome500_flag,gis_5km_flag,bench_data):

# using data, fill the web page with info about the cases
	large_test_file.write('<HTML>\n')
	large_test_file.write('<TITLE>Performance and Analysis Test Suite</TITLE>\n')
	large_test_file.write('<H1>Performance and Analysis Test Suite</H1>')

# link to descript_file about the test cases
	large_test_file.write('<TH ALIGN=LEFT><A HREF="largetest_descript.html">Test Suite Descriptions</A>\n')
	large_test_file.write('<BR>\n')

        dictionary = bit_list(perf_test,bench_data)


#apply flag to turn off running test
        if dome500_flag == 1:

# Dome 500 stats
            if dictionary['dome500'] == 0:
                large_test_file.write('<H2>Diagnostic Dome 500 Test: <font color="green">Bit-for-Bit</font></H2>')
            else:
                large_test_file.write('<H2>Diagnostic Dome 500 Test: <font color="red">NOT Bit-for-Bit</font></H2>')
	
#put something here to flag BFB results and no need to do any more calculations
	    flag_to_plot_dome500 = 1
	    if flag_to_plot_dome500:

# link to dome500_file with descriptions about the test cases
		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome500_details.html">Diagnostic Dome 500 Velocity Solver Details</A>\n')
		    large_test_file.write('<BR>\n')
                    failedt = VV_largetestdetails.d500details(dome500_file,perf_test,bench_data)

		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome500_xml.html">Solver Parameter Settings: Diagnostic Dome 500 XML Details</A>\n')
		    large_test_file.write('<BR>\n')
		    xml_path = perf_test + '/dome500/diagnostic/trilinosOptions.xml'
		    bench_xml_path = perf_test + '/bench/dome500/diagnostic/trilinosOptions.xml'
                    VV_utilities.xml(dome500_xml,xml_path,bench_xml_path)

		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome500_case.html">Diagnostic Dome 500 Case Details</A>\n')
		    large_test_file.write('<BR>\n')
                    configure_path = perf_test + '/dome500/diagnostic/dome.30.JFNK.trilinos.config.1'
                    bench_configure_path = perf_test + '/bench/dome500/diagnostic/dome.30.JFNK.trilinos.config.1'
        	    VV_utilities.conf(dome500_case,configure_path,bench_configure_path)

		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome500d_plot.html">Diagnostic Dome 500 Plots</A>\n')
		    large_test_file.write('<BR>\n')
                    if failedt != 0:
                        dome500d_plot.write("<H2>Diagnostic Dome 500 Test failed, plots may not be generated</H2><br>")
                    checkpath = perf_test + '/dome500/diagnostic/data/dome.1.nc'
                    checkpath2 = perf_test + '/dome500/diagnostic/data/dome.4.nc'
                    noplot = VV_checks.emptycheck(checkpath)
                    noplot1 = noplot
                    noplot = VV_checks.emptycheck(checkpath2)
                    if noplot1 != 1 and noplot != 1:
                        VV_dome500details.dplot(dome500_plot,perf_test,ncl_path,html_path,script_path,bench_data)

# Time stamping
	    strrand = ''
	    mode = os.stat(perf_test + '/dome500/diagnostic').st_mtime
	    mode = mode - 14400
	    mode = time.gmtime(mode)
	    ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
	    strrand = '<b>Time of last access: ' + str(ctime) + '</b>'
	    large_test_file.write(strrand)

        else:
            print "NOT RUNNING DIAGNOSTIC DOME500 TESTCASE"


#apply flag to turn off running test
        if gis_5km_flag == 1:

# GIS 5km stats
            if dictionary['gis5km'] == 0:
                large_test_file.write('<H2>GIS 5KM Test: <font color="green">Bit-for-Bit</font></H2>')
            else:
                large_test_file.write('<H2>GIS 5KM Test: <font color="red">NOT Bit-for-Bit</font></H2>')

# put something here to flag BFB results between data and bench and pgi and gnu etc.
	    flag_to_plot_gis5km = 1
	    if flag_to_plot_gis5km:

		    large_test_file.write('<TH ALIGN=LEFT><A HREF="gis5km_details.html">GIS 5km Velocity Solver Details</A>\n')
		    large_test_file.write('<BR>\n')
        	    failedt = VV_gis5details.details(gis5km_file,perf_test,bench_data)

		    large_test_file.write('<TH ALIGN=LEFT><A HREF="gis5km_xml.html">Solver Parameter Settings: GIS 5km XML Details</A>\n')
                    large_test_file.write('<BR>\n')
                    xml_path = perf_test + '/gis_5km/trilinosOptions.xml'
                    bench_xml_path = perf_test + '/bench/gis_5km/trilinosOptions.xml'
                    VV_utilities.xml(gis5km_xml,xml_path,bench_xml_path)
                
                    large_test_file.write('<TH ALIGN=LEFT><A HREF="gis5km_case.html">GIS 5km Case Details</A>\n')
		    large_test_file.write('<BR>\n')
                    configure_path = perf_test + '/gis_5km/gis_5km.config'
                    bench_configure_path = perf_test + '/bench/gis_5km/gis_5km.config'
        	    VV_utilities.conf(gis5km_case,configure_path,bench_configure_path)

		    large_test_file.write('<TH ALIGN=LEFT><A HREF="gis5km_plot.html">GIS 5km Plots</A>\n')
		    large_test_file.write('<BR>\n')
                    if failedt != 0:
                        gis5_plot.write("<H2>GIS 5km Test failed, plots may not be generated</H2><br>")
                    checkpath = perf_test + '/gis_5km/data/gis_5km.ice2sea.init.nc'
                    noplot = VV_checks.emptycheck(checkpath)
                    if noplot != 1:
                        VV_gis5details.gis5_plot(gis5km_plot,perf_test,ncl_path,html_path,script_path,bench_data)

# Time stamping
	    mode = os.stat(perf_test + '/gis_5km').st_mtime
	    mode = mode - 14400
	    mode = time.gmtime(mode)
	    ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
	    strrand = '<b>Time of last access: ' + ctime + '</b>\n'
	    large_test_file.write(strrand)

        else:
            print "NOT RUNNING GIS 5KM TESTCASE"


        large_test_file.write('<BR>\n')
        large_test_file.write('<BR>\n')
        large_test_file.write('<TH ALIGN=LEFT><A HREF="livv_kit_main.html">Home</A>\n')
	large_test_file.write('</HTML>\n')
	large_test_file.close()

	descript_file.write('<HTML>\n')
	descript_file.write('<TITLE>Descriptions about the Test Suite</TITLE>\n')
	descript_file.write('<H2>Test Suite Details</H2>')
	descript_file.write('<BR>\n')
	descript_file.write('The Diagnostic Dome 500 test case \n')
	descript_file.write('<BR>\n')
        descript_file.write('  Attributes: 3-D paraboloid dome of ice with a circular, 60 km diameter base sitting on a flat bed. The horizontal spatial resolution studies are 2 km, 1 km, 0.5 km and 0.25 km, and there are 10 vertical levels. For this set of experiments a quasi no-slip basal condition in imposed by setting. A zero-flux boundary condition is applied to the dome margins. \n')
	descript_file.write('<BR>\n')
	descript_file.write('  What does it test? \n')
	descript_file.write('<BR><BR>\n')
	descript_file.write('<BR>\n')
	descript_file.write('GIS 5KM Test Case \n')
	descript_file.write('<BR>\n')
        descript_file.write('  Attributes: 3-D paraboloid dome of ice with a circular, 60 km diameter base sitting on a flat bed. The horizontal spatial resolution studies are 2 km, 1 km, 0.5 km and 0.25 km, and there are 10 vertical levels. For this set of experiments a quasi no-slip basal condition in imposed by setting. A zero-flux boundary condition is applied to the dome margins. \n')
	descript_file.write('<BR>\n')
	descript_file.write('  What does it test? \n')
	descript_file.write('<BR><BR>\n')
	descript_file.write('</HTML>\n')
	descript_file.close()


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
import VV_largetestdetails

#bit-for-bit check for each test case
def bit_list(perf_test,data_dir,dome60_flag,dome120_flag,dome240_flag, \
        dome500_flag,dome1000_flag,gis_5km_flag):
    dictionary_large = {}
#dome60 case
    #apply flag to turn off running test
    if dome60_flag == 1:
        data_file_path = perf_test + '/dome60/' + data_dir
        bench_file_path = perf_test + '/bench/dome60/' + data_dir
        flag = VV_checks.bit4bit(data_file_path,bench_file_path)
        dictionary_large['dome60'] = flag
    else:
        dictionary_large['dome60'] = 0
#dome120 case
    #apply flag to turn off running test
    if dome120_flag == 1:
        data_file_path = perf_test + '/dome120/' + data_dir
        bench_file_path = perf_test + '/bench/dome120/' + data_dir
        flag = VV_checks.bit4bit(data_file_path,bench_file_path)
        dictionary_large['dome120'] = flag
    else:
        dictionary_large['dome120'] = 0
#dome240 case
    #apply flag to turn off running test
    if dome240_flag == 1:
        data_file_path = perf_test + '/dome240/' + data_dir
        bench_file_path = perf_test + '/bench/dome240/' + data_dir
        flag = VV_checks.bit4bit(data_file_path,bench_file_path)
        dictionary_large['dome240'] = flag
    else:
        dictionary_large['dome240'] = 0
#dome500 case
    #apply flag to turn off running test
    if dome500_flag == 1:
        data_file_path = perf_test + '/dome500/' + data_dir
        bench_file_path = perf_test + '/bench/dome500/' + data_dir
        flag = VV_checks.bit4bit(data_file_path,bench_file_path)
        dictionary_large['dome500'] = flag
    else:
        dictionary_large['dome500'] = 0
#dome1000 case
    #apply flag to turn off running test
    if dome1000_flag == 1:
        data_file_path = perf_test + '/dome1000/' + data_dir
        bench_file_path = perf_test + '/bench/dome1000/' + data_dir
        flag = VV_checks.bit4bit(data_file_path,bench_file_path)
        dictionary_large['dome1000'] = flag
    else:
        dictionary_large['dome1000'] = 0
#gis 5km case
    #apply flag to turn off running test
    if gis_5km_flag == 1:
        data_file_path = perf_test + '/gis_5km/' + data_dir
        bench_file_path = perf_test + '/bench/gis_5km/' + data_dir
        flag = VV_checks.bit4bit(data_file_path,bench_file_path)
        dictionary_large['gis5km'] = flag
    else:
        dictionary_large['gis5km'] = 0

    return dictionary_large


def large_tests(descript_file,large_test_file,dome60_file,dome60_case,dome60_plot,dome60_xml, \
            dome120_file,dome120_case,dome120_plot,dome120_xml,dome240_file,dome240_case,dome240_plot,dome240_xml, \
            dome500_file,dome500_case,dome500_plot,dome500_xml,dome1000_file,dome1000_case,dome1000_plot,dome1000_xml, \
            gis5km_file,gis5km_case,gis5km_plot,gis5km_xml, \
            perf_test,ncl_path,html_path,script_path, \
            dome60_flag,dome120_flag,dome240_flag, \
            dome500_flag,dome1000_flag,gis_5km_flag,data_dir):

# using data, fill the web page with info about the cases
	large_test_file.write('<HTML>\n')
	large_test_file.write('<TITLE>Performance and Analysis Test Suite</TITLE>\n')
	large_test_file.write('<H1>Performance and Analysis Test Suite</H1>')

# link to descript_file about the test cases
	large_test_file.write('<TH ALIGN=LEFT><A HREF="largetest_descript.html">Test Suite Descriptions</A>\n')
	large_test_file.write('<BR>\n')

        dictionary = bit_list(perf_test,data_dir,dome60_flag,dome120_flag,dome240_flag, \
               dome500_flag,dome1000_flag,gis_5km_flag)


#apply flag to turn off running test
        if dome60_flag == 1:

# Dome 60 stats
            print "running dome60 testcase"
            if dictionary['dome60'] == 0:
                large_test_file.write('<H2>Diagnostic Dome 60 Test: <font color="green">Bit-for-Bit</font></H2>')
            else:
                large_test_file.write('<H2>Diagnostic Dome 60 Test: <font color="red">NOT Bit-for-Bit</font></H2>')
	
#put something here to flag BFB results and no need to do any more calculations
	    flag_to_plot_dome60 = 1
	    if flag_to_plot_dome60:

# link to dome60_file with descriptions about the test cases
		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome60_details.html">Diagnostic Dome 60 Velocity Solver Details</A>\n')
		    large_test_file.write('<BR>\n')
                    failedt = VV_largetestdetails.details60(dome60_file,perf_test,data_dir)

		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome60_xml.html">Solver Parameter Settings: Diagnostic Dome 60 XML Details</A>\n')
		    large_test_file.write('<BR>\n')
		    xml_path = perf_test + '/dome60/trilinosOptions.xml'
		    bench_xml_path = perf_test + '/bench/dome60/trilinosOptions.xml'
                    VV_utilities.xml(dome60_xml,xml_path,bench_xml_path)

		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome60_case.html">Diagnostic Dome 60 Case Details</A>\n')
		    large_test_file.write('<BR>\n')
                    configure_path = perf_test + '/dome60/dome.60.JFNK.trilinos.config'
                    bench_configure_path = perf_test + '/bench/dome60/dome.60.JFNK.trilinos.config'
        	    VV_utilities.conf(dome60_case,configure_path,bench_configure_path)

#		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome60_plot.html">Diagnostic Dome 60 Plots</A>\n')
#		    large_test_file.write('<BR>\n')
#                    if failedt != 0:
#                        dome60_plot.write("<H2>Diagnostic Dome 60 Test failed, plots may not be generated</H2><br>")
#                    checkpath = perf_test + '/dome60/data/dome.1.nc'
#                    checkpath2 = perf_test + '/dome60/data/dome.4.nc'
#                    noplot = VV_checks.emptycheck(checkpath)
#                    noplot1 = noplot
#                    noplot = VV_checks.emptycheck(checkpath2)
#                    if noplot1 != 1 and noplot != 1:
#                        VV_dome60details.plot(dome60_plot,perf_test,ncl_path,html_path,script_path,data_dir)
# Time stamping
	    strrand = ''
	    mode = os.stat(perf_test + '/dome60/').st_mtime
	    mode = mode - 14400
	    mode = time.gmtime(mode)
	    ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
	    strrand = '<b>Time of Last Simulation: ' + str(ctime) + '</b>'
	    large_test_file.write(strrand)

        else:
            print "NOT RUNNING DOME60 TESTCASE"


#apply flag to turn off running test
        if dome120_flag == 1:

# Dome 120 stats
            print "running dome120 testcase"
            if dictionary['dome120'] == 0:
                large_test_file.write('<H2>Diagnostic Dome 120 Test: <font color="green">Bit-for-Bit</font></H2>')
            else:
                large_test_file.write('<H2>Diagnostic Dome 120 Test: <font color="red">NOT Bit-for-Bit</font></H2>')
	
#put something here to flag BFB results and no need to do any more calculations
	    flag_to_plot_dome120 = 1
	    if flag_to_plot_dome120:

# link to dome120_file with descriptions about the test cases
		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome120_details.html">Diagnostic Dome 120 Velocity Solver Details</A>\n')
		    large_test_file.write('<BR>\n')
                    failedt = VV_largetestdetails.details120(dome120_file,perf_test,data_dir)

		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome120_xml.html">Solver Parameter Settings: Diagnostic Dome 120 XML Details</A>\n')
		    large_test_file.write('<BR>\n')
		    xml_path = perf_test + '/dome120/trilinosOptions.xml'
		    bench_xml_path = perf_test + '/bench/dome120/trilinosOptions.xml'
                    VV_utilities.xml(dome120_xml,xml_path,bench_xml_path)

		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome120_case.html">Diagnostic Dome 120 Case Details</A>\n')
		    large_test_file.write('<BR>\n')
                    configure_path = perf_test + '/dome120/dome.120.JFNK.trilinos.config'
                    bench_configure_path = perf_test + '/bench/dome120/dome.120.JFNK.trilinos.config'
        	    VV_utilities.conf(dome120_case,configure_path,bench_configure_path)

#		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome120_plot.html">Diagnostic Dome 120 Plots</A>\n')
#		    large_test_file.write('<BR>\n')
#                    if failedt != 0:
#                        dome120_plot.write("<H2>Diagnostic Dome 120 Test failed, plots may not be generated</H2><br>")
#                    checkpath = perf_test + '/dome120/data/dome.1.nc'
#                    checkpath2 = perf_test + '/dome120/data/dome.4.nc'
#                    noplot = VV_checks.emptycheck(checkpath)
#                    noplot1 = noplot
#                    noplot = VV_checks.emptycheck(checkpath2)
#                    if noplot1 != 1 and noplot != 1:
#                        VV_dome120details.plot(dome120_plot,perf_test,ncl_path,html_path,script_path,data_dir)
# Time stamping
	    strrand = ''
	    mode = os.stat(perf_test + '/dome120/').st_mtime
	    mode = mode - 14400
	    mode = time.gmtime(mode)
	    ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
	    strrand = '<b>Time of Last Simulation: ' + str(ctime) + '</b>'
	    large_test_file.write(strrand)

        else:
            print "NOT RUNNING DOME120 TESTCASE"


#apply flag to turn off running test
        if dome240_flag == 1:

# Dome 240 stats
            print "running dome240 testcase"
            if dictionary['dome240'] == 0:
                large_test_file.write('<H2>Diagnostic Dome 240 Test: <font color="green">Bit-for-Bit</font></H2>')
            else:
                large_test_file.write('<H2>Diagnostic Dome 240 Test: <font color="red">NOT Bit-for-Bit</font></H2>')
	
#put something here to flag BFB results and no need to do any more calculations
	    flag_to_plot_dome240 = 1
	    if flag_to_plot_dome240:

# link to dome240_file with descriptions about the test cases
		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome240_details.html">Diagnostic Dome 240 Velocity Solver Details</A>\n')
		    large_test_file.write('<BR>\n')
                    failedt = VV_largetestdetails.details240(dome240_file,perf_test,data_dir)

		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome240_xml.html">Solver Parameter Settings: Diagnostic Dome 240 XML Details</A>\n')
		    large_test_file.write('<BR>\n')
		    xml_path = perf_test + '/dome240/trilinosOptions.xml'
		    bench_xml_path = perf_test + '/bench/dome240/trilinosOptions.xml'
                    VV_utilities.xml(dome240_xml,xml_path,bench_xml_path)

		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome240_case.html">Diagnostic Dome 240 Case Details</A>\n')
		    large_test_file.write('<BR>\n')
                    configure_path = perf_test + '/dome240/dome.240.JFNK.trilinos.config'
                    bench_configure_path = perf_test + '/bench/dome240/dome.240.JFNK.trilinos.config'
        	    VV_utilities.conf(dome240_case,configure_path,bench_configure_path)

#		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome240_plot.html">Diagnostic Dome 240 Plots</A>\n')
#		    large_test_file.write('<BR>\n')
#                    if failedt != 0:
#                        dome240_plot.write("<H2>Diagnostic Dome 240 Test failed, plots may not be generated</H2><br>")
#                    checkpath = perf_test + '/dome240/data/dome.1.nc'
#                    checkpath2 = perf_test + '/dome240/data/dome.4.nc'
#                    noplot = VV_checks.emptycheck(checkpath)
#                    noplot1 = noplot
#                    noplot = VV_checks.emptycheck(checkpath2)
#                    if noplot1 != 1 and noplot != 1:
#                        VV_dome240details.plot(dome240_plot,perf_test,ncl_path,html_path,script_path,data_dir)
# Time stamping
	    strrand = ''
	    mode = os.stat(perf_test + '/dome240/').st_mtime
	    mode = mode - 14400
	    mode = time.gmtime(mode)
	    ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
	    strrand = '<b>Time of Last Simulation: ' + str(ctime) + '</b>'
	    large_test_file.write(strrand)

        else:
            print "NOT RUNNING DOME240 TESTCASE"


#apply flag to turn off running test
        if dome500_flag == 1:

# Dome 500 stats
            print "running dome500 testcase"
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
                    failedt = VV_largetestdetails.details500(dome500_file,perf_test,data_dir)

		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome500_xml.html">Solver Parameter Settings: Diagnostic Dome 500 XML Details</A>\n')
		    large_test_file.write('<BR>\n')
		    xml_path = perf_test + '/dome500/trilinosOptions.xml'
		    bench_xml_path = perf_test + '/bench/dome500/trilinosOptions.xml'
                    VV_utilities.xml(dome500_xml,xml_path,bench_xml_path)

		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome500_case.html">Diagnostic Dome 500 Case Details</A>\n')
		    large_test_file.write('<BR>\n')
                    configure_path = perf_test + '/dome500/dome.500.JFNK.trilinos.config'
                    bench_configure_path = perf_test + '/bench/dome500/dome.500.JFNK.trilinos.config'
        	    VV_utilities.conf(dome500_case,configure_path,bench_configure_path)

#		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome500_plot.html">Diagnostic Dome 500 Plots</A>\n')
#		    large_test_file.write('<BR>\n')
#                    if failedt != 0:
#                        dome500_plot.write("<H2>Diagnostic Dome 500 Test failed, plots may not be generated</H2><br>")
#                    checkpath = perf_test + '/dome500/data/dome.1.nc'
#                    checkpath2 = perf_test + '/dome500/data/dome.4.nc'
#                    noplot = VV_checks.emptycheck(checkpath)
#                    noplot1 = noplot
#                    noplot = VV_checks.emptycheck(checkpath2)
#                    if noplot1 != 1 and noplot != 1:
#                        VV_dome500details.plot(dome500_plot,perf_test,ncl_path,html_path,script_path,data_dir)
# Time stamping
	    strrand = ''
	    mode = os.stat(perf_test + '/dome500/').st_mtime
	    mode = mode - 14400
	    mode = time.gmtime(mode)
	    ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
	    strrand = '<b>Time of Last Simulation: ' + str(ctime) + '</b>'
	    large_test_file.write(strrand)

        else:
            print "NOT RUNNING DOME500 TESTCASE"


#apply flag to turn off running test
        if dome1000_flag == 1:

# Dome 1000 stats
            print "running dome1000 testcase"
            if dictionary['dome1000'] == 0:
                large_test_file.write('<H2>Diagnostic Dome 1000 Test: <font color="green">Bit-for-Bit</font></H2>')
            else:
                large_test_file.write('<H2>Diagnostic Dome 1000 Test: <font color="red">NOT Bit-for-Bit</font></H2>')
	
#put something here to flag BFB results and no need to do any more calculations
	    flag_to_plot_dome1000 = 1
	    if flag_to_plot_dome1000:

# link to dome1000_file with descriptions about the test cases
		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome500_details.html">Diagnostic Dome 1000 Velocity Solver Details</A>\n')
		    large_test_file.write('<BR>\n')
                    failedt = VV_largetestdetails.details1000(dome1000_file,perf_test,data_dir)

		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome1000_xml.html">Solver Parameter Settings: Diagnostic Dome 1000 XML Details</A>\n')
		    large_test_file.write('<BR>\n')
		    xml_path = perf_test + '/dome1000/trilinosOptions.xml'
		    bench_xml_path = perf_test + '/bench/dome1000/trilinosOptions.xml'
                    VV_utilities.xml(dome1000_xml,xml_path,bench_xml_path)

		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome1000_case.html">Diagnostic Dome 1000 Case Details</A>\n')
		    large_test_file.write('<BR>\n')
                    configure_path = perf_test + '/dome1000/dome.1000.JFNK.trilinos.config'
                    bench_configure_path = perf_test + '/bench/dome1000/dome.1000.JFNK.trilinos.config'
        	    VV_utilities.conf(dome1000_case,configure_path,bench_configure_path)

#		    large_test_file.write('<TH ALIGN=LEFT><A HREF="dome1000_plot.html">Diagnostic Dome 1000 Plots</A>\n')
#		    large_test_file.write('<BR>\n')
#                    if failedt != 0:
#                        dome1000_plot.write("<H2>Diagnostic Dome 1000 Test failed, plots may not be generated</H2><br>")
#                    checkpath = perf_test + '/dome1000/data/dome.1.nc'
#                    checkpath2 = perf_test + '/dome1000/data/dome.4.nc'
#                    noplot = VV_checks.emptycheck(checkpath)
#                    noplot1 = noplot
#                    noplot = VV_checks.emptycheck(checkpath2)
#                    if noplot1 != 1 and noplot != 1:
#                        VV_dome1000details.plot(dome1000_plot,perf_test,ncl_path,html_path,script_path,data_dir)
# Time stamping
	    strrand = ''
	    mode = os.stat(perf_test + '/dome1000/').st_mtime
	    mode = mode - 14400
	    mode = time.gmtime(mode)
	    ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
	    strrand = '<b>Time of Last Simulation: ' + str(ctime) + '</b>'
	    large_test_file.write(strrand)

        else:
            print "NOT RUNNING DOME1000 TESTCASE"


#apply flag to turn off running test
        if gis_5km_flag == 1:

# GIS 5km stats
            print "running gis5km testcase"
            if dictionary['gis5km'] == 0:
                large_test_file.write('<H2>GIS 5KM Test: <font color="green">Bit-for-Bit</font></H2>')
            else:
                large_test_file.write('<H2>GIS 5KM Test: <font color="red">NOT Bit-for-Bit</font></H2>')

# put something here to flag BFB results between data and bench and pgi and gnu etc.
	    flag_to_plot_gis5km = 1
	    if flag_to_plot_gis5km:

		    large_test_file.write('<TH ALIGN=LEFT><A HREF="gis5km_details.html">GIS 5km Velocity Solver Details</A>\n')
		    large_test_file.write('<BR>\n')
        	    failedt = VV_gis5details.details(gis5km_file,perf_test,data_dir)

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
                        VV_gis5details.gis5_plot(gis5km_plot,perf_test,ncl_path,html_path,script_path,data_dir)

# Time stamping
	    mode = os.stat(perf_test + '/gis_5km').st_mtime
	    mode = mode - 14400
	    mode = time.gmtime(mode)
	    ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
	    strrand = '<b>Time of Last Simulation: ' + ctime + '</b>\n'
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


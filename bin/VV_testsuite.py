#!/usr/bin/env

import sys
import os
from optparse import OptionParser
import subprocess
import collections
import VV_outprocess
import VV_utilities
import VV_dome30details
import VV_shelfdetails
import VV_ismip
import VV_gis10details
import VV_checks
from stat import *
import time

#bit-for-bit check for each test case
def bit_list(reg_test,bench_data):
    dictionary = {}
#diagnostic dome30 case
    data_file_path = reg_test + '/dome30/diagnostic/data'
    bench_file_path = reg_test + '/bench/dome30/diagnostic/' + bench_data
    flag = VV_checks.bit4bit(data_file_path,bench_file_path)
    dictionary['diagnostic'] = flag
#evolving dome30 case
    data_file_path = reg_test + '/dome30/evolving/data'
    bench_file_path = reg_test + '/bench/dome30/evolving/' + bench_data
    flag = VV_checks.bit4bit(data_file_path,bench_file_path)
    dictionary['evolving'] = flag
#circular shelf case
    data_file_path = reg_test + '/circular-shelf/data'
    bench_file_path = reg_test + '/bench/circular-shelf/' + bench_data
    flag = VV_checks.bit4bit(data_file_path,bench_file_path)
    dictionary['circular'] = flag
#confined shelf case
    data_file_path = reg_test + '/confined-shelf/data'
    bench_file_path = reg_test + '/bench/confined-shelf/' + bench_data
    flag = VV_checks.bit4bit(data_file_path,bench_file_path)
    dictionary['confined'] = flag
#ismip hom a 80 case
    data_file_path = reg_test + '/ismip-hom-a/80km/data'
    bench_file_path = reg_test + '/bench/ismip-hom-a/80km/' + bench_data
    flag = VV_checks.bit4bit(data_file_path,bench_file_path)
    dictionary['ismip-hom-a80'] = flag
#ismip hom a 20 case
    data_file_path = reg_test + '/ismip-hom-a/20km/data'
    bench_file_path = reg_test + '/bench/ismip-hom-a/20km/' + bench_data
    flag = VV_checks.bit4bit(data_file_path,bench_file_path)
    dictionary['ismip-hom-a20'] = flag
#ismip hom c case
    data_file_path = reg_test + '/ismip-hom-c/80km/data'
    bench_file_path = reg_test + '/bench/ismip-hom-c/80km/' + bench_data
    flag = VV_checks.bit4bit(data_file_path,bench_file_path)
    dictionary['ismip-hom-c'] = flag
#gis10km case
    data_file_path = reg_test + '/gis_10km/data'
    bench_file_path = reg_test + '/bench/gis_10km/' + bench_data
    flag = VV_checks.bit4bit(data_file_path,bench_file_path)
    dictionary['gis_10km'] = flag

    return dictionary

def web(descript_file,test_file, \
	dome30d_file,dome30d_case,dome30d_plot,dome30d_xml,dome30e_file,dome30e_case,dome30e_plot,dome30e_xml, \
	circ_file,circ_case,circ_plot,circ_xml,conf_file,conf_case,conf_plot,conf_xml, \
	ishoma80_file,ishoma80_case,ishoma80_plot,ishoma80_xml,ishoma20_file,ishoma20_case,ishoma20_plot,ishoma20_xml, \
        ishomc80_file,ishomc80_case,ishomc80_plot,ishomc80_xml, \
	gis10_file,gis10_case,gis10_plot,gis10_xml,job_path,bench_data,ncl_path,data_path,html_path,script_path,\
        diagnostic_flag,evolving_flag,circular_flag,confined_flag,
        ismip_hom_a80_flag,ismip_hom_a20_flag,ismip_hom_c_flag,gis_10km_flag):  

# using data, fill the web page with info about the cases
	test_file.write('<HTML>\n')
	test_file.write('<TITLE>Test Suite Diagnostics</TITLE>\n')
	test_file.write('<H1>Test Suite Diagnostics</H1>')

# link to descript_file about the test cases
	test_file.write('<TH ALIGN=LEFT><A HREF="test_descript.html">Test Suite Descriptions</A>\n')
	test_file.write('<BR>\n')

        dictionary = bit_list(job_path,bench_data)


#apply flag to turn off running test
        if diagnostic_flag == 1:

# Diagnostic Dome 30 stats
            if dictionary['diagnostic'] == 0:
                test_file.write('<H2>Diagnostic Dome 30 Test: <font color="green">Bit-for-Bit</font></H2>')
            else:
                test_file.write('<H2>Diagnostic Dome 30 Test: <font color="red">NOT Bit-for-Bit</font></H2>')
	
#put something here to flag BFB results and no need to do any more calculations
	    flag_to_plot_dome30d = 1
	    if flag_to_plot_dome30d:

# link to dome30d_file with descriptions about the test cases
		    test_file.write('<TH ALIGN=LEFT><A HREF="dome30d_details.html">Diagnostic Dome 30 Velocity Solver Details</A>\n')
		    test_file.write('<BR>\n')
                    failedt = VV_dome30details.ddetails(dome30d_file,job_path,ncl_path,data_path,html_path,bench_data)

		    test_file.write('<TH ALIGN=LEFT><A HREF="dome30d_xml.html">Solver Parameter Settings: Diagnostic Dome 30 XML Details</A>\n')
		    test_file.write('<BR>\n')
		    xml_path = job_path + '/dome30/diagnostic/trilinosOptions.xml'
		    bench_xml_path = job_path + '/bench/dome30/diagnostic/trilinosOptions.xml'
                    VV_utilities.xml(dome30d_xml,xml_path,bench_xml_path,ncl_path,html_path)

		    test_file.write('<TH ALIGN=LEFT><A HREF="dome30d_case.html">Diagnostic Dome 30 Case Details</A>\n')
		    test_file.write('<BR>\n')
                    configure_path = job_path + '/dome30/diagnostic/dome.30.JFNK.trilinos.config.1'
                    bench_configure_path = job_path + '/bench/dome30/diagnostic/dome.30.JFNK.trilinos.config.1'
        	    VV_utilities.conf(dome30d_case,configure_path,bench_configure_path,ncl_path,html_path)

		    test_file.write('<TH ALIGN=LEFT><A HREF="dome30d_plot.html">Diagnostic Dome 30 Plots</A>\n')
		    test_file.write('<BR>\n')
                    if failedt != 0:
                        dome30d_plot.write("<H2>Diagnostic Dome 30 Test failed, plots may not be generated</H2><br>")
                    checkpath = job_path + '/dome30/diagnostic/data/dome.1.nc'
                    checkpath2 = job_path + '/dome30/diagnostic/data/dome.4.nc'
                    noplot = VV_checks.emptycheck(checkpath)
                    noplot1 = noplot
                    noplot = VV_checks.emptycheck(checkpath2)
                    if noplot1 != 1 and noplot != 1:
                        VV_dome30details.dplot(dome30d_plot,job_path,ncl_path,html_path,script_path,bench_data)

# Time stamping
	    strrand = ''
	    mode = os.stat(job_path + '/dome30/diagnostic').st_mtime
	    mode = mode - 14400
	    mode = time.gmtime(mode)
	    ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
	    strrand = '<b>Time of last access: ' + str(ctime) + '</b>'
	    test_file.write(strrand)

        else:
            print "NOT RUNNING DIAGNOSTIC DOME30 TESTCASE"


#apply flag to turn off running test
        if evolving_flag == 1:

# Evolving Dome 30 stats
            if dictionary['evolving'] == 0:
                test_file.write('<H2>Evolving Dome 30 Test: <font color="green">Bit-for-Bit</font></H2>')
            else:
                test_file.write('<H2>Evolving Dome 30 Test: <font color="red">NOT Bit-for-Bit</font></H2>')

# put something here to flag BFB results and no need to do any more calculations
	    flag_to_plot_dome30e = 1
	    if flag_to_plot_dome30e:

# link to dome30e_file with descriptions about the test cases
		    test_file.write('<TH ALIGN=LEFT><A HREF="dome30e_details.html">Evolving Dome 30 Velocity Solver Details</A>\n')
		    test_file.write('<BR>\n')
        	    failedt = VV_dome30details.edetails(dome30e_file,job_path,ncl_path,data_path,html_path,bench_data)

		    test_file.write('<TH ALIGN=LEFT><A HREF="dome30e_xml.html">Solver Parameter Settings: Evolving Dome 30 XML Details</A>\n')
		    test_file.write('<BR>\n')
		    xml_path = job_path + '/dome30/evolving/trilinosOptions.xml'
		    bench_xml_path = job_path + '/bench/dome30/evolving/trilinosOptions.xml'
		    VV_utilities.xml(dome30e_xml,xml_path,bench_xml_path,ncl_path,html_path)

                    test_file.write('<TH ALIGN=LEFT><A HREF="dome30e_case.html">Evolving Dome 30 Case Details</A>\n')
		    test_file.write('<BR>\n')
                    configure_path = job_path + '/dome30/evolving/dome.30.JFNK.trilinos.config.15'
                    bench_configure_path = job_path + '/bench/dome30/evolving/dome.30.JFNK.trilinos.config.15'
        	    VV_utilities.conf(dome30e_case,configure_path,bench_configure_path,ncl_path,html_path)

		    test_file.write('<TH ALIGN=LEFT><A HREF="dome30e_plot.html">Evolving Dome 30 Plots</A>\n')
		    test_file.write('<BR>\n')
                    if failedt != 0:
                        dome30e_plot.write("<H2>Evolving Dome 30 Test failed, plots may not be generated</H2><br>")
                    checkpath = job_path + '/dome30/evolving/data/dome.9.nc'
                    checkpath2 = job_path + '/dome30/evolving/data/dome.15.nc'
                    noplot = VV_checks.emptycheck(checkpath)
                    noplot1 = noplot
                    noplot = VV_checks.emptycheck(checkpath2)
                    if noplot != 1 and noplot != 1:
                        VV_dome30details.eplot(dome30e_plot,job_path,ncl_path,html_path,script_path,bench_data)

# Time stamping
	    mode = os.stat(job_path + '/dome30/evolving').st_mtime
	    mode = mode - 14400
	    mode = time.gmtime(mode)
	    ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
	    strrand = '<b>Time of last access: ' + ctime + '</b>'
	    test_file.write(strrand)

        else:
            print "NOT RUNNING EVOLVING DOME30 TESTCASE"


#apply flag to turn off running test
        if circular_flag == 1:

# Circular Shelf stats
            if dictionary['circular'] == 0:
                test_file.write('<H2>Circular Shelf Test: <font color="green">Bit-for-Bit</font></H2>')
            else:
                test_file.write('<H2>Circular Shelf Test: <font color="red">NOT Bit-for-Bit</font></H2>')


# put something here to flag BFB results and no need to do any more calculations
	    flag_to_plot_circ = 1
    	    if flag_to_plot_circ:

		    test_file.write('<TH ALIGN=LEFT><A HREF="circ_details.html">Circular Shelf Velocity Solver Details</A>\n')
		    test_file.write('<BR>\n')
        	    failedt = VV_shelfdetails.circdetails(circ_file,job_path,bench_data)

		    test_file.write('<TH ALIGN=LEFT><A HREF="circ_xml.html">Solver Parameter Settings: Circular Shelf XML Details</A>\n')
                    test_file.write('<BR>\n')
                    xml_path = job_path + '/circular-shelf/trilinosOptions.xml'
                    bench_xml_path = job_path + '/bench/circular-shelf/trilinosOptions.xml'
                    VV_utilities.xml(circ_xml,xml_path,bench_xml_path,ncl_path,html_path)
                
                    test_file.write('<TH ALIGN=LEFT><A HREF="circ_case.html">Circular Shelf Case Details</A>\n')
		    test_file.write('<BR>\n')
                    configure_path = job_path + '/circular-shelf/circular-shelf.JFNK.config'
                    bench_configure_path = job_path + '/bench/circular-shelf/circular-shelf.JFNK.config'
        	    VV_utilities.conf(circ_case,configure_path,bench_configure_path,ncl_path,html_path)

		    test_file.write('<TH ALIGN=LEFT><A HREF="circ_plot.html">Circular Shelf Plots</A>\n')
		    test_file.write('<BR>\n')
                    if failedt != 0:
                        circ_plot.write("<H2>Circular Shelf Test failed, plots may not be generated</H2><br>")
                    checkpath = job_path + '/circular-shelf/data/circular-shelf.gnu.JFNK.nc'
                    noplot = VV_checks.emptycheck(checkpath)
                    if noplot != 1:
                        VV_shelfdetails.circplot(circ_plot,job_path,ncl_path,html_path,script_path,bench_data)

# Time stamping
	    mode = os.stat(job_path + '/circular-shelf').st_mtime
	    mode = mode - 14400
	    mode = time.gmtime(mode)
	    ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
	    strrand = '<b>Time of last access: ' + ctime + '</b>'
	    test_file.write(strrand)
	
        else:
            print "NOT RUNNING CIRCULAR SHELF TESTCASE"


#apply flag to turn off running test
        if confined_flag == 1:

# Confined Shelf stats
            if dictionary['confined'] == 0:
                test_file.write('<H2>Confined Shelf Test: <font color="green">Bit-for-Bit</font></H2>')
            else:
                test_file.write('<H2>Confined Shelf Test: <font color="red">NOT Bit-for-Bit</font></H2>')

# put something here to flag BFB results and no need to do any more calculations
	    flag_to_plot_conf = 1
	    if flag_to_plot_conf:

		    test_file.write('<TH ALIGN=LEFT><A HREF="conf_details.html">Confined Shelf Velocity Solver Details</A>\n')
		    test_file.write('<BR>\n')
        	    failedt = VV_shelfdetails.confdetails(conf_file,job_path,bench_data)

		    test_file.write('<TH ALIGN=LEFT><A HREF="conf_xml.html">Solver Parameter Details: Confined Shelf XML Details</A>\n')
                    test_file.write('<BR>\n')
                    xml_path = job_path + '/confined-shelf/trilinosOptions.xml'
                    bench_xml_path = job_path + '/bench/confined-shelf//trilinosOptions.xml'
                    VV_utilities.xml(conf_xml,xml_path,bench_xml_path,ncl_path,html_path)

                    test_file.write('<TH ALIGN=LEFT><A HREF="conf_case.html">Confined Shelf Case Details</A>\n')
		    test_file.write('<BR>\n')
                    configure_path = job_path + '/confined-shelf/confined-shelf.JFNK.config'
                    bench_configure_path = job_path + '/bench/confined-shelf/confined-shelf.JFNK.config'
        	    VV_utilities.conf(conf_case,configure_path,bench_configure_path,ncl_path,html_path)

		    test_file.write('<TH ALIGN=LEFT><A HREF="conf_plot.html">Confined Shelf Plot</A>\n')
		    test_file.write('<BR>\n')
                    if failedt != 0:
                        conf_plot.write("<H2>Confined Shelf Test failed, plots may not be generated</H2><br>")
                    checkpath = job_path + '/confined-shelf/data/confined-shelf.gnu.JFNK.nc'
                    noplot = VV_checks.emptycheck(checkpath)
                    if noplot != 1:
                        VV_shelfdetails.confplot(conf_plot,job_path,ncl_path,html_path,script_path,bench_data)

# Time stamping
	    mode = os.stat(job_path + '/confined-shelf').st_mtime
	    mode = mode - 14400
	    mode = time.gmtime(mode)
	    ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
	    strrand = '<b>Time of last access: ' + ctime + '</b>'
	    test_file.write(strrand)

        else:
            print "NOT RUNNING CONFINED SHELF TESTCASE"


#apply flag to turn off running test
        if ismip_hom_a80_flag == 1:

# ISMIP HOM A 80km stats
            if dictionary['ismip-hom-a80'] == 0:
                test_file.write('<H2>ISMIP HOM A 80KM Test: <font color="green">Bit-for-Bit</font></H2>')
            else:
                test_file.write('<H2>ISMIP HOM A 80KM Test: <font color="red">NOT Bit-for-Bit</font></H2>')

# put something here to flag BFB results and no need to do any more calculations
	    flag_to_plot_iha80 = 1
	    if flag_to_plot_iha80:

		    test_file.write('<TH ALIGN=LEFT><A HREF="ishoma80_details.html">ISMIP HOM A 80km Velocity Solver Details</A>\n')
		    test_file.write('<BR>\n')
        	    failedt = VV_ismip.a80details(ishoma80_file,job_path,bench_data)

		    test_file.write('<TH ALIGN=LEFT><A HREF="ishoma80_xml.html">Solver Parameter Details: ISMIP HOM A 80km XML Details</A>\n')
                    test_file.write('<BR>\n')
                    xml_path = job_path + '/ismip-hom-a/80km/trilinosOptions.xml'
                    bench_xml_path = job_path + '/bench/ismip-hom-a/80km/trilinosOptions.xml'
                    VV_utilities.xml(ishoma80_xml,xml_path,bench_xml_path,ncl_path,html_path)
                
                    test_file.write('<TH ALIGN=LEFT><A HREF="ishoma80_case.html">ISMIP HOM A 80km Case Details</A>\n')
		    test_file.write('<BR>\n')
                    configure_path = job_path + '/ismip-hom-a/80km/ishom.a.80km.JFNK.trilinos.config'
                    bench_configure_path = job_path + '/bench/ismip-hom-a/80km/ishom.a.80km.JFNK.trilinos.config'
        	    VV_utilities.conf(ishoma80_case,configure_path,bench_configure_path,ncl_path,html_path)

		    test_file.write('<TH ALIGN=LEFT><A HREF="ishoma80_plot.html">ISMIP HOM A 80km Plots</A>\n')
		    test_file.write('<BR>\n')
                    if failedt != 0:
                        ishoma80_plot.write("<H2>ISMIP HOM A 80km Test failed, plots may not be generated</H2><br>")
                    checkpath = job_path + '/ismip-hom-a/80km/data/ishom.a.80km.JFNK.out.nc'
                    noplot = VV_checks.emptycheck(checkpath)
                    if noplot != 1:
                        VV_ismip.a80plot(ishoma80_plot,job_path,ncl_path,html_path,script_path,bench_data)

# Time stamping
	    mode = os.stat(job_path + '/ismip-hom-a/80km').st_mtime
	    mode = mode - 14400
	    mode = time.gmtime(mode)
	    ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
	    strrand = '<b>Time of last access: ' + ctime + '</b>'
	    test_file.write(strrand)

        else:
            print "NOT RUNNING ISMIP HOM A 80KM TESTCASE"


#apply flag to turn off running test
        if ismip_hom_a20_flag == 1:
 
# ISMIP HOM A 20km stats
            if dictionary['ismip-hom-a20'] == 0:
                test_file.write('<H2>ISMIP HOM A 20KM Test: <font color="green">Bit-for-Bit</font></H2>')
            else:
                test_file.write('<H2>ISMIP HOM A 20KM Test: <font color="red">NOT Bit-for-Bit</font></H2>')

# put something here to flag BFB results and no need to do any more calculations
            flag_to_plot_iha20 = 1
            if flag_to_plot_iha20:

                test_file.write('<TH ALIGN=LEFT><A HREF="ishoma20_details.html">ISMIP HOM A 20km Velocity Solver Details</A>\n')
                test_file.write('<BR>\n')
                failedt = VV_ismip.a20details(ishoma20_file,job_path,bench_data)

                test_file.write('<TH ALIGN=LEFT><A HREF="ishoma20_xml.html">Solver Parameter Details: ISMIP HOM A 20km XML Details</A>\n')
                test_file.write('<BR>\n')
                xml_path = job_path + '/ismip-hom-a/20km/trilinosOptions.xml'
                bench_xml_path = job_path + '/bench/ismip-hom-a/20km/trilinosOptions.xml'
                VV_utilities.xml(ishoma20_xml,xml_path,bench_xml_path,ncl_path,html_path)
                
                test_file.write('<TH ALIGN=LEFT><A HREF="ishoma20_case.html">ISMIP HOM A 20km Case Details</A>\n')
                test_file.write('<BR>\n')
                configure_path = job_path + '/ismip-hom-a/20km/ishom.a.20km.JFNK.trilinos.config'
                bench_configure_path = job_path + '/bench/ismip-hom-a/20km/ishom.a.20km.JFNK.trilinos.config'
                VV_utilities.conf(ishoma20_case,configure_path,bench_configure_path,ncl_path,html_path)
                test_file.write('<TH ALIGN=LEFT><A HREF="ishoma20_plot.html">ISMIP HOM A 20km Plots</A>\n')
                test_file.write('<BR>\n')
                if failedt != 0:
                    ishoma20_plot.write("<H2>ISMIP HOM A 20 Test failed, plots may not be generated</H2><br>")
                checkpath = job_path + '/ismip-hom-a/20km/data/ishom.a.20km.JFNK.out.nc'
                noplot = VV_checks.emptycheck(checkpath)
                if noplot != 1:
                    VV_ismip.a20plot(ishoma20_plot,job_path,ncl_path,html_path,script_path,bench_data)
 
# Time stamping
            mode = os.stat(job_path + '/ismip-hom-a/20km').st_mtime
            mode = mode - 14400
            mode = time.gmtime(mode)
            ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
            strrand = '<b>Time of last access: ' + ctime + '</b>'
            test_file.write(strrand)
 
        else:
            print "NOT RUNNING ISMIP HOM A 20KM TESTCASE"


#apply flag to turn off running test
        if ismip_hom_c_flag == 1:

# ISMIP HOM C stats
            if dictionary['ismip-hom-c'] == 0:
                test_file.write('<H2>ISMIP HOM C 80KM Test: <font color="green">Bit-for-Bit</font></H2>')
            else:
                test_file.write('<H2>ISMIP HOM C 80KM Test: <font color="red">NOT Bit-for-Bit</font></H2>')

# put something here to flag BFB results and no need to do any more calculations
	    flag_to_plot_ihc = 1
	    if flag_to_plot_ihc:

		    test_file.write('<TH ALIGN=LEFT><A HREF="ishomc80_details.html">ISMIP HOM C 80km Velocity Solver Details</A>\n')
		    test_file.write('<BR>\n')
        	    failedt = VV_ismip.c80details(ishomc80_file,job_path,bench_data)

		    test_file.write('<TH ALIGN=LEFT><A HREF="ishomc80_xml.html">Solver Parameter Settings: ISMIP HOM C 80km XML Details</A>\n')
                    test_file.write('<BR>\n')
                    xml_path = job_path + '/ismip-hom-c/80km/trilinosOptions.xml'
                    bench_xml_path = job_path + '/bench/ismip-hom-c/80km/trilinosOptions.xml'
                    VV_utilities.xml(ishomc80_xml,xml_path,bench_xml_path,ncl_path,html_path)
                
                    test_file.write('<TH ALIGN=LEFT><A HREF="ishomc80_case.html">ISMIP HOM C 80km Case Details</A>\n')
		    test_file.write('<BR>\n')
                    configure_path = job_path + '/ismip-hom-c/80km/ishom.c.80km.JFNK.trilinos.config'
                    bench_configure_path = job_path + '/bench/ismip-hom-c/80km/ishom.c.80km.JFNK.trilinos.config'
        	    VV_utilities.conf(ishomc80_case,configure_path,bench_configure_path,ncl_path,html_path)

		    test_file.write('<TH ALIGN=LEFT><A HREF="ishomc80_plot.html">ISMIP HOM C 80km Plots</A>\n')
		    test_file.write('<BR>\n')
                    if failedt != 0:
                        ishomc80_plot.write("<H2>ISMIP HOM C Test failed, plots may not be generated</H2><br>")
                    checkpath = job_path + '/ismip-hom-c/80km/data/ishom.c.80km.JFNK.out.nc'
                    noplot = VV_checks.emptycheck(checkpath)
                    if noplot != 1:
                        VV_ismip.c80plot(ishomc80_plot,job_path,ncl_path,html_path,script_path,bench_data)

# Time stamping
	    mode = os.stat(job_path + '/ismip-hom-c/80km').st_mtime
	    mode = mode - 14400
	    mode = time.gmtime(mode)
	    ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
	    strrand = '<b>Time of last access: ' + ctime + '</b>'
	    test_file.write(strrand)

        else:
            print "NOT RUNNING ISMIP HOM C TESTCASE"


#apply flag to turn off running test
        if gis_10km_flag == 1:

# GIS 10km stats
            if dictionary['gis_10km'] == 0:
                test_file.write('<H2>GIS 10KM Test: <font color="green">Bit-for-Bit</font></H2>')
            else:
                test_file.write('<H2>GIS 10KM Test: <font color="red">NOT Bit-for-Bit</font></H2>')

# put something here to flag BFB results between data and bench and pgi and gnu etc.
	    flag_to_plot_gis10km = 1
	    if flag_to_plot_gis10km:

		    test_file.write('<TH ALIGN=LEFT><A HREF="gis10_details.html">GIS 10km Velocity Solver Details</A>\n')
		    test_file.write('<BR>\n')
        	    failedt = VV_gis10details.details(gis10_file,job_path,ncl_path,data_path,html_path,bench_data)

		    test_file.write('<TH ALIGN=LEFT><A HREF="gis10_xml.html">Solver Parameter Settings: GIS 10km XML Details</A>\n')
                    test_file.write('<BR>\n')
                    xml_path = job_path + '/gis_10km/trilinosOptions.xml'
                    bench_xml_path = job_path + '/bench/gis_10km/trilinosOptions.xml'
                    VV_utilities.xml(gis10_xml,xml_path,bench_xml_path,ncl_path,html_path)
                
                    test_file.write('<TH ALIGN=LEFT><A HREF="gis10_case.html">GIS 10km Case Details</A>\n')
		    test_file.write('<BR>\n')
                    configure_path = job_path + '/gis_10km/gis_10km.JFNK.trilinos.10.config'
                    bench_configure_path = job_path + '/bench/gis_10km/gis_10km.JFNK.trilinos.10.config'
        	    VV_utilities.conf(gis10_case,configure_path,bench_configure_path,ncl_path,html_path)

		    test_file.write('<TH ALIGN=LEFT><A HREF="gis10_plot.html">GIS 10km Plots</A>\n')
		    test_file.write('<BR>\n')
                    if failedt != 0:
                        gis10_plot.write("<H2>GIS 10km Test failed, plots may not be generated</H2><br>")
                    checkpath = job_path + '/gis_10km/data/gis_10km.seacism.nc'
                    noplot = VV_checks.emptycheck(checkpath)
                    if noplot != 1:
                        VV_gis10details.gis10_plot(gis10_plot,job_path,ncl_path,html_path,script_path,bench_data)

# Time stamping
	    mode = os.stat(job_path + '/gis_10km').st_mtime
	    mode = mode - 14400
	    mode = time.gmtime(mode)
	    ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
	    strrand = '<b>Time of last access: ' + ctime + '</b>\n'
	    test_file.write(strrand)

        else:
            print "NOT RUNNING GIS 10KM TESTCASE"


        test_file.write('<BR>\n')
        test_file.write('<BR>\n')
        test_file.write('<TH ALIGN=LEFT><A HREF="GIS-main-diag.html">Home</A>\n')

	test_file.write('</HTML>\n')
	test_file.close()

#	descript_file = open(options.html_path + '/test_descript.html', 'w')
	descript_file.write('<HTML>\n')
	descript_file.write('<TITLE>Descriptions about the Test Suite</TITLE>\n')
	descript_file.write('<H2>Test Suite Details</H2>')
	descript_file.write('<BR>\n')
	descript_file.write('The Diagnostic Dome 30 test case \n')
	descript_file.write('<BR>\n')
	descript_file.write('  Attributes -  \n')
	descript_file.write('<BR>\n')
	descript_file.write('  What does it test? \n')
	descript_file.write('<BR><BR>\n')
	descript_file.write('The Evolving Dome 30 test case \n')
	descript_file.write('<BR>\n')
	descript_file.write('  Attributes \n')
	descript_file.write('<BR>\n')
	descript_file.write('  What does it test? \n')
	descript_file.write('<BR><BR>\n')
	descript_file.write('The Circular Shelf test case \n')
	descript_file.write('<BR>\n')
	descript_file.write('  Attributes \n')
	descript_file.write('<BR>\n')
	descript_file.write('  What does it test? \n')
	descript_file.write('<BR><BR>\n')
	descript_file.write('The Confined Shelf test case \n')
	descript_file.write('<BR>\n')
	descript_file.write('  Attributes \n')
	descript_file.write('<BR>\n')
	descript_file.write('  What does it test? \n')
	descript_file.write('<BR><BR>\n')
	descript_file.write('The ISMIP HOM A 80km test case \n')
	descript_file.write('<BR>\n')
	descript_file.write('  Attributes \n')
	descript_file.write('<BR>\n')
	descript_file.write('  What does it test? simulates steady ice flow with no basal slip over a sinusoidally varying bed with periodic boundary conditions\n')
	descript_file.write('<BR><BR>\n')
	descript_file.write('The ISMIP HOM C 80km test case \n')
	descript_file.write('<BR>\n')
	descript_file.write('  Attributes \n')
	descript_file.write('<BR>\n')
	descript_file.write('  What does it test? simulates steady ice flow with sinusoidally carrying basal traction over a flat bed with periodic boundary conditions \n')
	descript_file.write('<BR><BR>\n')
	descript_file.write('The Greenland Ice Sheet 10km test case \n')
	descript_file.write('<BR>\n')
	descript_file.write('  Attributes \n')
	descript_file.write('<BR>\n')
	descript_file.write('  What does it test? \n')
	descript_file.write('<BR><BR>\n')
	descript_file.write('</HTML>\n')
	descript_file.close()

#	dome30_file.write('</HTML>\n')
#	dome30_file.close()

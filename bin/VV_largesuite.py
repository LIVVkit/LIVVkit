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
import VV_timing
import VV_timing_check

#check to see which driver was used for current run file
#and then runs check to make sure all 10 timing files and current run file exist
def driver_check(perf_test,dome60_flag,dome120_flag,dome240_flag,dome500_flag,dome1000_flag,\
                gis_1km_flag,gis_2km_flag,gis_4km_flag):
    dictionary_dycore = {}
    dictionary_large = {}
    dictionary_c_flag = {}
    flag = 0
#dome60
    if dome60_flag == 1:
        current_run_config = perf_test + '/dome60/configure_files/dome.60.config'
        driver,c_flag = VV_checks.driver_check(current_run_config)
        dictionary_dycore['dome60c'] = driver
        dictionary_c_flag['dome60'] = c_flag
        current_run_path = perf_test + '/dome60/data/out.60.' + dictionary_dycore['dome60c'] + '.timing'
        timing_path_10runs = perf_test + '/bench/dome60/data_titan/out.60.glide.timing'
        test = 'dome60'
        dictionary_large['dome60'] = VV_timing_check.timing_check(timing_path_10runs,current_run_path,flag,test)
    else:
        dictionary_dycore['dome60c'] = 0
        dictionary_large['dome60'] = 0
        
#dome120
    if dome120_flag == 1:
        current_run_config = perf_test + '/dome120/configure_files/dome.120.config'
        driver,c_flag = VV_checks.driver_check(current_run_config)
        dictionary_dycore['dome120c'] = driver
        dictionary_c_flag['dome120'] = c_flag
        current_run_path = perf_test + '/dome120/data/out.120.' + dictionary_dycore['dome120c'] + '.timing'
        timing_path_10runs = perf_test + '/bench/dome120/data_titan/out.120.glide.timing'
        test = 'dome120'
        dictionary_large['dome120'] = VV_timing_check.timing_check(timing_path_10runs,current_run_path,flag,test)
    else:
        dictionary_dycore['dome120c'] = 0
        dictionary_large['dome120'] = 0
#dome240
    if dome240_flag == 1:
        current_run_config = perf_test + '/dome240/configure_files/dome.240.config'
        driver,c_flag = VV_checks.driver_check(current_run_config)
        dictionary_dycore['dome240c'] = driver
        dictionary_c_flag['dome240'] = c_flag
        current_run_path = perf_test + '/dome240/data/out.240.' + dictionary_dycore['dome240c'] + '.timing'
        timing_path_10runs = perf_test + '/bench/dome240/data_titan/out.240.glide.timing'
        test = 'dome240'
        dictionary_large['dome240'] = VV_timing_check.timing_check(timing_path_10runs,current_run_path,flag,test)
    else:
        dictionary_dycore['dome240c'] = 0
        dictionary_large['dome240'] = 0
#dome500
    if dome500_flag == 1:
        current_run_config = perf_test + '/dome500/configure_files/dome.500.config'
        driver,c_flag = VV_checks.driver_check(current_run_config)
        dictionary_dycore['dome500c'] = driver
        dictionary_c_flag['dome500'] = c_flag
        current_run_path = perf_test + '/dome500/data/out.500.' + dictionary_dycore['dome500c'] + '.timing'
        timing_path_10runs = perf_test + '/bench/dome500/data_titan/out.500.glide.timing'
        test = 'dome500'
        dictionary_large['dome500'] = VV_timing_check.timing_check(timing_path_10runs,current_run_path,flag,test)
    else:
        dictionary_dycore['dome500c'] = 0
        dictionary_large['dome500'] = 0
#dome1000
    if dome1000_flag == 1:
        current_run_config = perf_test + '/dome1000/configure_files/dome.1000.config'
        driver,c_flag = VV_checks.driver_check(current_run_config)
        dictionary_dycore['dome1000c'] = driver
        dictionary_c_flag['dome1000'] = c_flag
        current_run_path = perf_test + '/dome1000/data/out.1000.' + dictionary_dycore['dome1000c'] + '.timing'
        timing_path_10runs = perf_test + '/bench/dome1000/data_titan/out.1000.glide.timing'
        test = 'dome1000'
        dictionary_large['dome1000'] = VV_timing_check.timing_check(timing_path_10runs,current_run_path,flag,test)
    else:
        dictionary_dycore['dome1000c'] = 0
        dictionary_large['dome1000'] = 0

    return dictionary_dycore, dictionary_large, dictionary_c_flag

#timing check to see if all tests are within range
def time_check(perf_test,dome60_flag,dome120_flag,dome240_flag,dome500_flag,dome1000_flag,\
                gis_1km_flag,gis_2km_flag,gis_4km_flag):
    dictionary_large_gis = {}
    flag = 0
#gis4km
    if gis_4km_flag == 1:
        current_run_path = perf_test + '/gis_4km/data/out.gis.4km.albany.n256_10timesteps.timing'
        timing_path_10runs = perf_test + '/bench/gis_4km/data_titan/out.gis.4km.albany.timing'
        test = 'gis4km'
        dictionary_large_gis['gis4km'] = VV_timing_check.timing_check(timing_path_10runs,current_run_path,flag,test)
    else:
        dictionary_large_gis['gis4km'] = 0
#gis2km
    if gis_2km_flag == 1:
        current_run_path = perf_test + '/gis_4km/data/out.gis.4km.glissade.timing'
        timing_path_10runs = perf_test + '/bench/gis_2km/data_titan/out.gis.2km.glissade.timing'
        test = 'gis2km'
        dictionary_large_gis['gis2km'] = VV_timing_check.timing_check(timing_path_10runs,current_run_path,flag,test)
    else:
        dictionary_large_gis['gis2km'] = 0
#gis1km
    if gis_1km_flag == 1:
        current_run_path = perf_test + '/gis_1km/data/out.gis.1km.albany.n256_0timesteps.timing'
        timing_path_10runs = perf_test + '/bench/gis_1km/data_titan/out.gis.1km.glissade.timing'
        test = 'gis1km'
        dictionary_large_gis['gis1km'] = VV_timing_check.timing_check(timing_path_10runs,current_run_path,flag,test)
    else:
        dictionary_large_gis['gis1km'] = 0
    return dictionary_large_gis

def large_tests(descript_file,large_test_file,dome60_file,dome60_case,dome60_time,dome60_plot, \
    dome120_file,dome120_case,dome120_time,dome120_plot,dome240_file,dome240_case,dome240_time,dome240_plot, \
    dome500_file,dome500_case,dome500_time,dome500_plot,dome1000_file,dome1000_case,dome1000_time,dome1000_plot, \
    gis1km_file,gis1km_case,gis1km_time,gis1km_plot,gis2km_file,gis2km_case,gis2km_time,gis2km_plot, \
    gis4km_file,gis4km_case,gis4km_time,gis4km_plot, \
    perf_test,ncl_path,html_path,script_path, \
    dome60_flag,dome120_flag,dome240_flag,dome500_flag,dome1000_flag, \
    gis_1km_flag,gis_2km_flag,gis_4km_flag,data_dir):

# using data, fill the web page with info about the cases
    large_test_file.write('<HTML>\n')
    large_test_file.write('<TITLE>Performance and Analysis Test Suite</TITLE>\n')
    large_test_file.write('<BODY BGCOLOR="#CADFE0">\n') 
    large_test_file.write('<H1>Performance and Analysis Test Suite</H1>')

# link to descript_file about the test cases
    large_test_file.write('<TH ALIGN=LEFT><A HREF="largetest_descript.html">Test Suite Descriptions</A>\n')
    large_test_file.write('<BR>\n')

    dictionary_large_gis = time_check(perf_test,dome60_flag,dome120_flag,dome240_flag, \
                    dome500_flag,dome1000_flag,gis_1km_flag,gis_2km_flag,gis_4km_flag)

    dictionary_dycore,dictionary_large,dictionary_c_flag = driver_check(perf_test,dome60_flag,dome120_flag,dome240_flag, \
                                        dome500_flag,dome1000_flag,gis_1km_flag,gis_2km_flag,gis_4km_flag)

#apply flag to turn off running test
    if dome60_flag == 1:

# Dome 60 stats
        print "running dome60 testcase"
        large_test_file.write('<BR>\n')
        if dictionary_large['dome60'] == 0:
            large_test_file.write('<H2>Diagnostic Dome 60 Test: <font color="blue"> Test Within Expected Performance Range</font></H2>')
        elif dictionary_large['dome60'] == 1:
            large_test_file.write('<H2>Diagnostic Dome 60 Test: <font color="red">Test Slower Than Expected Performance Range</font></H2>')
        else:
            large_test_file.write('<H2>Diagnostic Dome 60 Test: <font color="#4CC417">Test Faster Than Expected Performance Range</font></H2>')

#put something here to flag BFB results and no need to do any more calculations
        flag_to_plot_dome60 = 1
        if flag_to_plot_dome60:

# link to dome60_file with descriptions about the test cases
            large_test_file.write('<TH ALIGN=LEFT><A HREF="dome60_details.html">Velocity Solver Details</A>\n')
            large_test_file.write('<BR>\n')
            number = '60'
            failedt = VV_largetestdetails.detailsdome(dome60_file,perf_test,data_dir,dictionary_dycore['dome60c'],number)

            large_test_file.write('<TH ALIGN=LEFT><A HREF="dome60_case.html">Case and Parameter Settings Details</A>\n')
            large_test_file.write('<BR>\n')
            xml_path = perf_test + '/dome60/trilinosOptions.xml'
            bench_xml_path = perf_test + '/bench/dome60/trilinosOptions.xml'
            if os.path.isdir(perf_test + '/dome60/configure_files/') == True: 
                configure_path = perf_test + '/dome60/configure_files/dome.60.' + dictionary_dycore['dome60c'] + '.config'
                bench_configure_path = perf_test + '/bench/dome60/configure_files/dome.60.glide.config'
            else:
                configure_path = perf_test + '/dome60/dome.60.' + dictionary_dycore['dome60c'] + '.config'
                bench_configure_path = perf_test + '/bench/dome60/dome.60.glide.config'
            c_flag = dictionary_c_flag['dome60']
            VV_utilities.confxml(dome60_case,configure_path,bench_configure_path,xml_path,bench_xml_path,c_flag)

            large_test_file.write('<TH ALIGN=LEFT><A HREF="dome60_timing.html">Timing Details</A>\n')
            large_test_file.write('<BR>\n')
            flag = 0
            timing_path_10runs = perf_test + '/bench/dome60/data_titan/out.60.glide.timing'
            current_run_path = perf_test + '/dome60/data/out.60.' + dictionary_dycore['dome60c'] + '.timing'
            VV_timing.timing_table_current_run(dome60_time,timing_path_10runs,current_run_path,flag)

# Time stamping
        strrand = ''
        mode = os.stat(perf_test + '/dome60/').st_mtime
        mode = mode - 14400
        mode = time.gmtime(mode)
        ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
        strrand = '<b>Time of Last Simulation: ' + str(ctime) + '</b>'
        large_test_file.write(strrand)
        large_test_file.write('<BR>\n')

    else:
        print "NOT RUNNING DOME60 TESTCASE"


#apply flag to turn off running test
    if dome120_flag == 1:

# Dome 120 stats
        print "running dome120 testcase"
        large_test_file.write('<BR>\n')
        if dictionary_large['dome120'] == 0:
            large_test_file.write('<H2>Diagnostic Dome 120 Test: <font color="blue">Test Within Expected Performance Range</font></H2>')
        elif dictionary_large['dome120'] == 1:
            large_test_file.write('<H2>Diagnostic Dome 120 Test: <font color="red">Test Slower Than Expected Performance Range</font></H2>')
        else:
            large_test_file.write('<H2>Diagnostic Dome 120 Test: <font color="#4CC417">Test Faster Than Expected Performance Range</font></H2>')

#put something here to flag BFB results and no need to do any more calculations
        flag_to_plot_dome120 = 1
        if flag_to_plot_dome120:

# link to dome120_file with descriptions about the test cases
            large_test_file.write('<TH ALIGN=LEFT><A HREF="dome120_details.html">Velocity Solver Details</A>\n')
            large_test_file.write('<BR>\n')
            number = '120'
            failedt = VV_largetestdetails.detailsdome(dome120_file,perf_test,data_dir,dictionary_dycore['dome120c'],number)

            large_test_file.write('<TH ALIGN=LEFT><A HREF="dome120_case.html">Case and Parameter Settings Details</A>\n')
            large_test_file.write('<BR>\n')
            xml_path = perf_test + '/dome120/trilinosOptions.xml'
            bench_xml_path = perf_test + '/bench/dome120/trilinosOptions.xml'
            if os.path.isdir(perf_test + '/dome120/configure_files/') == True: 
                configure_path = perf_test + '/dome120/configure_files/dome.120.' + dictionary_dycore['dome120c'] + '.config'
                bench_configure_path = perf_test + '/bench/dome120/configure_files/dome.120.glide.config'
            else:
                configure_path = perf_test + '/dome120/dome.120.' + dictionary_dycore['dome120c'] + '.config'
                bench_configure_path = perf_test + '/bench/dome120/dome.120.glide.config'
            c_flag = dictionary_c_flag['dome120']
            VV_utilities.confxml(dome120_case,configure_path,bench_configure_path,xml_path,bench_xml_path,c_flag)

            large_test_file.write('<TH ALIGN=LEFT><A HREF="dome120_timing.html">Timing Details</A>\n')
            large_test_file.write('<BR>\n')
            flag = 0
            timing_path_10runs = perf_test + '/bench/dome120/data_titan/out.120.glide.timing'
            current_run_path = perf_test + '/dome120/data/out.120.' + dictionary_dycore['dome120c'] + '.timing'
            VV_timing.timing_table_current_run(dome120_time,timing_path_10runs,current_run_path,flag)

# Time stamping
        strrand = ''
        mode = os.stat(perf_test + '/dome120/').st_mtime
        mode = mode - 14400
        mode = time.gmtime(mode)
        ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
        strrand = '<b>Time of Last Simulation: ' + str(ctime) + '</b>'
        large_test_file.write(strrand)
        large_test_file.write('<BR>\n')

    else:
        print "NOT RUNNING DOME120 TESTCASE"


#apply flag to turn off running test
    if dome240_flag == 1:

# Dome 240 stats
        print "running dome240 testcase"
        large_test_file.write('<BR>\n')
        if dictionary_large['dome240'] == 0:
            large_test_file.write('<H2>Diagnostic Dome 240 Test: <font color="blue">Test Within Expected Performance Range</font></H2>')
        elif dictionary_large['dome240'] == 1:
            large_test_file.write('<H2>Diagnostic Dome 240 Test: <font color="red">Test Slower Than Expected Performance Range</font></H2>')
        else:
            large_test_file.write('<H2>Diagnostic Dome 240 Test: <font color="#4CC417">Test Faster Than Expected Performance Range</font></H2>')

#put something here to flag BFB results and no need to do any more calculations
        flag_to_plot_dome240 = 1
        if flag_to_plot_dome240:

# link to dome240_file with descriptions about the test cases
            large_test_file.write('<TH ALIGN=LEFT><A HREF="dome240_details.html">Velocity Solver Details</A>\n')
            large_test_file.write('<BR>\n')
            number = '240'
            failedt = VV_largetestdetails.detailsdome(dome240_file,perf_test,data_dir,dictionary_dycore['dome240c'],number)

            large_test_file.write('<TH ALIGN=LEFT><A HREF="dome240_case.html">Case and Parameter Settings Details</A>\n')
            large_test_file.write('<BR>\n')
            xml_path = perf_test + '/dome240/trilinosOptions.xml'
            bench_xml_path = perf_test + '/bench/dome240/trilinosOptions.xml'
            if os.path.isdir(perf_test + '/dome240/configure_files/') == True: 
                configure_path = perf_test + '/dome240/configure_files/dome.240.' + dictionary_dycore['dome240c'] + '.config'
                bench_configure_path = perf_test + '/bench/dome240/configure_files/dome.240.glide.config'
            else:
                configure_path = perf_test + '/dome240/dome.240.' + dictionary_dycore['dome240c'] + '.config'
                bench_configure_path = perf_test + '/bench/dome240/dome.240.glide.config'
            c_flag = dictionary_c_flag['dome240']
            VV_utilities.confxml(dome240_case,configure_path,bench_configure_path,xml_path,bench_xml_path,c_flag)

            large_test_file.write('<TH ALIGN=LEFT><A HREF="dome240_timing.html">Timing Details</A>\n')
            large_test_file.write('<BR>\n')
            flag = 0
            timing_path_10runs = perf_test + '/bench/dome240/data_titan/out.240.glide.timing'
            current_run_path = perf_test + '/dome240/data/out.240.' + dictionary_dycore['dome240c'] + '.timing'
            VV_timing.timing_table_current_run(dome240_time,timing_path_10runs,current_run_path,flag)

# Time stamping
        strrand = ''
        mode = os.stat(perf_test + '/dome240/').st_mtime
        mode = mode - 14400
        mode = time.gmtime(mode)
        ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
        strrand = '<b>Time of Last Simulation: ' + str(ctime) + '</b>'
        large_test_file.write(strrand)
        large_test_file.write('<BR>\n')

    else:
        print "NOT RUNNING DOME240 TESTCASE"


#apply flag to turn off running test
    if dome500_flag == 1:

# Dome 500 stats
        print "running dome500 testcase"
        large_test_file.write('<BR>\n')
        if dictionary_large['dome500'] == 0:
            large_test_file.write('<H2>Diagnostic Dome 500 Test: <font color="blude">Test Within Expected Performance Range</font></H2>')
        elif dictionary_large['dome500'] == 1:
            large_test_file.write('<H2>Diagnostic Dome 500 Test: <font color="red">Test Slower Than Expected Performance Range</font></H2>')
        else:
            large_test_file.write('<H2>Diagnostic Dome 500 Test: <font color="#4CC417">Test Faster Than Expected Performance Range</font></H2>')

#put something here to flag BFB results and no need to do any more calculations
        flag_to_plot_dome500 = 1
        if flag_to_plot_dome500:

# link to dome500_file with descriptions about the test cases
            large_test_file.write('<TH ALIGN=LEFT><A HREF="dome500_details.html">Velocity Solver Details</A>\n')
            large_test_file.write('<BR>\n')
            number = '500'
            failedt = VV_largetestdetails.detailsdome(dome500_file,perf_test,data_dir,dictionary_dycore['dome500c'],number)

            large_test_file.write('<TH ALIGN=LEFT><A HREF="dome500_case.html">Case and Parameter Settings Details</A>\n')
            large_test_file.write('<BR>\n')
            xml_path = perf_test + '/dome500/trilinosOptions.xml'
            bench_xml_path = perf_test + '/bench/dome500/trilinosOptions.xml'
            if os.path.isdir(perf_test + '/dome500/configure_files/') == True: 
                configure_path = perf_test + '/dome500/configure_files/dome.500.' + dictionary_dycore['dome500c'] + '.config'
                bench_configure_path = perf_test + '/bench/dome500/configure_files/dome.500.glide.config'
            else:
                configure_path = perf_test + '/dome500/dome.500.' + dictionary_dycore['dome500c'] + '.config'
                bench_configure_path = perf_test + '/bench/dome500/dome.500.glide.config'
            c_flag = dictionary_c_flag['dome500']
            VV_utilities.confxml(dome500_case,configure_path,bench_configure_path,xml_path,bench_xml_path,c_flag)
            
            large_test_file.write('<TH ALIGN=LEFT><A HREF="dome500_timing.html">Timing Details</A>\n')
            large_test_file.write('<BR>\n')
            flag = 0
            timing_path_10runs = perf_test + '/bench/dome500/data_titan/out.500.glide.timing'
            current_run_path = perf_test + '/dome500/data/out.500.' + dictionary_dycore['dome500c'] + '.timing'
            VV_timing.timing_table_current_run(dome500_time,timing_path_10runs,current_run_path,flag)

# Time stamping
        strrand = ''
        mode = os.stat(perf_test + '/dome500/').st_mtime
        mode = mode - 14400
        mode = time.gmtime(mode)
        ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
        strrand = '<b>Time of Last Simulation: ' + str(ctime) + '</b>'
        large_test_file.write(strrand)
        large_test_file.write('<BR>\n')

    else:
        print "NOT RUNNING DOME500 TESTCASE"


#apply flag to turn off running test
    if dome1000_flag == 1:

# Dome 1000 stats
        print "running dome1000 testcase"
        large_test_file.write('<BR>\n')
        if dictionary_large['dome1000'] == 0:
            large_test_file.write('<H2>Diagnostic Dome 1000 Test: <font color="blue">Test Within Expected Performance Range</font></H2>')
        elif dictionary_large['dome1000'] == 1:
            large_test_file.write('<H2>Diagnostic Dome 1000 Test: <font color="red">Test Slower Than Expected Performance Range</font></H2>')
        else:
            large_test_file.write('<H2>Diagnostic Dome 1000 Test: <font color="#4CC417">Test Faster Than Expected Performance Range</font></H2>')

#put something here to flag BFB results and no need to do any more calculations
        flag_to_plot_dome1000 = 1
        if flag_to_plot_dome1000:

# link to dome1000_file with descriptions about the test cases
            large_test_file.write('<TH ALIGN=LEFT><A HREF="dome500_details.html">Velocity Solver Details</A>\n')
            large_test_file.write('<BR>\n')
            number = '1000'
            failedt = VV_largetestdetails.detailsdome(dome1000_file,perf_test,data_dir,dictionary_dycore['dome1000c'],number)

            large_test_file.write('<TH ALIGN=LEFT><A HREF="dome1000_case.html">Case and Parameter Settings Details</A>\n')
            large_test_file.write('<BR>\n')
            xml_path = perf_test + '/dome1000/trilinosOptions.xml'
            bench_xml_path = perf_test + '/bench/dome1000/trilinosOptions.xml'
            if os.path.isdir(perf_test + '/dome1000/configure_files/') == True: 
                configure_path = perf_test + '/dome1000/configure_files/dome.1000.' + dicionary_dycore['dome1000c'] + '.config'
                bench_configure_path = perf_test + '/bench/dome1000/configure_files/dome.1000.glideconfig'
            else:
                configure_path = perf_test + '/dome1000/dome.1000.' + dictionary_dycore['dome1000c'] + '.config'
                bench_configure_path = perf_test + '/bench/dome1000/dome.1000.glide.config'
            c_flag = dictionary_c_flag['dome1000']
            VV_utilities.confxml(dome1000_case,configure_path,bench_configure_path,xml_path,bench_xml_path,c_flag)

            large_test_file.write('<TH ALIGN=LEFT><A HREF="dome1000_timing.html">Timing Details</A>\n')
            large_test_file.write('<BR>\n')
            flag = 0
            timing_path_10runs = perf_test + '/bench/dome1000/data_titan/out.1000.glide.timing'
            current_run_path = perf_test + '/dome1000/data/out.1000.' + dictionary_dycore['dome1000c'] + '.timing'
            VV_timing.timing_table_current_run(dome1000_time,timing_path_10runs,current_run_path,flag)

# Time stamping
        strrand = ''
        mode = os.stat(perf_test + '/dome1000/').st_mtime
        mode = mode - 14400
        mode = time.gmtime(mode)
        ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
        strrand = '<b>Time of Last Simulation: ' + str(ctime) + '</b>'
        large_test_file.write(strrand)
        large_test_file.write('<BR>\n')

    else:
        print "NOT RUNNING DOME1000 TESTCASE"


#apply flag to turn off running test
    if gis_4km_flag == 1:

# GIS 4km stats
        print "running gis4km testcase"
        large_test_file.write('<BR>\n')
        if dictionary_large_gis['gis4km'] == 0:
            large_test_file.write('<H2>GIS 4KM Test: <font color="blue">Test Within Expected Performance Range</font></H2>')
        elif dictionary_large_gis['gis4km'] == 1:
            large_test_file.write('<H2>GIS 4KM Test: <font color="red">Test Slower Than Expected Performance Range</font></H2>')
        else:
            large_test_file.write('<H2>GIS 4KM Test: <font color="#4CC417">Test Faster Than Expected Performance Range</font></H2>')

# put something here to flag BFB results between data and bench and pgi and gnu etc.
        flag_to_plot_gis4km = 1
        if flag_to_plot_gis4km:

            large_test_file.write('<TH ALIGN=LEFT><A HREF="gis4km_case.html">Case and Parameter Settings Details</A>\n')
            large_test_file.write('<BR>\n')
            xml_path = perf_test + '/gis_4km/trilinosOptions.xml'
            bench_xml_path = perf_test + '/bench/gis_4km/trilinosOptions.xml'
            if os.path.isdir(perf_test + '/gis_4km/configure_files/') == True: 
                configure_path = perf_test + '/gis_4km/configure_files/gis.4km.config'
                bench_configure_path = perf_test + '/bench/gis_4km/configure_files/gis.4km.config'
            else:
                configure_path = perf_test + '/gis_4km/gis.4km.config'
                bench_configure_path = perf_test + '/bench/gis_4km/gis.4km.config'
            c_flag = 0
            VV_utilities.confxml(gis4km_case,configure_path,bench_configure_path,xml_path,bench_xml_path,c_flag)

            large_test_file.write('<TH ALIGN=LEFT><A HREF="gis4km_timing.html">Timing Details</A>\n')
            large_test_file.write('<BR>\n')
            flag = 0
            timing_path_10runs = perf_test + '/bench/gis_4km/data_titan/out.gis.4km.albany.timing'
            current_run_path = perf_test + '/gis_4km/data/out.gis.4km.albany.n256_10timesteps.timing'
            VV_timing.timing_table_current_run(gis4km_time,timing_path_10runs,current_run_path,flag)
            
            #large_test_file.write('<TH ALIGN=LEFT><A HREF="gis4km_plot.html">Plots</A>\n')
            #large_test_file.write('<BR>\n')
            #if failedt != 0:
            #    gis4_plot.write("<H2>GIS 4km Test failed, plots may not be generated</H2><br>")
            #checkpath = perf_test + '/gis_4km/data/gis_4km.ice2sea.init.nc'
            #noplot = VV_checks.emptycheck(checkpath)
            #if noplot != 1:
            #    VV_gis4details.gis4_plot(gis4km_plot,perf_test,ncl_path,html_path,script_path,data_dir)

# Time stamping
        mode = os.stat(perf_test + '/gis_4km').st_mtime
        mode = mode - 14400
        mode = time.gmtime(mode)
        ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
        strrand = '<b>Time of Last Simulation: ' + ctime + '</b>\n'
        large_test_file.write(strrand)
        large_test_file.write('<BR>\n')

    else:
        print "NOT RUNNING GIS 4KM TESTCASE"


#apply flag to turn off running test
    if gis_2km_flag == 1:

# GIS 2km stats
        print "running gis2km testcase"
        large_test_file.write('<BR>\n')
        if dictionary_large_gis['gis2km'] == 0:
            large_test_file.write('<H2>GIS 2KM Test: <font color="blue">Test Within Expected Performance Range</font></H2>')
        elif dictionary_large_gis['gis2km'] == 1:
            large_test_file.write('<H2>GIS 2KM Test: <font color="red">Test Slower Than Expected Performance Range</font></H2>')
        else:
            large_test_file.write('<H2>GIS 2KM Test: <font color="#4CC417">Test Faster Than Expected Performance Range</font></H2>')

# put something here to flag BFB results between data and bench and pgi and gnu etc.
        flag_to_plot_gis2km = 1
        if flag_to_plot_gis2km:

            large_test_file.write('<TH ALIGN=LEFT><A HREF="gis2km_case.html">Case and Parameter Settings Details</A>\n')
            large_test_file.write('<BR>\n')
            xml_path = perf_test + '/gis_2km/trilinosOptions.xml'
            bench_xml_path = perf_test + '/bench/gis_2km/trilinosOptions.xml'
            if os.path.isdir(perf_test + '/gis_2km/configure_files/') == True: 
                configure_path = perf_test + '/gis_2km/configure_files/gis.2km.config'
                bench_configure_path = perf_test + '/bench/gis_2km/configure_files/gis.2km.config'
            else:
                configure_path = perf_test + '/gis_2km/gis.2km.config'
                bench_configure_path = perf_test + '/bench/gis_2km/gis.2km.config'
            c_flag = 0
            VV_utilities.confxml(gis2km_case,configure_path,bench_configure_path,xml_path,bench_xml_path,c_flag)

            large_test_file.write('<TH ALIGN=LEFT><A HREF="gis2km_timing.html">Timing Details</A>\n')
            large_test_file.write('<BR>\n')
            flag = 0
            timing_path_10runs = perf_test + '/bench/gis_2km/data_titan/out.gis.2km.albany.timing'
            current_run_path = perf_test + '/gis_2km/data/out.gis.2km.albany.timing'
            VV_timing.timing_table_current_run(gis2km_time,timing_path_10runs,current_run_path,flag)
            
            #large_test_file.write('<TH ALIGN=LEFT><A HREF="gis2km_plot.html">Plots</A>\n')
            #large_test_file.write('<BR>\n')
            #if failedt != 0:
            #    gis2_plot.write("<H2>GIS 2km Test failed, plots may not be generated</H2><br>")
            #checkpath = perf_test + '/gis_2km/data/gis_2km.ice2sea.init.nc'
            #noplot = VV_checks.emptycheck(checkpath)
            #if noplot != 1:
            #    VV_gis2details.gis2_plot(gis2km_plot,perf_test,ncl_path,html_path,script_path,data_dir)

# Time stamping
        mode = os.stat(perf_test + '/gis_2km').st_mtime
        mode = mode - 14400
        mode = time.gmtime(mode)
        ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
        strrand = '<b>Time of Last Simulation: ' + ctime + '</b>\n'
        large_test_file.write(strrand)
        large_test_file.write('<BR>\n')

    else:
        print "NOT RUNNING GIS 2KM TESTCASE"


#apply flag to turn off running test
    if gis_1km_flag == 1:

# GIS 1km stats
        print "running gis1km testcase"
        large_test_file.write('<BR>\n')
        if dictionary_large_gis['gis1km'] == 0:
            large_test_file.write('<H2>GIS 1KM Test: <font color="blue">Test Within Expected Performance Range</font></H2>')
        elif dictionary_large_gis['gis1km'] == 1:
            large_test_file.write('<H2>GIS 1KM Test: <font color="red">Test Slower Than Expected Performance Range</font></H2>')
        else:
            large_test_file.write('<H2>GIS 1KM Test: <font color="#4CC417">Test Faster Than Expected Performance Range</font></H2>')

# put something here to flag BFB results between data and bench and pgi and gnu etc.
        flag_to_plot_gis1km = 1
        if flag_to_plot_gis1km:

            large_test_file.write('<TH ALIGN=LEFT><A HREF="gis1km_case.html">Case and Parameter Settings Details</A>\n')
            large_test_file.write('<BR>\n')
            xml_path = perf_test + '/gis_1km/trilinosOptions.xml'
            bench_xml_path = perf_test + '/bench/gis_1km/trilinosOptions.xml'
            if os.path.isdir(perf_test + '/gis_1km/configure_files/') == True: 
                configure_path = perf_test + '/gis_1km/configure_files/gis.1km.config'
                bench_configure_path = perf_test + '/bench/gis_1km/configure_files/gis.1km.glissade_0timesteps.config'
            else:
                configure_path = perf_test + '/gis_1km/gis.1km.config'
                bench_configure_path = perf_test + '/bench/gis_1km/gis.1km.glissade_0timesteps.config'
            c_flag = 0
            VV_utilities.confxml(gis1km_case,configure_path,bench_configure_path,xml_path,bench_xml_path,c_flag)

            large_test_file.write('<TH ALIGN=LEFT><A HREF="gis1km_timing.html">Timing Details</A>\n')
            large_test_file.write('<BR>\n')
            flag = 0
            timing_path_10runs = perf_test + '/bench/gis_1km/data_titan/out.gis.1km.albany.timing'
            current_run_path = perf_test + '/gis_1km/data/out.gis.1km.albany.timing'
            VV_timing.timing_table_current_run(gis1km_time,timing_path_10runs,current_run_path,flag)
            
            #large_test_file.write('<TH ALIGN=LEFT><A HREF="gis1km_plot.html">Plots</A>\n')
            #large_test_file.write('<BR>\n')
            #if failedt != 0:
            #    gis1_plot.write("<H2>GIS 1km Test failed, plots may not be generated</H2><br>")
            #checkpath = perf_test + '/gis_1km/data/gis_1km.ice2sea.init.nc'
            #noplot = VV_checks.emptycheck(checkpath)
            #if noplot != 1:
            #    VV_gis1details.gis1_plot(gis1km_plot,perf_test,ncl_path,html_path,script_path,data_dir)

# Time stamping
        mode = os.stat(perf_test + '/gis_1km').st_mtime
        mode = mode - 14400
        mode = time.gmtime(mode)
        ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
        strrand = '<b>Time of Last Simulation: ' + ctime + '</b>\n'
        large_test_file.write(strrand)
        large_test_file.write('<BR>\n')

    else:
        print "NOT RUNNING GIS 1KM TESTCASE"


    large_test_file.write('<BR>\n')
    large_test_file.write('<BR>\n')
    large_test_file.write('<TH ALIGN=LEFT><A HREF="livv_kit_main.html">Home</A>\n')
    large_test_file.write('</HTML>\n')
    large_test_file.close()

    descript_file.write('<HTML>\n')
    descript_file.write('<TITLE>Descriptions about the Test Suite</TITLE>\n')
    descript_file.write('<BODY BGCOLOR="#CADFE0">\n') 
    descript_file.write('<H2>Test Suite Details</H2>')
    descript_file.write('<BR>\n')
    descript_file.write('The Diagnostic Dome 500 test case \n')
    descript_file.write('<BR>\n')
    descript_file.write('  Attributes: 3-D paraboloid dome of ice with a circular, 60 km diameter base sitting on a flat bed. The horizontal spatial resolution studies are 2 km, 1 km, 0.5 km and 0.25 km, and there are 10 vertical levels. For this set of experiments a quasi no-slip basal condition in imposed by setting. A zero-flux boundary condition is applied to the dome margins. \n')
    descript_file.write('<BR>\n')
    descript_file.write('  What does it test? \n')
    descript_file.write('<BR><BR>\n')
    descript_file.write('<BR>\n')
    descript_file.write('GIS 4KM, 2KM, 1KM Test Case \n')
    descript_file.write('<BR>\n')
    descript_file.write('  Attributes: 3-D paraboloid dome of ice with a circular, 60 km diameter base sitting on a flat bed. The horizontal spatial resolution studies are 2 km, 1 km, 0.5 km and 0.25 km, and there are 10 vertical levels. For this set of experiments a quasi no-slip basal condition in imposed by setting. A zero-flux boundary condition is applied to the dome margins. \n')
    descript_file.write('<BR>\n')
    descript_file.write('  What does it test? \n')
    descript_file.write('<BR><BR>\n')
    descript_file.write('</HTML>\n')
    descript_file.close()

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
import VV_checks
from stat import *
import time

#bit-for-bit check for each test case
def bit_list(reg_test,data_dir,diagnostic_flag,evolving_flag,circular_flag,confined_flag,\
                ismip_hom_a80_flag,ismip_hom_a20_flag,ismip_hom_c80_flag,ismip_hom_c20_flag):
    dictionary = {}
#diagnostic dome30 case
    #apply flag to turn off running test
    if diagnostic_flag == 1:
        data_file_path = reg_test + '/dome30/diagnostic/' + data_dir
        bench_file_path = reg_test + '/bench/dome30/diagnostic/' + data_dir
        dictionary['diagnostic'] = VV_checks.bit4bit(data_file_path,bench_file_path)
    else:
        dictionary['diagnostic'] = 0
#evolving dome30 case
    #apply flag to turn off running test
    if evolving_flag == 1:
        data_file_path = reg_test + '/dome30/evolving/' + data_dir
        bench_file_path = reg_test + '/bench/dome30/evolving/' + data_dir
        dictionary['evolving'] = VV_checks.bit4bit(data_file_path,bench_file_path)
    else:
        dictionary['evolving'] = 0
#circular shelf case
    #apply flag to turn off running test
    if circular_flag == 1:
        data_file_path = reg_test + '/circular-shelf/' + data_dir
        bench_file_path = reg_test + '/bench/circular-shelf/' + data_dir
        dictionary['circular'] = VV_checks.bit4bit(data_file_path,bench_file_path)
    else:
        dictionary['circular'] = 0
#confined shelf case
    #apply flag to turn off running test
    if confined_flag == 1:
        data_file_path = reg_test + '/confined-shelf/' + data_dir
        bench_file_path = reg_test + '/bench/confined-shelf/' + data_dir
        dictionary['confined'] = VV_checks.bit4bit(data_file_path,bench_file_path)
    else:
        dictionary['confined'] = 0
#ismip hom a 80 case
    #apply flag to turn off running test
    if ismip_hom_a80_flag == 1:
        data_file_path = reg_test + '/ismip-hom-a/80km/' + data_dir
        bench_file_path = reg_test + '/bench/ismip-hom-a/80km/' + data_dir
        dictionary['ismip-hom-a80'] = VV_checks.bit4bit(data_file_path,bench_file_path)
    else:
        dictionary['ismip-hom-a80'] = 0
#ismip hom a 20 case
    #apply flag to turn off running test
    if ismip_hom_a20_flag == 1:
        data_file_path = reg_test + '/ismip-hom-a/20km/' + data_dir
        bench_file_path = reg_test + '/bench/ismip-hom-a/20km/' + data_dir
        dictionary['ismip-hom-a20'] = VV_checks.bit4bit(data_file_path,bench_file_path)
    else:
        dictionary['ismip-hom-a20'] = 0
#ismip hom c 80 case
    #apply flag to turn off running test
    if ismip_hom_c80_flag == 1:
        data_file_path = reg_test + '/ismip-hom-c/80km/' + data_dir
        bench_file_path = reg_test + '/bench/ismip-hom-c/80km/' + data_dir
        dictionary['ismip-hom-c80'] = VV_checks.bit4bit(data_file_path,bench_file_path)
    else:
        dictionary['ismip-hom-c80'] = 0
#ismip hom c 20 case
    #apply flag to turn off running test
    if ismip_hom_c20_flag == 1:
        data_file_path = reg_test + '/ismip-hom-c/20km/' + data_dir
        bench_file_path = reg_test + '/bench/ismip-hom-c/20km/' + data_dir
        dictionary['ismip-hom-c20'] = VV_checks.bit4bit(data_file_path,bench_file_path)
    else:
        dictionary['ismip-hom-c20'] = 0

    return dictionary


def web(glide_flag,descript_file,test_file, \
    dome30d_file,dome30d_case,dome30d_plot,dome30e_file,dome30e_case,dome30e_plot, \
    circ_file,circ_case,circ_plot,conf_file,conf_case,conf_plot, \
    ishoma80_file,ishoma80_case,ishoma80_plot,ishoma20_file,ishoma20_case,ishoma20_plot, \
    ishomc80_file,ishomc80_case,ishomc80_plot,ishomc20_file,ishomc20_case,ishomc20_plot, \
    reg_test,test_suite,data_dir,ncl_path,html_path,script_path,\
    diagnostic_flag,evolving_flag,circular_flag,confined_flag, \
    ismip_hom_a80_flag,ismip_hom_a20_flag,ismip_hom_c80_flag,ismip_hom_c20_flag):

# using data, fill the web page with info about the cases
    test_file.write('<HTML>\n')
    test_file.write('<TITLE>Test Suite Diagnostics</TITLE>\n')
    test_file.write('<BODY BGCOLOR="#CADFE0">\n')
    test_file.write('<H1>Test Suite Diagnostics</H1>')

# link to descript_file about the test cases
    test_file.write('<TH ALIGN=LEFT><A HREF="test_descript.html">Test Suite Descriptions</A>\n')
    test_file.write('<BR>\n')

    dictionary = bit_list(reg_test,data_dir,diagnostic_flag,evolving_flag,circular_flag,confined_flag,\
                    ismip_hom_a80_flag,ismip_hom_a20_flag,ismip_hom_c80_flag,ismip_hom_c20_flag)

#apply flag to turn off running test
    if diagnostic_flag == 1:

# Diagnostic Dome 30 stats
        if glide_flag == 1:
            print "running diagnostic dome30 glide testcase"
        else:
            print "running diagnostic dome30 glissade testcase"
        test_file.write('<BR>\n')
        if dictionary['diagnostic'] == 0:
            test_file.write('<H2>Diagnostic Dome 30 Test: <font color="green">Bit-for-Bit</font></H2>')
        else:
            test_file.write('<H2>Diagnostic Dome 30 Test: <font color="red">NOT Bit-for-Bit</font></H2>')

#put something here to flag BFB results and no need to do any more calculations
        flag_to_plot_dome30d = 1
        if flag_to_plot_dome30d:

# link to dome30d_file with descriptions about the test cases
            #since glissade does not output solver information:
            if glide_flag == 1:
                test_file.write('<TH ALIGN=LEFT><A HREF="dome30d_details.html">Velocity Solver Details</A>\n')
                test_file.write('<BR>\n')
                failedt = VV_dome30details.ddetails(dome30d_file,reg_test,data_dir)

            if glide_flag == 1:
                test_file.write('<TH ALIGN=LEFT><A HREF="dome30d_case.html">Case and Parameter Settings Details</A>\n')
            else:
                test_file.write('<TH ALIGN=LEFT><A HREF="dome30d_case_glissade.html">Case and Parameter Settings Details</A>\n')
            test_file.write('<BR>\n')
            xml_path = reg_test + '/dome30/diagnostic/trilinosOptions.xml'
            bench_xml_path = reg_test + '/bench/dome30/diagnostic/trilinosOptions.xml'
            if glide_flag == 1:
                c_flag = 1
                if os.path.isdir(reg_test + '/dome30/diagnostic/configure_files/') == True:
                    configure_path = reg_test + '/dome30/diagnostic/configure_files/dome.30.JFNK.trilinos.config.1'
                    bench_configure_path = reg_test + '/bench/dome30/diagnostic/configure_files/dome.30.JFNK.trilinos.config.1'
                else:
                    configure_path = reg_test + '/dome30/diagnostic/dome.30.JFNK.trilinos.config.1'
                    bench_configure_path = reg_test + '/bench/dome30/diagnostic/dome.30.JFNK.trilinos.config.1'
            else:
                c_flag = 0
                if os.path.isdir(reg_test + '/dome30/diagnostic/configure_files/') == True:
                    configure_path = reg_test + '/dome30/diagnostic/configure_files/dome.30.glissade.config.1'
                    bench_configure_path = reg_test + '/bench/dome30/diagnostic/configure_files/dome.30.glissade.config.1'
                else:
                    configure_path = reg_test + '/dome30/diagnostic/dome.30.glissade.config.1'
                    bench_configure_path = reg_test + '/bench/dome30/diagnostic/dome.30.glissade.config.1'
            VV_utilities.confxml(dome30d_case,configure_path,bench_configure_path,xml_path,bench_xml_path,c_flag)

            if glide_flag == 1:
                test_file.write('<TH ALIGN=LEFT><A HREF="dome30d_plot.html">Plots</A>\n')
            else:
                test_file.write('<TH ALIGN=LEFT><A HREF="dome30d_plot_glissade.html">Plots</A>\n')
            test_file.write('<BR>\n')
            #if failedt != 0:
            #    dome30d_plot.write("<H2>Diagnostic Dome 30 Test failed, plots may not be generated</H2><br>")
            checkpath = reg_test + '/dome30/diagnostic/' + data_dir + '/dome.1.nc'
            checkpath2 = reg_test + '/dome30/diagnostic/' + data_dir + '/dome.4.nc'
            noplot = VV_checks.emptycheck(checkpath)
            noplot1 = noplot
            noplot = VV_checks.emptycheck(checkpath2)
            if noplot1 != 1 and noplot != 1:
                VV_dome30details.dplot(glide_flag,dome30d_plot,reg_test,ncl_path,html_path,script_path,data_dir)

# Time stamping
        strrand = ''
        mode = os.stat(reg_test + '/dome30/diagnostic').st_mtime
        mode = mode - 18000
        mode = time.gmtime(mode)
        ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
        strrand = '<b>Time of Last Simulation: ' + str(ctime) + '</b>'
        test_file.write(strrand)
        test_file.write('<BR>\n')

    else:
        print "NOT RUNNING DIAGNOSTIC DOME30 TESTCASE"


#apply flag to turn off running test
    if evolving_flag == 1:

# Evolving Dome 30 stats
        if glide_flag == 1:
            print "running evolving dome30 glide testcase"
        else:
            print "running evolving dome30 glissade testcase"
        test_file.write('<BR>\n')
        if dictionary['evolving'] == 0:
            test_file.write('<H2>Evolving Dome 30 Test: <font color="green">Bit-for-Bit</font></H2>')
        else:
            test_file.write('<H2>Evolving Dome 30 Test: <font color="red">NOT Bit-for-Bit</font></H2>')

# put something here to flag BFB results and no need to do any more calculations
        flag_to_plot_dome30e = 1 
        if flag_to_plot_dome30e:

# link to dome30e_file with descriptions about the test cases
            # since glissade does not output solver information:
            if glide_flag == 1:
                test_file.write('<TH ALIGN=LEFT><A HREF="dome30e_details.html">Velocity Solver Details</A>\n')
                test_file.write('<BR>\n')
                failedt = VV_dome30details.edetails(dome30e_file,test_suite,reg_test,ncl_path,html_path,data_dir)

            if glide_flag == 1:
                test_file.write('<TH ALIGN=LEFT><A HREF="dome30e_case.html">Case and Parameter Settings Details</A>\n')
            else:
                test_file.write('<TH ALIGN=LEFT><A HREF="dome30e_case_glissade.html">Case and Parameter Settings Details</A>\n')
            test_file.write('<BR>\n')
            xml_path = reg_test + '/dome30/evolving/trilinosOptions.xml'
            bench_xml_path = reg_test + '/bench/dome30/evolving/trilinosOptions.xml'
            if glide_flag == 1:
                c_flag = 1
                if os.path.isdir(reg_test + '/dome30/evolving/configure_files/') == True:
                    configure_path = reg_test + '/dome30/evolving/configure_files/dome.30.JFNK.trilinos.config.15'
                    bench_configure_path = reg_test + '/bench/dome30/evolving/configure_files/dome.30.JFNK.trilinos.config.15'
                else:
                    configure_path = reg_test + '/dome30/evolving/dome.30.JFNK.trilinos.config.15'
                    bench_configure_path = reg_test + '/bench/dome30/evolving/dome.30.JFNK.trilinos.config.15'
            else:
                c_flag = 0
                if os.path.isdir(reg_test + '/dome30/evolving/configure_files/') == True:
                    configure_path = reg_test + '/dome30/evolving/configure_files/dome.30.glissade.config.15'
                    bench_configure_path = reg_test + '/bench/dome30/evolving/configure_files/dome.30.glissade.config.15'
                else:
                    configure_path = reg_test + '/dome30/evolving/dome.30.glissade.config.15'
                    bench_configure_path = reg_test + '/bench/dome30/evolving/dome.30.glissade.config.15'
            VV_utilities.confxml(dome30e_case,configure_path,bench_configure_path,xml_path,bench_xml_path,c_flag)

            if glide_flag == 1:
                test_file.write('<TH ALIGN=LEFT><A HREF="dome30e_plot.html">Plots</A>\n')
            else:
                test_file.write('<TH ALIGN=LEFT><A HREF="dome30e_plot_glissade.html">Plots</A>\n')
            test_file.write('<BR>\n')
            #if failedt != 0:
            #    dome30e_plot.write("<H2>Evolving Dome 30 Test failed, plots may not be generated</H2><br>")
            checkpath = reg_test + '/dome30/evolving/' + data_dir + '/dome.9.nc'
            checkpath2 = reg_test + '/dome30/evolving/' + data_dir + '/dome.15.nc'
            noplot = VV_checks.emptycheck(checkpath)
            noplot1 = noplot
            noplot = VV_checks.emptycheck(checkpath2)
            if noplot != 1 and noplot != 1:
                VV_dome30details.eplot(glide_flag,dome30e_plot,reg_test,ncl_path,html_path,script_path,data_dir)

# Time stamping
        mode = os.stat(reg_test + '/dome30/evolving').st_mtime
        mode = mode - 18000
        mode = time.gmtime(mode)
        ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
        strrand = '<b>Time of Last Simulation: ' + ctime + '</b>'
        test_file.write(strrand)
        test_file.write('<BR>\n')

    else:
        print "NOT RUNNING EVOLVING DOME30 TESTCASE"


#apply flag to turn off running test
    if circular_flag == 1:

# Circular Shelf stats
        if glide_flag == 1:
            print "running circular shelf glide testcase"
        else:
            print "running circular shelf glissade testcase"
        test_file.write('<BR>\n')
        if dictionary['circular'] == 0:
            test_file.write('<H2>Circular Shelf Test: <font color="green">Bit-for-Bit</font></H2>')
        else:
            test_file.write('<H2>Circular Shelf Test: <font color="red">NOT Bit-for-Bit</font></H2>')

# put something here to flag BFB results and no need to do any more calculations
        flag_to_plot_circ = 1
        if flag_to_plot_circ:

# link to circ_file with descriptions about the test cases
            # since glissade does not output solver information:
            if glide_flag == 1:
                test_file.write('<TH ALIGN=LEFT><A HREF="circ_details.html">Velocity Solver Details</A>\n')
                test_file.write('<BR>\n')
                failedt = VV_shelfdetails.circdetails(circ_file,reg_test,data_dir)

            if glide_flag ==1:
                test_file.write('<TH ALIGN=LEFT><A HREF="circ_case.html">Case and Parameter Settings Details</A>\n')
            else:
                test_file.write('<TH ALIGN=LEFT><A HREF="circ_case_glissade.html">Case and Parameter Settings Details</A>\n')
            test_file.write('<BR>\n')
            xml_path = reg_test + '/circular-shelf/trilinosOptions.xml'
            bench_xml_path = reg_test + '/bench/circular-shelf/trilinosOptions.xml'
            if glide_flag == 1:
                c_flag = 1
                if os.path.isdir(reg_test + '/circular-shelf/configure_files/') == True:
                    configure_path = reg_test + '/circular-shelf/configure_files/circular-shelf.JFNK.config'
                    bench_configure_path = reg_test + '/bench/circular-shelf/configure_files/circular-shelf.JFNK.config'
                else:
                    configure_path = reg_test + '/circular-shelf/circular-shelf.JFNK.config'
                    bench_configure_path = reg_test + '/bench/circular-shelf/circular-shelf.JFNK.config'
            else:
                c_flag = 0
                if os.path.isdir(reg_test + '/circular-shelf/configure_files/') == True:
                    configure_path = reg_test + '/circular-shelf/configure_files/circular-shelf.glissade.config'
                    bench_configure_path = reg_test + '/bench/circular-shelf/configure_files/circular-shelf.glissade.config'
                else:
                    configure_path = reg_test + '/circular-shelf/circular-shelf.glissade.config'
                    bench_configure_path = reg_test + '/bench/circular-shelf/circular-shelf.glissade.config'
            VV_utilities.confxml(circ_case,configure_path,bench_configure_path,xml_path,bench_xml_path,c_flag)

            if glide_flag == 1:
                test_file.write('<TH ALIGN=LEFT><A HREF="circ_plot.html">Plots</A>\n')
            else:
                test_file.write('<TH ALIGN=LEFT><A HREF="circ_plot_glissade.html">Plots</A>\n')
            test_file.write('<BR>\n')
            #if failedt != 0:
            #    circ_plot.write("<H2>Circular Shelf Test failed, plots may not be generated</H2><br>")
            checkpath = reg_test + '/circular-shelf/' + data_dir + '/circular-shelf.gnu.JFNK.nc'
            noplot = VV_checks.emptycheck(checkpath)
            if noplot != 1:
                VV_shelfdetails.circplot(glide_flag,circ_plot,reg_test,ncl_path,html_path,script_path,data_dir)

# Time stamping
        mode = os.stat(reg_test + '/circular-shelf').st_mtime
        mode = mode - 18000
        mode = time.gmtime(mode)
        ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
        strrand = '<b>Time of Last Simulation: ' + ctime + '</b>'
        test_file.write(strrand)
        test_file.write('<BR>\n')

    else:
        print "NOT RUNNING CIRCULAR SHELF TESTCASE"


#apply flag to turn off running test
    if confined_flag == 1:

# Confined Shelf stats
        if glide_flag == 1:
            print "running confined shelf glide testcase"
        else:
            print "running confined shelf glissade testcase"
        test_file.write('<BR>\n')
        if dictionary['confined'] == 0:
            test_file.write('<H2>Confined Shelf Test: <font color="green">Bit-for-Bit</font></H2>')
        else:
            test_file.write('<H2>Confined Shelf Test: <font color="red">NOT Bit-for-Bit</font></H2>')

# put something here to flag BFB results and no need to do any more calculations
        flag_to_plot_conf = 1
        if flag_to_plot_conf:

# link to conf_file with descriptions about the test cases          
            # since glissade does not output solver information:
            if glide_flag == 1:
                test_file.write('<TH ALIGN=LEFT><A HREF="conf_details.html">Velocity Solver Details</A>\n')
                test_file.write('<BR>\n')
                failedt = VV_shelfdetails.confdetails(conf_file,reg_test,data_dir)

            if glide_flag == 1:
                test_file.write('<TH ALIGN=LEFT><A HREF="conf_case.html">Case and Parameter Settings Details</A>\n')
            else:
                test_file.write('<TH ALIGN=LEFT><A HREF="conf_case_glissade.html">Case and Parameter Settings Details</A>\n')
            test_file.write('<BR>\n')
            xml_path = reg_test + '/confined-shelf/trilinosOptions.xml'
            bench_xml_path = reg_test + '/bench/confined-shelf/trilinosOptions.xml'
            if glide_flag == 1:
                c_flag = 1
                if os.path.isdir(reg_test + '/confined-shelf/configure_files/') == True:
                    configure_path = reg_test + '/confined-shelf/configure_files/confined-shelf.JFNK.config'
                    bench_configure_path = reg_test + '/bench/confined-shelf/configure_files/confined-shelf.JFNK.config'
                else:
                    configure_path = reg_test + '/confined-shelf/confined-shelf.JFNK.config'
                    bench_configure_path = reg_test + '/bench/confined-shelf/confined-shelf.JFNK.config'
            else:
                c_flag = 0
                if os.path.isdir(reg_test + '/confined-shelf/configure_files/') == True:
                    configure_path = reg_test + '/confined-shelf/configure_files/confined-shelf.glissade.config'
                    bench_configure_path = reg_test + '/bench/confined-shelf/configure_files/confined-shelf.glissade.config'
                else:
                    configure_path = reg_test + '/confined-shelf/confined-shelf.glissade.config'
                    bench_configure_path = reg_test + '/bench/confined-shelf/confined-shelf.glissade.config'
            VV_utilities.confxml(conf_case,configure_path,bench_configure_path,xml_path,bench_xml_path,c_flag)

            if glide_flag == 1:
                test_file.write('<TH ALIGN=LEFT><A HREF="conf_plot.html">Plots</A>\n')
            else:
                test_file.write('<TH ALIGN=LEFT><A HREF="conf_plot_glissade.html">Plots</A>\n')
            test_file.write('<BR>\n')
            #if failedt != 0:
            #    conf_plot.write("<H2>Confined Shelf Test failed, plots may not be generated</H2><br>")
            checkpath = reg_test + '/confined-shelf/' + data_dir + '/confined-shelf.gnu.JFNK.nc'
            noplot = VV_checks.emptycheck(checkpath)
            if noplot != 1:
                VV_shelfdetails.confplot(glide_flag,conf_plot,reg_test,ncl_path,html_path,script_path,data_dir)

# Time stamping
        mode = os.stat(reg_test + '/confined-shelf').st_mtime
        mode = mode - 18000
        mode = time.gmtime(mode)
        ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
        strrand = '<b>Time of Last Simulation: ' + ctime + '</b>'
        test_file.write(strrand)
        test_file.write('<BR>\n')

    else:
        print "NOT RUNNING CONFINED SHELF TESTCASE"


#apply flag to turn off running test
    if ismip_hom_a80_flag == 1:

# ISMIP HOM A 80km stats
        if glide_flag == 1:
            print "running ismip hom a 80km glide testcase"
        else:
            print "running ismip hom a 80km glissade testcase"
        test_file.write('<BR>\n')
        if dictionary['ismip-hom-a80'] == 0:
            test_file.write('<H2>ISMIP HOM A 80KM Test: <font color="green">Bit-for-Bit</font></H2>')
        else:
            test_file.write('<H2>ISMIP HOM A 80KM Test: <font color="red">NOT Bit-for-Bit</font></H2>')

# put something here to flag BFB results and no need to do any more calculations
        flag_to_plot_iha80 = 1
        if flag_to_plot_iha80:

# link to ismip_hom_a80_file with descriptions about the test cases 
            # since glissade does not output solver information:
            if glide_flag == 1:
                test_file.write('<TH ALIGN=LEFT><A HREF="ishoma80_details.html">Velocity Solver Details</A>\n')
                test_file.write('<BR>\n')
                failedt = VV_ismip.a80details(ishoma80_file,reg_test,data_dir)
            
            if glide_flag == 1:
                test_file.write('<TH ALIGN=LEFT><A HREF="ishoma80_case.html">Case and Parameter Settings Details</A>\n')
            else:
                test_file.write('<TH ALIGN=LEFT><A HREF="ishoma80_case_glissade.html">Case and Parameter Settings Details</A>\n')
            test_file.write('<BR>\n')
            xml_path = reg_test + '/ismip-hom-a/80km/trilinosOptions.xml'
            bench_xml_path = reg_test + '/bench/ismip-hom-a/80km/trilinosOptions.xml'
            if glide_flag == 1:
                c_flag = 1
                if os.path.isdir(reg_test + '/ismip-hom-a/80km/configure_files/') == True:
                    configure_path = reg_test + '/ismip-hom-a/80km/configure_files/ishom.a.80km.JFNK.trilinos.config'
                    bench_configure_path = reg_test + '/bench/ismip-hom-a/80km/configure_files/ishom.a.80km.JFNK.trilinos.config'
                else:
                    configure_path = reg_test + '/ismip-hom-a/80km/ishom.a.80km.JFNK.trilinos.config'
                    bench_configure_path = reg_test + '/bench/ismip-hom-a/80km/ishom.a.80km.JFNK.trilinos.config'
            else:
                c_flag = 0
                if os.path.isdir(reg_test + '/ismip-hom-a/80km/configure_files/') == True:
                    configure_path = reg_test + '/ismip-hom-a/80km/configure_files/ishom.a.80km.glissade.1.config'
                    bench_configure_path = reg_test + '/bench/ismip-hom-a/80km/configure_files/ishom.a.80km.glissade.1.config'
                else:
                    configure_path = reg_test + '/ismip-hom-a/80km/ishom.a.80km.glissade.1.config'
                    bench_configure_path = reg_test + '/bench/ismip-hom-a/80km/ishom.a.80km.glissade.1.config'
            VV_utilities.confxml(ishoma80_case,configure_path,bench_configure_path,xml_path,bench_xml_path,c_flag)

            if glide_flag == 1:
                test_file.write('<TH ALIGN=LEFT><A HREF="ishoma80_plot.html">Plots</A>\n')
            else:
                test_file.write('<TH ALIGN=LEFT><A HREF="ishoma80_plot_glissade.html">Plots</A>\n')
            test_file.write('<BR>\n')
            #if failedt != 0:
            #    ishoma80_plot.write("<H2>ISMIP HOM A 80km Test failed, plots may not be generated</H2><br>")
            checkpath = reg_test + '/ismip-hom-a/80km/' + data_dir + '/ishom.a.80km.JFNK.out.nc'
            noplot = VV_checks.emptycheck(checkpath)
            if noplot != 1:
                VV_ismip.a80plot(glide_flag,ishoma80_plot,reg_test,ncl_path,html_path,script_path,data_dir)

# Time stamping
        mode = os.stat(reg_test + '/ismip-hom-a/80km').st_mtime
        mode = mode - 18000
        mode = time.gmtime(mode)
        ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
        strrand = '<b>Time of Last Simulation: ' + ctime + '</b>'
        test_file.write(strrand)
        test_file.write('<BR>\n')

    else:
        print "NOT RUNNING ISMIP HOM A 80KM TESTCASE"


#apply flag to turn off running test
    if ismip_hom_a20_flag == 1:

# ISMIP HOM A 20km stats
        if glide_flag == 1:
            print "running ismip hom a 20km glide testcase"
        else:
            print "running ismip hom a 20km glissade testcase"
        test_file.write('<BR>\n')
        if dictionary['ismip-hom-a20'] == 0:
            test_file.write('<H2>ISMIP HOM A 20KM Test: <font color="green">Bit-for-Bit</font></H2>')
        else:
            test_file.write('<H2>ISMIP HOM A 20KM Test: <font color="red">NOT Bit-for-Bit</font></H2>')

# put something here to flag BFB results and no need to do any more calculations
        flag_to_plot_iha20 = 1
        if flag_to_plot_iha20:

# link to ismip_hom_a20_file with descriptions about the test cases 
            # since glissade does not output solver information:
            if glide_flag == 1:
                test_file.write('<TH ALIGN=LEFT><A HREF="ishoma20_details.html">Velocity Solver Details</A>\n')
                test_file.write('<BR>\n')
                failedt = VV_ismip.a20details(ishoma20_file,reg_test,data_dir)

            if glide_flag == 1:
                test_file.write('<TH ALIGN=LEFT><A HREF="ishoma20_case.html">Case and Parameter Settings Details</A>\n')
            else:
                test_file.write('<TH ALIGN=LEFT><A HREF="ishoma20_case_glissade.html">Case and Parameter Settings Details</A>\n')
            test_file.write('<BR>\n')
            xml_path = reg_test + '/ismip-hom-a/20km/trilinosOptions.xml'
            bench_xml_path = reg_test + '/bench/ismip-hom-a/20km/trilinosOptions.xml'
            if glide_flag == 1:
                c_flag = 1
                if os.path.isdir(reg_test + '/ismip-hom-a/20km/configure_files/') == True:
                    configure_path = reg_test + '/ismip-hom-a/20km/configure_files/ishom.a.20km.JFNK.trilinos.config'
                    bench_configure_path = reg_test + '/bench/ismip-hom-a/20km/configure_files/ishom.a.20km.JFNK.trilinos.config'
                else:
                    configure_path = reg_test + '/ismip-hom-a/20km/ishom.a.20km.JFNK.trilinos.config'
                    bench_configure_path = reg_test + '/bench/ismip-hom-a/20km/ishom.a.20km.JFNK.trilinos.config'
            else:
                c_flag = 0
                if os.path.isdir(reg_test + '/ismip-hom-a/20km/configure_files/') == True:
                    configure_path = reg_test + '/ismip-hom-a/20km/configure_files/ishom.a.20km.glissade.1.config'
                    bench_configure_path = reg_test + '/bench/ismip-hom-a/20km/configure_files/ishom.a.20km.glissade.1.config'
                else:
                    configure_path = reg_test + '/ismip-hom-a/20km/ishom.a.20km.glissade.1.config'
                    bench_configure_path = reg_test + '/bench/ismip-hom-a/20km/ishom.a.20km.glissade.1.config'
            VV_utilities.confxml(ishoma20_case,configure_path,bench_configure_path,xml_path,bench_xml_path,c_flag)

            if glide_flag == 1:
                test_file.write('<TH ALIGN=LEFT><A HREF="ishoma20_plot.html">Plots</A>\n')
            else:
                test_file.write('<TH ALIGN=LEFT><A HREF="ishoma20_plot_glissade.html">Plots</A>\n')
            test_file.write('<BR>\n')
            #if failedt != 0:
            #    ishoma20_plot.write("<H2>ISMIP HOM A 20 Test failed, plots may not be generated</H2><br>")
            checkpath = reg_test + '/ismip-hom-a/20km/' + data_dir + '/ishom.a.20km.JFNK.out.nc'
            noplot = VV_checks.emptycheck(checkpath)
            if noplot != 1:
                VV_ismip.a20plot(glide_flag,ishoma20_plot,reg_test,ncl_path,html_path,script_path,data_dir)

# Time stamping
        mode = os.stat(reg_test + '/ismip-hom-a/20km').st_mtime
        mode = mode - 18000
        mode = time.gmtime(mode)
        ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
        strrand = '<b>Time of Last Simulation: ' + ctime + '</b>'
        test_file.write(strrand)
        test_file.write('<BR>\n')

    else:
        print "NOT RUNNING ISMIP HOM A 20KM TESTCASE"


#apply flag to turn off running test
    if ismip_hom_c80_flag == 1:
        if glide_flag == 0:
# ISMIP HOM C 80km stats
            print "running ismip hom c 80km glissade testcase"
            test_file.write('<BR>\n')
            if dictionary['ismip-hom-c80'] == 0:
                test_file.write('<H2>ISMIP HOM C 80KM Test: <font color="green">Bit-for-Bit</font></H2>')
            else:
                test_file.write('<H2>ISMIP HOM C 80KM Test: <font color="red">NOT Bit-for-Bit</font></H2>')

# put something here to flag BFB results and no need to do any more calculations
            flag_to_plot_ihc = 1
            if flag_to_plot_ihc:

# link to ismip_hom_c80_file with descriptions about the test cases       
                if glide_flag == 1:
                    test_file.write('<TH ALIGN=LEFT><A HREF="ishomc80_details.html">Velocity Solver Details</A>\n')
                    test_file.write('<BR>\n')
                    failedt = VV_ismip.c80details(ishomc80_file,reg_test,data_dir)

                if glide_flag == 1:
                    test_file.write('<TH ALIGN=LEFT><A HREF="ishomc80_case.html">Case and Parameter Settings Details</A>\n')
                else:
                    test_file.write('<TH ALIGN=LEFT><A HREF="ishomc80_case_glissade.html">Case and Parameter Settings Details</A>\n')
                test_file.write('<BR>\n')
                xml_path = reg_test + '/ismip-hom-c/80km/trilinosOptions.xml'
                bench_xml_path = reg_test + '/bench/ismip-hom-c/80km/trilinosOptions.xml'
                if glide_flag == 1:
                    c_flag = 1
                    if os.path.isdir(reg_test + '/ismip-hom-c/80km/configure_files/') == True:
                        configure_path = reg_test + '/ismip-hom-c/80km/configure_files/ishom.c.80km.JFNK.trilinos.config'
                        bench_configure_path = reg_test + '/bench/ismip-hom-c/80km/configure_files/ishom.c.80km.JFNK.trilinos.config'
                    else:
                        configure_path = reg_test + '/ismip-hom-c/80km/ishom.c.80km.JFNK.trilinos.config'
                        bench_configure_path = reg_test + '/bench/ismip-hom-c/80km/ishom.c.80km.JFNK.trilinos.config'
                else:
                    c_flag = 0
                    if os.path.isdir(reg_test + '/ismip-hom-c/80km/configure_files/') == True:
                        configure_path = reg_test + '/ismip-hom-c/80km/configure_files/ishom.c.80km.glissade.1.config'
                        bench_configure_path = reg_test + '/bench/ismip-hom-c/80km/configure_files/ishom.c.80km.glissade.1.config'
                    else:
                        configure_path = reg_test + '/ismip-hom-c/80km/ishom.c.80km.glissade.1.config'
                        bench_configure_path = reg_test + '/bench/ismip-hom-c/80km/ishom.c.80km.glissade.1..config'
                VV_utilities.confxml(ishomc80_case,configure_path,bench_configure_path,xml_path,bench_xml_path,c_flag)

                if glide_flag == 1:
                    test_file.write('<TH ALIGN=LEFT><A HREF="ishomc80_plot.html">Plots</A>\n')
                else:
                    test_file.write('<TH ALIGN=LEFT><A HREF="ishomc80_plot_glissade.html">Plots</A>\n')
                test_file.write('<BR>\n')
                #if failedt != 0:
                #    ishomc80_plot.write("<H2>ISMIP HOM C 80km Test failed, plots may not be generated</H2><br>")
                checkpath = reg_test + '/ismip-hom-c/80km/' + data_dir + '/ishom.c.80km.glissade.1.out.nc'
                noplot = VV_checks.emptycheck(checkpath)
                if noplot != 1:
                    VV_ismip.c80plot(glide_flag,ishomc80_plot,reg_test,ncl_path,html_path,script_path,data_dir)

# Time stamping
            mode = os.stat(reg_test + '/ismip-hom-c/80km').st_mtime
            mode = mode - 18000
            mode = time.gmtime(mode)
            ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
            strrand = '<b>Time of Last Simulation: ' + ctime + '</b>'
            test_file.write(strrand)
            test_file.write('<BR>\n')

    else:
        print "NOT RUNNING ISMIP HOM C 80KM TESTCASE"


#apply flag to turn off running test
    if ismip_hom_c20_flag == 1:
        if glide_flag == 0:
# ISMIP HOM C 20km stats
            print "running ismip hom c 20km glissade testcase"
            test_file.write('<BR>\n')
            if dictionary['ismip-hom-c20'] == 0:
                test_file.write('<H2>ISMIP HOM C 20KM Test: <font color="green">Bit-for-Bit</font></H2>')
            else:
                test_file.write('<H2>ISMIP HOM C 20KM Test: <font color="red">NOT Bit-for-Bit</font></H2>')

# put something here to flag BFB results and no need to do any more calculations
            flag_to_plot_ihc = 1
            if flag_to_plot_ihc:

# link to ismip_hom_c20_file with descriptions about the test cases       
                if glide_flag == 1:
                    test_file.write('<TH ALIGN=LEFT><A HREF="ishomc20_details.html">Velocity Solver Details</A>\n')
                    test_file.write('<BR>\n')
                    failedt = VV_ismip.c20details(ishomc20_file,reg_test,data_dir)

                if glide_flag == 1:
                    test_file.write('<TH ALIGN=LEFT><A HREF="ishomc20_case.html">Case and Parameter Settings Details</A>\n')
                else:
                    test_file.write('<TH ALIGN=LEFT><A HREF="ishomc20_case_glissade.html">Case and Parameter Settings Details</A>\n')
                test_file.write('<BR>\n')
                xml_path = reg_test + '/ismip-hom-c/20km/trilinosOptions.xml'
                bench_xml_path = reg_test + '/bench/ismip-hom-c/20km/trilinosOptions.xml'
                if glide_flag == 1:
                    c_flag = 1
                    if os.path.isdir(reg_test + '/ismip-hom-c/20km/configure_files/') == True:
                        configure_path = reg_test + '/ismip-hom-c/20km/configure_files/ishom.c.20km.JFNK.trilinos.config'
                        bench_configure_path = reg_test + '/bench/ismip-hom-c/20km/configure_files/ishom.c.20km.JFNK.trilinos.config'
                    else:
                        configure_path = reg_test + '/ismip-hom-c/20km/ishom.c.20km.JFNK.trilinos.config'
                        bench_configure_path = reg_test + '/bench/ismip-hom-c/20km/ishom.c.20km.JFNK.trilinos.config'
                else:
                    c_flag = 0
                    if os.path.isdir(reg_test + '/ismip-hom-c/20km/configure_files/') == True:
                        configure_path = reg_test + '/ismip-hom-c/20km/configure_files/ishom.c.20km.glissade.1.config'
                        bench_configure_path = reg_test + '/bench/ismip-hom-c/20km/configure_files/ishom.c.20km.glissade.1.config'
                    else:
                        configure_path = reg_test + '/ismip-hom-c/20km/ishom.c.20km.glissade.1.config'
                        bench_configure_path = reg_test + '/bench/ismip-hom-c/20km/ishom.c.20km.glissade.1.config'
                VV_utilities.confxml(ishomc20_case,configure_path,bench_configure_path,xml_path,bench_xml_path,c_flag)

                if glide_flag == 1:
                    test_file.write('<TH ALIGN=LEFT><A HREF="ishomc20_plot.html">Plots</A>\n')
                else:
                    test_file.write('<TH ALIGN=LEFT><A HREF="ishomc20_plot_glissade.html">Plots</A>\n')
                test_file.write('<BR>\n')
                #if failedt != 0:
                #    ishomc20_plot.write("<H2>ISMIP HOM C 20km Test failed, plots may not be generated</H2><br>")
                checkpath = reg_test + '/ismip-hom-c/20km/' + data_dir + '/ishom.c.20km.glissade.1.out.nc'
                noplot = VV_checks.emptycheck(checkpath)
                if noplot != 1:
                    VV_ismip.c20plot(glide_flag,ishomc20_plot,reg_test,ncl_path,html_path,script_path,data_dir)

# Time stamping
            mode = os.stat(reg_test + '/ismip-hom-c/20km').st_mtime
            mode = mode - 18000
            mode = time.gmtime(mode)
            ctime = time.strftime("%m/%d/%Y %I:%M %p", mode)
            strrand = '<b>Time of Last Simulation: ' + ctime + '</b>'
            test_file.write(strrand)
            test_file.write('<BR>\n')

    else:
        print "NOT RUNNING ISMIP HOM C 20KM TESTCASE"


    test_file.write('<BR>\n')
    test_file.write('<BR>\n')
    test_file.write('<TH ALIGN=LEFT><A HREF="livv_kit_main.html">Home</A>\n')
    test_file.write('</HTML>\n')
    test_file.close()

# descript_file = open(options.html_path + '/test_descript.html', 'w')
    descript_file.write('<HTML>\n')
    descript_file.write('<BODY BGCOLOR="#CADFE0">\n')
    descript_file.write('<TITLE>Descriptions about the Test Suite</TITLE>\n')
    descript_file.write('<H2>Test Suite Details</H2>')
    descript_file.write('<BR>\n')
    descript_file.write('The Diagnostic Dome 30 test case \n')
    descript_file.write('<BR>\n')
    descript_file.write('  Attributes: 3-D paraboloid dome of ice with a circular, 60 km diameter base sitting on a flat bed. The horizontal spatial resolution studies are 2 km, 1 km, 0.5 km and 0.25 km, and there are 10 vertical levels. For this set of experiments a quasi no-slip basal condition in imposed by setting. A zero-flux boundary condition is applied to the dome margins. \n')
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
    descript_file.write('  Attributes: Simulates steady ice flow with no basal slip over a sinusoidally varying bed with periodic boundary conditions at 80km resolution. \n')
    descript_file.write('<BR>\n')
    descript_file.write('  What does it test?\n')
    descript_file.write('<BR><BR>\n')
    descript_file.write('The ISMIP HOM A 20km test case \n')
    descript_file.write('<BR>\n')
    descript_file.write('  Attributes: Simulates steady ice flow with no basal slip over a sinusoidally varying bed with periodic boundary conditions at 20km resolution. \n')
    descript_file.write('<BR>\n')
    descript_file.write('  What does it test?\n')
    descript_file.write('<BR><BR>\n')
    descript_file.write('The ISMIP HOM C 80km test case \n')
    descript_file.write('<BR>\n')
    descript_file.write('  Attributes: Simulates steady ice flow with sinusoidally carrying basal traction over a flat bed with periodic boundary conditions. In the experiment, r is specified to equal 0 in the sliding law. \n')
    descript_file.write('<BR>\n')
    descript_file.write('  What does it test? \n')
    descript_file.write('<BR><BR>\n')
    descript_file.write('The Greenland Ice Sheet 5km test cases \n')
    descript_file.write('<BR>\n')
    descript_file.write('  Attributes: This test case represents the Greenland ice sheet (GIS) at different spatial resolutions (10km and 5km). A quasi-no slip boundary condition is applied at the bed. As with the dome test cases, a zero-flux boundary condition is applied to the lateral margins. In all test cases, the ice is taken as isothermal with a constant and uniform rate factor of. \n')
    descript_file.write('<BR>\n')
    descript_file.write('  What does it test? \n')
    descript_file.write('<BR><BR>\n')
    descript_file.write('</HTML>\n')
    descript_file.close()

#   dome30_file.write('</HTML>\n')
#   dome30_file.close()



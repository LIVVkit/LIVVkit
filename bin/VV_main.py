
import sys
import os
import re
from optparse import OptionParser
import subprocess
import collections
import VV_outprocess
import VV_testsuite
import VV_largesuite
import VV_validation_suite
import VV_timing_check

user = os.environ['USER']

#enable use input for filepaths from the command line
usage_string = "%prog [options]"
parser = OptionParser(usage=usage_string)
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
parser.add_option('-G', '--glam', action='store', type='int', dest='glam_flag', \
                  metavar='FLAG', help='flag to run glam test (always run glissade)')
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
parser.add_option('-C', '--ismip-hom-C80', action='store', type='int', dest='ismip_hom_c80_flag', \
                  metavar='FLAG', help='flag to run ismip hom c 80km test')
parser.add_option('-X', '--ismip-hom-C20', action='store', type='int', dest='ismip_hom_c20_flag', \
                  metavar='FLAG', help='flag to run ismip hom c 20km test')
parser.add_option('-J', '--dome60', action='store', type='int', dest='dome60_flag', \
                  metavar='FLAG', help='flag to run dome60 test')
parser.add_option('-K', '--dome120', action='store', type='int', dest='dome120_flag', \
                  metavar='FLAG', help='flag to run dome120 test')
parser.add_option('-L', '--dome240', action='store', type='int', dest='dome240_flag', \
                  metavar='FLAG', help='flag to run dome240 test')
parser.add_option('-F', '--dome500', action='store', type='int', dest='dome500_flag', \
                  metavar='FLAG', help='flag to run dome500 test')
parser.add_option('-M', '--dome1000', action='store', type='int', dest='dome1000_flag', \
                  metavar='FLAG', help='flag to run dome1000 test')
parser.add_option('-T', '--gis1km', action='store', type='int', dest='gis_1km_flag', \
                  metavar='FLAG', help='flag to run gis1km test')
parser.add_option('-U', '--gis2km', action='store', type='int', dest='gis_2km_flag', \
                  metavar='FLAG', help='flag to run gis2km test')
parser.add_option('-W', '--gis4km', action='store', type='int', dest='gis_4km_flag', \
                  metavar='FLAG', help='flag to run gis4km test')
parser.add_option('-V', '--validation', action='store', type='int', dest='validation_flag', \
                  metavar='FLAG', help='flag to run validation')
#parser.add_option('-ANT', '--ant_prod', action='store_true', dest='ant_prod', \
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

#remove www/livv directory if it exists
if os.path.isdir(options.html_path + 'livv') == True:
    rmdir = ['rm', '-rf', options.html_path + 'livv']
    try:
        subprocess.check_call(rmdir)
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))

#create www directory if it doesn't exists already
if os.path.isdir(options.html_path) == True:
    
        target_html = options.html_path
else:
        mkdir = ['mkdir', options.html_path]
        try:
                subprocess.check_call(mkdir)
        except subprocess.CalledProcessError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.returncode)
        except OSError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.errno)

#remove html/livv if it already exists
if os.path.isdir(options.html_path + 'livv') == True:

        remove_html = ['rm', '-rf', options.html_path+'livv']
        try:
                subprocess.check_call(remove_html)
        except subprocess.CalledProcessError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.returncode)
        except OSError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.errno)

#create www/livv directory
mkdir = ['mkdir', options.html_path+'livv']
try:
        subprocess.check_call(mkdir)
except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)

target_html = options.html_path + 'livv'

if (options.username):
	print 'placing HTML files in the ' + options.username + ' subdirectory (check permissions)'
else:
	print 'no username specified, placing HTML files in the main html directory'

#remove plot_details file previously used in specified subdirectory
if (options.test_suite + '/livv/plot_details.out'):
        plotdetails = ["rm", "-f", "plot_details.out"]
        try:
                subprocess.check_call(plotdetails)
        except subprocess.CalledProcessError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.returncode)
        except OSError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.errno)

#remove iter_details file previously used in specified subdirectory
if (options.test_suite + '/livv/iter_details.out'):
        iterdetails = ["rm", "-f", "iter_details.out"]
        try:
                subprocess.check_call(iterdetails)
        except subprocess.CalledProcessError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.returncode)
        except OSError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.errno)

#remove valid_details file previously used in specified subdirectory
if (options.test_suite + '/livv/valid_details.out'):
        validdetails = ["rm", "-f", "valid_details.out"]
        try:
                subprocess.check_call(validdetails)
        except subprocess.CalledProcessError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.returncode)
        except OSError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.errno)

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


#create all the test suite diagnostics pages for glam
if options.test_suite and options.glam_flag:
        glam_flag = options.glam_flag 

	test_file = open(target_html + '/test_suite.html', 'w')
        descript_file = open(target_html + '/test_descript.html', 'w')
# diagnostic dome case
        dome30d_file = open(target_html + '/dome30d_details.html', 'w')
        dome30d_case = open(target_html + '/dome30d_case.html', 'w')
        dome30d_plot = open(target_html + '/dome30d_plot.html', 'w')
# evolving dome case
        dome30e_file = open(target_html + '/dome30e_details.html', 'w')
        dome30e_case = open(target_html + '/dome30e_case.html', 'w')
        dome30e_plot = open(target_html + '/dome30e_plot.html', 'w')
#circular shelf case
        circ_file = open(target_html + '/circ_details.html', 'w')
        circ_case = open(target_html + '/circ_case.html', 'w')
        circ_plot = open(target_html + '/circ_plot.html', 'w')
# confined shelf case
        conf_file = open(target_html + '/conf_details.html', 'w')
        conf_case = open(target_html + '/conf_case.html', 'w')
        conf_plot = open(target_html + '/conf_plot.html', 'w')
# ismip hom a 80km case
        ishoma80_file = open(target_html + '/ishoma80_details.html', 'w')
        ishoma80_case = open(target_html + '/ishoma80_case.html', 'w')
        ishoma80_plot = open(target_html + '/ishoma80_plot.html', 'w')
# ismip hom a 20km case
        ishoma20_file = open(target_html + '/ishoma20_details.html', 'w')
        ishoma20_case = open(target_html + '/ishoma20_case.html', 'w')
        ishoma20_plot = open(target_html + '/ishoma20_plot.html', 'w')
# ismip hom c 80km case
        ishomc80_file = open(target_html + '/ishomc80_details.html', 'w')
        ishomc80_case = open(target_html + '/ishomc80_case.html', 'w')
        ishomc80_plot = open(target_html + '/ishomc80_plot.html', 'w')
# ismip hom c 20km case
        ishomc20_file = open(target_html + '/ishomc20_details.html', 'w')
        ishomc20_case = open(target_html + '/ishomc20_case.html', 'w')
        ishomc20_plot = open(target_html + '/ishomc20_plot.html', 'w')

#path to python code to create all the test suite pages and data
        reg_test = options.test_suite + "/reg_test"

        VV_testsuite.web(glam_flag,descript_file,test_file,dome30d_file,dome30d_case,dome30d_plot, \
                dome30e_file,dome30e_case,dome30e_plot, \
                circ_file,circ_case,circ_plot,conf_file,conf_case,conf_plot, \
                ishoma80_file,ishoma80_case,ishoma80_plot,ishoma20_file,ishoma20_case,ishoma20_plot, \
                ishomc80_file,ishomc80_case,ishomc80_plot,ishomc20_file,ishomc20_case,ishomc20_plot,\
                reg_test,options.test_suite,options.data_dir,options.ncl_path,target_html,options.script_path,\
                options.diagnostic_flag,options.evolving_flag,options.circular_flag,options.confined_flag,\
                options.ismip_hom_a80_flag,options.ismip_hom_a20_flag,options.ismip_hom_c80_flag,options.ismip_hom_c20_flag)

        dictionary = VV_testsuite.bit_list(reg_test,options.data_dir,options.diagnostic_flag,options.evolving_flag,options.circular_flag,options.confined_flag,\
                        options.ismip_hom_a80_flag,options.ismip_hom_a20_flag,options.ismip_hom_c80_flag,options.ismip_hom_c20_flag)

#create all the test suite diagnostics pages for glissade
if options.test_suite:

        glam_flag = 0
        test_file_glissade = open(target_html + '/test_suite_glissade.html', 'w')
        descript_file_glissade = open(target_html + '/test_descript.html', 'w')
# diagnostic dome case
        dome30d_file_glissade = open(target_html + '/dome30d_details_glissade.html', 'w')
        dome30d_case_glissade = open(target_html + '/dome30d_case_glissade.html', 'w')
        dome30d_plot_glissade = open(target_html + '/dome30d_plot_glissade.html', 'w')
# evolving dome case
        dome30e_file_glissade = open(target_html + '/dome30e_details_glissade.html', 'w')
        dome30e_case_glissade = open(target_html + '/dome30e_case_glissade.html', 'w')
        dome30e_plot_glissade = open(target_html + '/dome30e_plot_glissade.html', 'w')
#circular shelf case
        circ_file_glissade = open(target_html + '/circ_details_glissade.html', 'w')
        circ_case_glissade = open(target_html + '/circ_case_glissade.html', 'w')
        circ_plot_glissade = open(target_html + '/circ_plot_glissade.html', 'w')
# confined shelf case
        conf_file_glissade = open(target_html + '/conf_details_glissade.html', 'w')
        conf_case_glissade = open(target_html + '/conf_case_glissade.html', 'w')
        conf_plot_glissade = open(target_html + '/conf_plot_glissade.html', 'w')
# ismip hom a 80km case
        ishoma80_file_glissade = open(target_html + '/ishoma80_details_glissade.html', 'w')
        ishoma80_case_glissade = open(target_html + '/ishoma80_case_glissade.html', 'w')
        ishoma80_plot_glissade = open(target_html + '/ishoma80_plot_glissade.html', 'w')
# ismip hom a 20km case
        ishoma20_file_glissade = open(target_html + '/ishoma20_details_glissade.html', 'w')
        ishoma20_case_glissade = open(target_html + '/ishoma20_case_glissade.html', 'w')
        ishoma20_plot_glissade = open(target_html + '/ishoma20_plot_glissade.html', 'w')
# ismip hom c 80km case
        ishomc80_file_glissade = open(target_html + '/ishomc80_details_glissade.html', 'w')
        ishomc80_case_glissade = open(target_html + '/ishomc80_case_glissade.html', 'w')
        ishomc80_plot_glissade = open(target_html + '/ishomc80_plot_glissade.html', 'w')
# ismip hom c 20km case
        ishomc20_file_glissade = open(target_html + '/ishomc20_details_glissade.html', 'w')
        ishomc20_case_glissade = open(target_html + '/ishomc20_case_glissade.html', 'w')
        ishomc20_plot_glissade = open(target_html + '/ishomc20_plot_glissade.html', 'w')
        
#path to python code to create all the test suite pages and data
        reg_test = options.test_suite + "/reg_test"

        VV_testsuite.web(glam_flag,descript_file_glissade,test_file_glissade, \
                dome30d_file_glissade,dome30d_case_glissade,dome30d_plot_glissade,dome30e_file_glissade,dome30e_case_glissade,dome30e_plot_glissade, \
                circ_file_glissade,circ_case_glissade,circ_plot_glissade,conf_file_glissade,conf_case_glissade,conf_plot_glissade, \
                ishoma80_file_glissade,ishoma80_case_glissade,ishoma80_plot_glissade,ishoma20_file_glissade,ishoma20_case_glissade,ishoma20_plot_glissade, \
                ishomc80_file_glissade,ishomc80_case_glissade,ishomc80_plot_glissade,ishomc20_file_glissade,ishomc20_case_glissade,ishomc20_plot_glissade, \
                reg_test,options.test_suite,options.data_dir,options.ncl_path,target_html,options.script_path,\
                options.diagnostic_flag,options.evolving_flag,options.circular_flag,options.confined_flag,\
                options.ismip_hom_a80_flag,options.ismip_hom_a20_flag,options.ismip_hom_c80_flag,options.ismip_hom_c20_flag)

        dictionary = VV_testsuite.bit_list(reg_test,options.data_dir,options.diagnostic_flag,options.evolving_flag,options.circular_flag,options.confined_flag,\
                        options.ismip_hom_a80_flag,options.ismip_hom_a20_flag,options.ismip_hom_c80_flag,options.ismip_hom_c20_flag)
        
#create all the large test suite diagnostics pages
if options.dome60_flag==1 or options.dome120_flag==1 or options.dome240_flag==1 or options.dome500_flag==1 \
        or options.dome1000_flag==1 or options.gis_1km_flag==1 or options.gis_2km_flag==1 or options.gis_4km_flag==1:

        large_test_file = open(target_html + '/large_test_suite.html', 'w')
        descript_file = open(target_html + '/large_test_descript.html', 'w')
# dome60 case
        dome60_file = open(target_html + '/dome60_details.html', 'w')
        dome60_case = open(target_html + '/dome60_case.html', 'w')
        dome60_time = open(target_html + '/dome60_timing.html', 'w')
        dome60_plot = open(target_html + '/dome60_plot.html', 'w')
# dome120 case
        dome120_file = open(target_html + '/dome120_details.html', 'w')
        dome120_case = open(target_html + '/dome120_case.html', 'w')
        dome120_time = open(target_html + '/dome120_timing.html', 'w')
        dome120_plot = open(target_html + '/dome120_plot.html', 'w')
# dome240 case
        dome240_file = open(target_html + '/dome240_details.html', 'w')
        dome240_case = open(target_html + '/dome240_case.html', 'w')
        dome240_time = open(target_html + '/dome240_timing.html', 'w')
        dome240_plot = open(target_html + '/dome240_plot.html', 'w')
# dome500 case
        dome500_file = open(target_html + '/dome500_details.html', 'w')
        dome500_case = open(target_html + '/dome500_case.html', 'w')
        dome500_time = open(target_html + '/dome500_timing.html', 'w')
        dome500_plot = open(target_html + '/dome500_plot.html', 'w')
# dome1000 case
        dome1000_file = open(target_html + '/dome1000_details.html', 'w')
        dome1000_case = open(target_html + '/dome1000_case.html', 'w')
        dome1000_time = open(target_html + '/dome1000_timing.html', 'w')
        dome1000_plot = open(target_html + '/dome1000_plot.html', 'w')
# gis 1km case
        gis1km_file = open(target_html + '/gis1km_details.html', 'w')
        gis1km_case = open(target_html + '/gis1km_case.html', 'w')
        gis1km_time = open(target_html + '/gis1km_timing.html', 'w')
        gis1km_plot = open(target_html + '/gis1km_plot.html', 'w')
# gis 2km case
        gis2km_file = open(target_html + '/gis2km_details.html', 'w')
        gis2km_case = open(target_html + '/gis2km_case.html', 'w')
        gis2km_time = open(target_html + '/gis2km_timing.html', 'w')
        gis2km_plot = open(target_html + '/gis2km_plot.html', 'w')
# gis 4km case
        gis4km_file = open(target_html + '/gis4km_details.html', 'w')
        gis4km_case = open(target_html + '/gis4km_case.html', 'w')
        gis4km_time = open(target_html + '/gis4km_timing.html', 'w')
        gis4km_plot = open(target_html + '/gis4km_plot.html', 'w')

#path to python code to create all the large test suite pages and data
        perf_test = options.test_suite + "/perf_test"

        VV_largesuite.large_tests(descript_file,large_test_file,dome60_file,dome60_case,dome60_time,dome60_plot, \
                dome120_file,dome120_case,dome120_time,dome120_plot,dome240_file,dome240_case,dome240_time,dome240_plot, \
                dome500_file,dome500_case,dome500_time,dome500_plot,dome1000_file,dome1000_case,dome1000_time,dome1000_plot, \
                gis1km_file,gis1km_case,gis1km_time,gis1km_plot, \
                gis2km_file,gis2km_case,gis2km_time,gis2km_plot, \
                gis4km_file,gis4km_case,gis4km_time,gis4km_plot, \
                perf_test,options.ncl_path,target_html,options.script_path, \
                options.dome60_flag,options.dome120_flag,options.dome240_flag, \
                options.dome500_flag,options.dome1000_flag,options.gis_1km_flag, \
                options.gis_2km_flag,options.gis_4km_flag,options.data_dir)

        dictionary_large = VV_largesuite.time_check(perf_test,options.dome60_flag,options.dome120_flag,options.dome240_flag,\
                            options.dome500_flag,options.dome1000_flag,options.gis_1km_flag,options.gis_2km_flag,options.gis_4km_flag)

#create all the validation plot pages
if options.validation_flag!=0:

        valid_file = open(target_html + '/validation_plots.html', 'w')
        details_file = open(target_html + 'case_details.html', 'w')
# table
        table = open(target_html + '/table.html', 'w')
# figure1
        figure1_plot = open(target_html + '/figure1_plot.html', 'w')
# figure2
        figure2_plot = open(target_html + '/figure2_plot.html', 'w')
# figure3
        figure3_plot = open(target_html + '/figure3_plot.html', 'w')
# figure4
        figure4_plot = open(target_html + '/figure4_plot.html', 'w')
# figure5
        figure5_plot = open(target_html + '/figure5_plot.html', 'w')

#path to python code to create all the test suite pages and data

        VV_validation_suite.web(valid_file,details_file,table,figure1_plot,figure2_plot,figure3_plot,figure4_plot,figure5_plot, \
                options.data_dir,options.ncl_path,target_html,options.script_path)

#writing the main HTML page

file = open(target_html + '/livv_kit_main.html', 'w')

file.write('<HTML><HEAD>\n')
file.write('<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">')
file.write('<title>Land Ice Verification and Validation toolkit</title>')
file.write('<link href="style.css" rel="stylesheet" type="text/css">')
file.write('<BODY>\n')
file.write('<BODY BGCOLOR="#CADFE0">\n')
file.write(' <div id="container"> <div id="content">')
file.write('<P>\n')
file.write('<OBJECT data="alaska_pic.png" type="image/png" width="400" height="300" hspace=10 align=left alt="ice sheet pic">\n')
file.write('</OBJECT>\n')
file.write('<FONT color=blue><B>\n')
file.write('Land Ice Verification and Validation Package  </B></FONT> <BR>\n')
file.write('Performed on ' + options.time_stamp + '<BR>\n')
file.write('Test case run by: ' + options.username + '<BR>\n')
file.write('Details: ' + options.comment + '<BR>\n')
file.write('</P>\n')
file.write('<BR clear=left>\n')
file.write('<BR>\n')
file.write('<HR noshade size=2 size="100%">\n')
if 1 in dictionary.values():
        file.write('<font color="red"> All Cases NOT Bit-for-Bit</font><br>')
else:
        file.write('<font color="green"> All Cases Bit-for-Bit</font><br>')
file.write('<BR>\n')
if options.test_suite and options.glam_flag:

	file.write('<TH ALIGN=LEFT><A HREF="test_suite.html">Basic Verification Test Suite Diagnostics - Glide</A>\n')
	file.write('<BR>\n')
	file.write('<BR>\n')

file.write('<TH ALIGN=LEFT><A HREF="test_suite_glissade.html">Basic Verification Test Suite Diagnostics - Glissade</A>\n')
file.write('<BR>\n')
file.write('<BR>\n')
file.write('<BR>\n')
file.write('<BR>\n')

if options.dome60_flag==1 or options.dome120_flag==1 or options.dome240_flag==1 or options.dome500_flag==1 \
        or options.dome1000_flag==1 or options.gis_1km_flag==1 or options.gis_2km_flag==1 or options.gis_4km_flag==1:
        
        if 1 in dictionary_large.values() or 2 in dictionary_large.values():
                file.write('<font color="red"> Not All Tests Within Expected Performance Range</font><br>')
                file.write('<BR>\n')
        else:
                file.write('<font color="green"> All Tests Within Expected Performance Range</font><br>')
                file.write('<BR>\n')
        
        file.write('<TH ALIGN=LEFT><A HREF="large_test_suite.html">Performance and Analysis Test Suite (pLIVV)</A>\n')
        
        if 1 in dictionary_large.values() or 2 in dictionary_large.values():
                file.write('<font color="red"> Not All Tests Within Expected Performance Range</font><br>')
        else:
                file.write('<font color="green"> All Tests Within Expected Performance Range</font><br>')

file.write('<BR>\n')
file.write('<BR>\n')
file.write('<BR>\n')
file.write('<BR>\n')
if options.validation_flag==1:
        file.write('<TH ALIGN=LEFT><A HREF="validation_plots.html">Validation Plots</A>\n')

file.write('<h4> For Additional Information: </h4> <p>')
file.write(' Kate Evans <br>')
file.write('Oak Ridge National Laboratory<br>')
file.write('1 Bethel Valley Road <br>')
file.write('Oak Ridge, Tennessee 37831-6015 <br>')
file.write('Email: 4ue@ornl.gov <br> </p>')

file.write('</BODY>\n')
file.write('</HTML>\n')
file.close()

if options.data_dir == "data_hopper":
	print "LIVV Completed. Go to " + options.html_link + " to view results"
else:
	print "LIVV Completed. Go to " + options.html_link + "livv/livv_kit_main.html to view results"


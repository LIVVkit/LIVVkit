import sys
import os
import re
from optparse import OptionParser
import subprocess
import collections
import VV_outprocess

def conf(con_file,configure_path):
        def makehashdome():
                return collections.defaultdict(makehashdome)
        data = makehashdome()

        con_flag = False
        keywords = ('parameters', 'CF output', 'grid', 'time', 'options')
        variable, value = '', ''


	for kw in keywords:
		try:
			configlog = open(configure_path, "r")
                except:
                        print "error reading configure file, or no file specified"
                        sys.exit(1)
                        raise

                for cfline in configlog:
                        if cfline.startswith('[' + kw + ']'):
                               con_flag = True
                               continue
                        if cfline.startswith('['):
                                con_flag = False
                                continue
                        if con_flag == True:
                                line = cfline.strip('\r\n')
                                if '#' in line:
                                        tmp = line.split('#')
                                        line = tmp[0]
                                if line == '':
                                        continue
                                if line.endswith('='):
                                        variable, junk = line.split()
                                        value = ''
                                else:
                                        variable, value = line.split('=')
                                variable = variable.strip()
                                value = value.strip()
                                data[kw][variable] = value

                configlog.close()

#Calculate number of time steps
        if data['time']['tend'] and data['time']['tstart']:
                diff = float(data['time']['tend']) - float(data['time']['tstart'])
                timestp = diff / float(data['time']['dt'])

        con_file.write('<HTML>\n')
        con_file.write('<TITLE>GIS Configure Diagnostics</TITLE>\n')
        con_file.write('<H2>Configure File Diagnostics</H2>')
        con_file.write("CF Output<BR>\n")
        con_file.write("-----------------------<BR>\n")
        if data['CF output']['variables']:
                con_file.write('variables = ' + data['CF output']['variables'] + "<BR>\n")
        con_file.write('<BR\n>')
        con_file.write("Grid<BR>\n")
        con_file.write("-----------------------<BR>\n")
        if data['grid']['upn']:
                con_file.write("upn = " + data['grid']['upn'] + "<BR>\n")
        if data['grid']['ewn']:
                con_file.write("ewn = " +  data['grid']['ewn'] + "<BR>\n")
        if data['grid']['nsn']:
                con_file.write("nsn = " + data['grid']['nsn'] + "<BR>\n")
        if data['grid']['dew']:
                con_file.write("dew = " + data['grid']['dew'] + "<BR>\n")
        if data['grid']['dns']:
                con_file.write("dns = " + data['grid']['dns'] + "<BR>\n")
        con_file.write('<BR\n>')
        con_file.write("Time<BR>\n")
        con_file.write("------------------------<BR>\n")
        if data['time']['tstart']:
                con_file.write("tstart = " + data['time']['tstart'] + "<BR>\n")
        if data['time']['tend']:
                con_file.write("tend = " + data['time']['tend'] + "<BR>\n")
        if data['time']['tend'] and data['time']['tstart']:
                con_file.write("# of time steps = " + str(timestp) + "<BR>\n")
        con_file.write('<BR\n>')
        con_file.write("Parameters<BR>\n")
        con_file.write("------------------------<BR>\n")
        if data['parameters']['ice_limit']:
                con_file.write("ice_limit = " + data['parameters']['ice_limit'] + "<BR>\n")
        if data['parameters']['flow_factor']:
                con_file.write("flow_factor = " + data['parameters']['flow_factor'] + "<BR>\n")
        con_file.write('<BR\n>')
        con_file.write("Options<BR>\n")
        con_file.write("------------------------<BR>\n")
        if data['options']['flow_law']:
                con_file.write("flow_law = " + data['options']['flow_law'] + "<BR>\n")
        if data['options']['evolution']:
                con_file.write("evolution = " + data['options']['evolution'] + "<BR>\n")
        if data['options']['temperature']:
                con_file.write("temperature = " + data['options']['temperature'] + "<BR>\n")
        con_file.write('<BR\n>')
        con_file.write('</HTML>\n')
        con_file.close()


def outfile(out_file,gis_output,filename):
   
# grabbing data from the job output file from the production run
    out_file.write('<HTML>\n')
    out_file.write('<TITLE>Production Job Output Diagnostics</TITLE>\n')
    procttl, nonlist, avg2, out_flag, nd_name, ld_name = VV_outprocess.jobprocess(gis_output,filename)
#   if error_flag == 1:
#       out_file.write('<FONT COLOR="purple"><H1>Model run incomplete, pick a new job output file for diagnostics!</H1></FONT>')
    if out_flag == 1:
            out_file.write('<FONT COLOR="red"><H2>Job Output Diagnostics</H2></FONT>')
    else:
            out_file.write('<H2>Job Output Diagnostics</H2>')

# create iteration plots for proudction simulation
#       data_script=options.ncl_path + "/solver_gis.ncl"
#
#       plot_gis_data = "ncl 'nfile=\"" + options.data_path + "" + nd_name + "\"'" + ' ' + \
#                     "'lfile=\"" + options.data_path + "" + ld_name + "\"'" + ' ' + \
#                     "'PNG=\"" + options.ncl_path + "/gis5km_iter\"'" + ' ' + \
#                    data_script + ' ' + "1> /dev/null"
#       print options.data_path
#
#       try:
#               output = subprocess.call(plot_gis_data, shell=True)
#       except:
#               print "error formatting iteration plot of production run"
#               raise

#transferring thickness plot to www location

#       if (options.ncl_path + '/gis5km_iter.png'):
#               iterpic = "mv -f " + options.ncl_path + "/gis5km_iter.png" + " " + target_html + "/"
#               try:
#                       output = subprocess.call(iterpic, shell=True)
#               except:
#                       print "error moving iter png file"
#                       raise

#    out_file.write('<TABLE>\n')
#    out_file.write('<TR>\n')
#    out_file.write('<H4>Iteration Count for Nonlinear and Linear Solver</H4>\n')
#    out_file.write('<OBJECT data="gis5km_iter.png" type="image/png" width="1300" height="800" hspace=10 align=left alt="Solver Plots">\n')
#    out_file.write('</OBJECT>\n')
#    out_file.write('<TR>\n')
#    out_file.write('<BR>\n')
#    out_file.write('</TABLE>\n')

    out_file.write('<BR>\n')
    out_file.write("Number of Processors = " + str(procttl[-1]) + "<BR>\n")
    out_file.write("Number of Nonlinear Iterations = ")

    for item in nonlist:
            out_file.write(str(item) + ", ")
    out_file.write('<BR>\n')
    if out_flag == 1:
            out_file.write('<FONT COLOR="red">***TIME STEP(S) WHICH FAILED TO CONVERGE</FONT> <BR>\n')
    out_file.write("Average Number of Linear Iterations per Time-Step = ")

    for item in avg2:
            out_file.write(str(item) + ", ")
    out_file.write('<BR>\n')
    out_file.write('</HTML>\n')
    out_file.close()


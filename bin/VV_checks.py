#!/opt/local/bin/python2.7
# #!/usr/bin/env

import sys
import os
from optparse import OptionParser
import subprocess
import collections
import netCDF4
from netCDF4 import Dataset
import glob

#pulls out the name of the file
def yank(temp):
    word = ''
    letter = ''
    for letter in temp:
        if letter == '/':
            word = ''
        word = word + letter
    return word


#zerocheck
def zerocheck(filename):
    data_vars =['thk', 'velnorm']
    data_ac_vars = []
    input_netcdf = filename
    netCDF4.python3 = True
    netCDF4.default_encoding = 'iso8859-1'
    if not os.path.isfile(input_netcdf):
        print("File does not exist: ", input_netcdf)
        sys.exit(0) 
    else:
        netcdf = Dataset(input_netcdf, 'r')


#read in variable from file. Don't know which one so try each.
#for v in data_vars:
    for var in data_vars:
        #input = open(filename)
        data_ac_vars = netcdf.variables.keys()
        if var not in data_ac_vars:
            return 0
        data = netcdf.variables[var][:]
        #print "got here with " + filename + " and variable: " + var
        time = netcdf.variables['time']
        if var != 'thk':
            level = netcdf.variables['level']
        if var == 'velnorm':
            x = netcdf.variables['x0']
            y = netcdf.variables['y0']
        else:
            x = netcdf.variables['x1']
            y = netcdf.variables['y1']
            change = False
            if var == 'thk':
                for t in range(time.size):
                    for j in range(y.size):
                        for i in range(x.size): 
                            if data[t, j, i] != 0.0:
                                change = True
            else:
                for t in range(time.size):
                    for l in range(level.size):
                        for j in range(y.size):
                            for i in range(x.size):
                                if data[t, l, j, i] != 0.0:
                                    change = True

    if change:
        return 1
    else:
        return 0


#bit4bit check
def bit4bit(model_file_path,bench_file_path):
    a = []
    b = []
    flag = []
    bench_file = ''

    model_file_list = glob.glob(model_file_path + '/*.nc')
    bench_file_list = glob.glob(bench_file_path + '/*.nc')

    output = open("temp.txt", 'w')
    output.write(model_file_path)
    output.write('\n')
    output.write(bench_file_path)
    output2 = ['rm', '-rf', 'temp.txt']

    try:
        subprocess.check_call(output2)
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)

    for bench_file in bench_file_list:
        for model_file in model_file_list:
            word1 = yank(bench_file)
            word2 = yank(model_file)
            if word1 == word2:
                file1 = bench_file
                file2 = model_file
                #print "Comparing: " + file1 + " and  " + file2
                comline = ['ncdiff', file1, file2, model_file_path+'/temp.nc', '-O']
                try:
                    subprocess.check_call(comline)
                except subprocess.CalledProcessError as e:
                    print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                            + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                    exit(e.returncode)
                except OSError as e:
                    print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                            + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                    exit(e.errno)
            
                flag.append(zerocheck(model_file_path + '/temp.nc'))
                comline = ['rm', model_file_path+'/temp.nc']
                try:
                    subprocess.check_call(comline)
                except subprocess.CalledProcessError as e:
                    print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                            + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                    exit(e.returncode)
                except OSError as e:
                    print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                            + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                    exit(e.errno)

#match up the md5sums in a and b, tell if bit-for-bit for each specific case
    if 1 in flag:
        return 1
    else:
        return 0
                        

#test failure check
def failcheck(job_path, path):
    failedt = 0
    flag = 0

    input = open(job_path + path, 'r')

    for line in input:
        if 'FATAL' in line:
            flag = 1
    input.close()

    input = open(job_path + path, 'r')

    while 1:
        line = input.readline()
        if line == '':
            return
        if line == "-- Final Status Test Results --\n":
            line = input.readline()
        for letter in line:
            if letter == 'F' or flag == 1:
                return 1
            else:
                return 0


def emptycheck(checkpath):
    noplot = 0
    comline = ('ncdump -c ' + checkpath + ' > ' + 'temp.txt')
    try:
        os.system(comline)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)


    input = open('temp.txt', 'r')
    line = ''

    for line in input:
        if line.find('// (0 currently)') != -1:
            noplot = 1

    comline2 = ['rm', 'temp.txt']
    try:
        subprocess.check_call(comline2)
    except subprocess.CalledProcessError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.returncode)
    except OSError as e:
        print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
        exit(e.errno)

        return noplot


def driver_check(file):

    try:
        config = open(file, 'r')
    except:
        print "error reading" + file
        sys.exit(1)
        raise

    for line in config:
        if "dycore" in line:
            driver = line.split()[2]
            if driver == '1':
                driver = 'glide'
                c_flag = 1
            if driver == '0':
                driver = 'glide'
                c_flag = 1
            elif driver == '2':
                driver = 'glissade'
                c_flag = 0
    
    return driver,c_flag

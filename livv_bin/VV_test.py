'''
Runs a test

Created on Dec 8, 2014

@author: bzq
'''

import sys
import os
import fnmatch
from optparse import OptionParser
import subprocess
import collections
import netCDF4
from netCDF4 import Dataset
import glob
import numpy

#
# Master run for LIVV tests.
#
# Input:
#   testCases: names of test cases to be run
#   testDirs: locations of files for each test
#   benchDirs: locations of benchmarks for each test
#
# Output:
#   to be determined
#
def run(testCases, testDir, benchDir):
    
    # Run the bit for bit tests and record the results in a dictionary
    print("Running bit for bit tests....")
    result = {-1 : 'N/A', 0 : 'SUCCESS', 1 : 'FAILURE'}
    bitList = { test : bit4bit(test, testDir, benchDir) for test in testCases}
    print("\nBit for bit summary: ")
    for test in bitList:
        print("  Test: " + test + "\t Result: " + result[bitList[test]])     
        
    print("\nRunning case specific tests....")
    for test in testCases:
        print("  No tests available for " + test + " at this moment.  Coming soon!")
    return 'in progress...'

    # Run specific test cases
    

#
# Tests all models and benchmarks against eachother in a bit for bit fashion.  
# If any differences are found the method will return 1, otherwise 0.  
#
# Input:
#   modelPath: the path to the model data
#   benchPath: the path to the benchmark data
#
# Output:
#   change: Is 0 if no changes were found, 1 otherwise
#
def bit4bit(test, modelPath, benchPath):
    # First, make sure that there is test data, otherwise not it.
    if not (os.path.exists(modelPath + "/" + test) or os.path.exists(benchPath + "/" + test)):
        print("Could not find model and benchmark data for " + test + "!  Skipping...")
        return -1     
    
    
    # Keeps track of whether there has been a change
    change = 0

    # Get all of the .nc files in the model directory
    modelFiles = []
    for file in os.listdir(modelPath + "/" + test):
        if fnmatch.fnmatch(file, '*.nc'):
            print(file)
            modelFiles.append(file)
                
    # Get all of the .nc files in the benchmark directory
    benchFiles = []
    for file in os.listdir(benchPath + "/" + test):
        if fnmatch.fnmatch(file, '*.nc'):
            print(file)
            modelFiles.append(file)

    # Get the intersection of the two file lists
    sameList = set(modelFiles).intersection(benchFiles)
   
    if len(sameList) == 0:
        print("  No benchmarks available for " + test)
        return -1
    else:
        print("  Running bit for bit tests of " + sameList + "....")
    
    # Go through and check if any differences occur
    for same in list(sameList):
        print("    Bit for bit test: " + same)
        modelFile = modelPath + os.pathsep + same
        benchFile = benchPath + os.pathsep + same
        
        # check if they match
        comline = ['ncdiff', modelFile, benchFile, modelPath + os.pathsep + 'temp.nc', '-O']
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
            
        # Grab the output of ncdiff
        diffData = Dataset(modelPath + os.pathsep + 'temp.nc', 'r')
        diffVars = diffData.variables.keys()
        
        # TODO: Could improve the nested loops by using numpy's any function
        # Check if any data in thk has changed, if it exists
        if 'thk' in diffVars:
            data = diffData.variable['thk'][:]
            x = diffData.variables['x1']
            y = diffData.variables['y1']
            t = diffData.variables['time']
            for k in range(t.size):
                for j in range(y.size):
                    for i in range(x.size): 
                        if data[k, j, i] != 0.0:
                            change = 1
                            
        # Check if any data in velnorm has changed, if it exists
        if 'velnorm' in diffVars:
            data = diffData.variables['velnorm'][:]
            x = diffData.variables['x0']
            y = diffData.variables['y0']
            l = diffData.variables['level']
            for k in range(l.size):
                for j in range(y.size):
                    for i in range(x.size): 
                        if data[k, j, i] != 0.0:
                            change = 1
        
        # Remove the temp file
        try:
            os.remove(modelPath + os.pathsep + 'temp.nc')
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                  + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)

    # If anything has changed, return 1, otherwise returns 0
    return change

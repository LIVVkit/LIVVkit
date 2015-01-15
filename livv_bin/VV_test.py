'''
Runs a test

Created on Dec 8, 2014

@author: bzq
'''

import sys
import os
import time
import fnmatch
import subprocess
import collections
import netCDF4
from netCDF4 import Dataset
import glob
import numpy
from abc import ABCMeta, abstractmethod
import livv

#
#
#
#
#
class AbstractTest(object):
    __metaclass__ = ABCMeta
    # Mapping of result codes to results
    result = {-1 : 'N/A', 0 : 'SUCCESS', 1 : 'FAILURE'}
    
    #
    # Definition for the general test run
    #
    @abstractmethod
    def run(self, test):
        pass
      
    #
    # Definition for how to generate test specific web pages
    #
    @abstractmethod
    def generate(self):
        pass  
    
    #
    # Tests all models and benchmarks against each other in a bit for bit fashion.  
    # If any differences are found the method will return 1, otherwise 0.  
    #
    # Input:
    #   modelPath: the path to the model data
    #   benchPath: the path to the benchmark data
    #
    # Output:
    #   change: Is 0 if no changes were found, 1 otherwise
    #
    def bit4bit(self, test):
        # First, make sure that there is test data, otherwise not it.
        modelPath = livv.inputDir
        benchPath = livv.benchmarkDir
        if not (os.path.exists(modelPath + "/" + test) or os.path.exists(benchPath + "/" + test)):
            print("Could not find model and benchmark data for " + test + "!  Skipping...")
            return -1     
           
        # Keeps track of whether there has been a change
        change = 0
    
        # Get all of the .nc files in the model directory
        modelFiles = []
        for file in os.listdir(modelPath + "/" + test):
            if fnmatch.fnmatch(file, '*.nc'):
                modelFiles.append(file)
                    
        # Get all of the .nc files in the benchmark directory
        benchFiles = []
        for file in os.listdir(benchPath + "/" + test):
            if fnmatch.fnmatch(file, '*.nc'):
                benchFiles.append(file)
    
        # Get the intersection of the two file lists
        sameList = set(modelFiles).intersection(benchFiles)
       
        if len(sameList) == 0:
            print("  Benchmark and model data not available for " + test)
            return -1
        else:
            print("  Running bit for bit tests of " + test + "....")
        
        # Go through and check if any differences occur
        for same in list(sameList):
            modelFile = modelPath + '/' + test + '/' + same
            benchFile = benchPath + '/' + test + '/' + same
            
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
                data = diffData.variables['thk'][:]
                if data.any():
                    change = 1
                                                    
            # Check if any data in velnorm has changed, if it exists
            if 'velnorm' in diffVars:
                data = diffData.variables['velnorm'][:]
                if data.any():
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

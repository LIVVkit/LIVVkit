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
import shutil
import collections
import netCDF4
from netCDF4 import Dataset
import glob
import numpy
import jinja2
from abc import ABCMeta, abstractmethod
import livv
from livv import *

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
    # Should return the name of the test
    #
    @abstractmethod
    def getName(self):
        pass
    
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
        modelPath = livv.inputDir + livv.dataDir
        benchPath = livv.benchmarkDir + livv.dataDir
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

    #
    # Definition for the general parser for standard output
    #
    # input:
    #   file: the file to be parsed
    #
    def parse(self, file):
        # Initialize a dictionary that will store all of the information
        testDict = dict()
        
        # Set up variables that we can use to map data and information
        dycoreTypes = {"0" : "Glide", "1" : "Glam", "2" : "Glissade", "3" : "AlbanyFelix", "4" : "BISICLES"}
        numberProcs = 0
        currentStep = 0
        avgItersToConverge = 0
        convergedIters = []
        itersToConverge = []
        
        
        # Make sure that we can actually read the file
        try:
            logfile = open(file, 'r')
        except:
            print "ERROR: Could not read " + file + " when parsing for test " + self.getName()
        
        # Go through and build up information about the simulation
        for line in logfile:
            #Determine the dycore type
            if ('CISM dycore type' in line):
                testDict['Dycore Type'] = dycoreTypes[line.split()[-1]]
            
            # Calculate the total number of processors used
            if ('total procs' in line):
                numberProcs += int(line.split()[-1])
            
            # Grab the current timestep
            if ('Nonlinear Solver Step' in line):
                currentStep = int(line.split()[4])
            
            # Get the number of iterations per timestep
            if ('"SOLVE_STATUS_CONVERGED"' in line):
                splitLine = line.split()
                itersToConverge.append(int(splitLine[splitLine.index('"SOLVE_STATUS_CONVERGED"') + 2]))
                
            # If the timestep converged mark it with a positive
            if ('Converged!' in line):
                convergedIters.append(currentStep)
                
            # If the timestep didn't converge mark it with a negative
            if ('Failed!' in line):
                convergedIters.append(-1*currentStep)
            
        # Calculate the average number of iterations it took to converge
        if (len(itersToConverge) > 0):
             avgItersToConverge = sum(itersToConverge) / len(itersToConverge)
    
        # Record some of the data in the testDict
        testDict['Number of processors'] = numberProcs
        testDict['Number of timesteps'] = currentStep
        if avgItersToConverge > 0:
            testDict['Average iterations to converge'] = avgItersToConverge 
        
        return testDict     
#
#
#
#
class GenericTest(AbstractTest):
    #
    # Return the name of the test
    # 
    def getName(self):
        return "generic test"
    
    #
    # Prepare the index of the website.
    #
    # input:
    #   testsRun: the top level names of each of the tests run
    #   testCases: the specific test cases being run
    #
    def webSetup(self, testsRun, testCases):   
        # Create directory structure
        for siteDir in [livv.indexDir, livv.testDir, livv.imgDir]:
            if not os.path.exists(siteDir):
                os.mkdir(siteDir);
        # Copy over css from source
        if os.path.exists(livv.indexDir + "/css"): shutil.rmtree(livv.indexDir + "/css")
        shutil.copytree(livv.websiteDir + "/css", livv.indexDir + "/css")
        
        # Where to look for page templates
        templateLoader = jinja2.FileSystemLoader( searchpath=livv.templateDir )
        templateEnv = jinja2.Environment( loader=templateLoader )
        
        # Create the index page
        templateFile = "/index.html"
        template = templateEnv.get_template( templateFile )
        
        # Set up imgs directory to have sub-directories for each test
        for test in testsRun:
            if not os.path.exists(imgDir + "/" + test):
                os.mkdir(imgDir + "/" + test)
        
        templateVars = {"indexDir" : livv.indexDir,
                        "testsRun" : testsRun,
                        "timestamp" : livv.timestamp,
                        "user" : livv.user,
                        "testCases" : testCases,
                        "cssDir" : "css" }
        
        # Write out the index page
        outputText = template.render( templateVars )
        page = open(indexDir + "/index.html", "w")
        page.write(outputText)
        page.close()
    
    # Override the abstract methods with empty calls    
    def run(self, test):
        pass
    def generate(self):
        pass

'''
Contains two classes for generalized testing in LIVV.

The AbstractTest class defines several methods that each test class must implement, 
as well as provides bit for bit and stdout parsing capabilities which are inherited
by all derived test classes.  

The TestSummary is a dummy class that is used to generate the index of the output.
It implements a method called webSetup that creates the index with a short summary
of the execution stats.  All other methods are dummies.  Further implementations
similar to TestSummary are discouraged to avoid breaking the AbstractTest template. 

Created on Dec 8, 2014

@author: arbennett
'''

import sys
import re
import os
import time
import fnmatch
import subprocess
import shutil
import collections
import netCDF4
from netCDF4 import Dataset
import matplotlib.pyplot as pyplot
import matplotlib.gridspec as gridspec
import glob
import numpy
import jinja2
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
import livv
from livv import *


## AbstractTest provides a description of how a test should work in LIVV.
#
#  Each test within LIVV needs to be able to run specific test code, and
#  generate its output.  Tests inherit a common method of checking for 
#  bit-for-bittedness as well for parsing the standard output of model output
#
class AbstractTest(object):
    __metaclass__ = ABCMeta
    
    ## Constructor
    #
    @abstractmethod
    def __init__(self):
        pass

    ## Should return the name of the test
    #
    @abstractmethod
    def getName(self):
        pass
    
    ## Definition for the general test run
    #
    @abstractmethod
    def run(self, test):
        pass
      
    ## Definition for how to generate test specific web pages
    #
    @abstractmethod
    def generate(self):
        pass  
        

    ## Tests all models and benchmarks against each other in a bit for bit fashion.  
    #  If any differences are found the method will return 1, otherwise 0.  
    #
    #  Input:
    #    @param modelPath: the path to the model data
    #    @param benchPath: the path to the benchmark data
    #
    #  Output:
    #    @returns change: Is 0 if no changes were found, 1 otherwise
    #
    def bit4bit(self, test):
        # Mapping of result codes to results
        numpy.set_printoptions(threshold='nan')
        result = {-1 : 'N/A', 0 : 'SUCCESS', 1 : 'FAILURE'}
        bitDict = dict()
        
        # First, make sure that there is test data, otherwise not it.
        modelPath = livv.inputDir + test + livv.dataDir
        benchPath = livv.benchmarkDir + test + livv.dataDir
        if not (os.path.exists(modelPath) or os.path.exists(benchPath)):
            return {'No matching benchmark and data files found': ''}     
             
        # Get all of the .nc files in the model & benchmark directories
        regex = re.compile('^[^\.].*?.nc')
        modelFiles = filter(regex.search, os.listdir(modelPath))
        benchFiles = filter(regex.search, os.listdir(benchPath))
    
        # Get the intersection of the two file lists
        sameList = set(modelFiles).intersection(benchFiles)
       
        if len(sameList) == 0:
            print("  Benchmark and model data not available for " + test)
            return {'No matching benchmark and data files found': ''}
        else:
            print("  Running bit for bit tests of " + test + "....")
        
        # Go through and check if any differences occur
        for same in list(sameList):
            change = 0
            absDifference = 0.0
            maxDifference = 0.0
            plotVars = []
            modelFile = modelPath + os.sep + same
            benchFile = benchPath + os.sep + same
            
            # check if they match
            comline = ['ncdiff', modelFile, benchFile, modelPath + os.sep + 'temp.nc', '-O']
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
            diffData = Dataset(modelPath + os.sep + 'temp.nc', 'r')
            diffVars = diffData.variables.keys()
                            
            # Check if any data in thk has changed, if it exists
            if 'thk' in diffVars and diffData.variables['thk'].size != 0:
                data = diffData.variables['thk'][:]
                if data.any():
                    absDifference += numpy.sum(numpy.ndarray.flatten(data))
                    maxDifference = numpy.amax([maxDifference, numpy.amax(data)])
                    plotVars.append('thk')
                    change = 1
                                                    
            # Check if any data in velnorm has changed, if it exists
            if 'velnorm' in diffVars and diffData.variables['velnorm'].size != 0:
                data = diffData.variables['velnorm'][:]
                if data.any():
                    absDifference += numpy.sum(numpy.ndarray.flatten(data))
                    maxDifference = numpy.amax([maxDifference, numpy.amax(data)])
                    plotVars.append('velnorm')
                    change = 1
            
            # If there were any differences plot them out
            if change:
                self.plotDifferences(plotVars, modelFile, benchFile, modelPath + os.sep + 'temp.nc')

            # Remove the temp file
            try:
                os.remove(modelPath + os.sep + 'temp.nc')
            except OSError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                      + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.errno)

    
            bitDict[same] = [result[change], "{:.4g}".format(absDifference)]
        # If anything has changed, return 1, otherwise returns 0
        return bitDict


    ## plotDifferences
    #
    #  When a bit4bit test fails the differences between the datasets need to be
    #  printed out so that a user can inspect them.  
    #
    #  input:
    #    @param plotVars: the variables which differ between datasets
    #    @param modelFile: path to the model output NetCDF file
    #    @param benchFile: path to the benchmark output NetCDF file
    #
    def plotDifferences(self, plotVars, modelFile, benchFile, differenceFile):
        pyplot.figure(figsize=(12, 4*len(plotVars)), dpi=80)
        pyplot.clf()
        nSubplots=len(plotVars)
        for idx, var in enumerate(plotVars):
            # Get the right data
            if var == 'thk':
                varData = Dataset(modelFile, 'r').variables[var]
                modelData = Dataset(modelFile, 'r').variables[var][len(varData)-1]
                benchData = Dataset(benchFile, 'r').variables[var][len(varData)-1]
                diffData = Dataset(differenceFile, 'r').variables[var][len(varData)-1]
            elif var == 'velnorm':
                modelData = Dataset(modelFile, 'r').variables[var][:][0][0]
                benchData = Dataset(benchFile, 'r').variables[var][:][0][0]
                diffData = Dataset(differenceFile, 'r').variables[var][:][0][0]

            # Calculate min and max to scale the colorbars
            max = numpy.amax([numpy.amax(modelData), numpy.amax(benchData)])
            min = numpy.amin([numpy.amin(modelData), numpy.amin(benchData)]) 
                        
            # Plot the model output
            pyplot.subplot(nSubplots,3,1+idx+(idx*nSubplots))
            pyplot.xlabel("Model Data")
            pyplot.ylabel(var)
            pyplot.imshow(modelData, vmin=min, vmax=max, interpolation="bessel")
            pyplot.colorbar()
            pyplot.tight_layout()
            
            # Plot the benchmark data
            pyplot.subplot(nSubplots,3,2+idx+(idx*nSubplots))
            pyplot.xlabel("Benchmark Data")
            pyplot.imshow(benchData, vmin=min, vmax=max, interpolation="bessel")
            pyplot.colorbar()
            pyplot.tight_layout()
            
            # Plot the difference
            pyplot.subplot(nSubplots, 3,3+idx+(idx*nSubplots))
            pyplot.xlabel("Difference")
            pyplot.imshow(diffData, interpolation="bessel")
            pyplot.colorbar()
            pyplot.tight_layout()
        
        # Save the figure
        pyplot.savefig(livv.imgDir + os.sep + self.getName() + os.sep + "bit4bit" + os.sep + modelFile.split(os.sep)[-1] + ".png")
        

    ## Definition for the general parser for standard output
    #
    #  input:
    #    @param file: the file to be parsed
    #
    def parse(self, file):
        # Initialize a dictionary that will store all of the information
        testDict = livv.parserVars.copy()
        
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
                if line.split()[-1] == '=':
                    testDict['Dycore Type'] = dycoreTypes[next(logfile).strip()]
                else:
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
        
        if testDict['Dycore Type'] == None: testDict['Dycore Type'] = 'Unavailable'
        for key in testDict.keys():
            if testDict[key] == None:
                testDict[key] = 'N/A'
        
        return testDict     


## TestSummary provides LIVV the ability to assemble the overview and main page.
#
#  The TestSummary class does not strictly fall under the category of a test
#  but can take advantage of the infrastructure that the AbstractTest class
#  provides.
#
class TestSummary(AbstractTest):
    

    ## Constructor
    #
    def __init__(self):
        return
    
    ## Return the name of the test
    # 
    def getName(self):
        return "test summary"
    
    ## Prepare the index of the website.
    #
    #  input:
    #    @param testsRun: the top level names of each of the tests run
    #    @param testCases: the specific test cases being run
    #
    def webSetup(self, testsRun, testCases):   
        # Create directory structure
        for siteDir in [livv.indexDir, livv.testDir]:
            if not os.path.exists(siteDir):
                os.mkdir(siteDir);
        # Copy over css && imgs directories from source
        if os.path.exists(livv.indexDir + "/css"): shutil.rmtree(livv.indexDir + "/css")
        shutil.copytree(livv.websiteDir + "/css", livv.indexDir + "/css")
        if os.path.exists(livv.indexDir + "/imgs"): shutil.rmtree(livv.indexDir + "/imgs")
        shutil.copytree(livv.websiteDir + "/imgs", livv.indexDir + "/imgs")
        
        # Where to look for page templates
        templateLoader = jinja2.FileSystemLoader( searchpath=livv.templateDir )
        templateEnv = jinja2.Environment( loader=templateLoader )
        
        # Create the index page
        templateFile = "/index.html"
        template = templateEnv.get_template( templateFile )
        
        # Set up imgs directory to have sub-directories for each test
        for test in testsRun:
            if not os.path.exists(imgDir + os.sep + test):
                os.mkdir(imgDir + os.sep + test)
                if not os.path.exists(imgDir + os.sep + test + os.sep + "bit4bit"):
                    os.mkdir(imgDir + os.sep + test + os.sep + "bit4bit")
        
        templateVars = {"indexDir" : livv.indexDir,
                        "testsRun" : testsRun,
                        "timestamp" : livv.timestamp,
                        "user" : livv.user,
                        "comment" : livv.comment,
                        "testCases" : testCases,
                        "cssDir" : "css", 
                        "imgDir" : "imgs"}
        
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

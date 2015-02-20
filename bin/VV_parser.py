'''
A general parser for extracting data from text files

Created on Feb 6, 2015

@author: bzq
'''
import re
import os
import sys
import glob
import subprocess

import livv
from livv import *
from timeit import itertools

## 
#
class Parser(Object):
    
    ## Constructor
    #
    def __init__(self):
        self.outputFiles = []
        self.configFiles = []
    
    ##
    #
    def parseConfigurations(self, modelDir, benchmarkDir):
        modelFiles = os.listDir(modelDir)
        modelData = dict()
        benchmarkFiles = os.listDir(benchmarkDir)
        benchmarkData = dict()
        keywords = ['parameters', 'CF output', 'grid', 'time', 'options', 'ho_options']
        
        # TODO: Use configparser to make this nice and simple
                    
                
    ## parseOutput
    #
    def parseOutput(self, file):
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
            print "ERROR: Could not read " + file
        
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
'''
A general parser for extracting data from text files.  When using parseConfigurations the
resulting dictionaries can be iterated over via the following code:

            for key1,value1 in modelConfigs.iteritems():
                fileName = key1
                for key2,value2 in value1.iteritems():
                    sectionHeader = key2
                    for key3, value3 in value2.iteritems():
                        variable = key3 
                        value = value3.split("#")[0]


Created on Feb 19, 2015

@author: arbennett
'''
import os
import re
import glob
import ConfigParser
import numpy as np

import util.variables
from collections import OrderedDict

'''
The generalized parser for processing text files associated with a test case

The parser class is to be used within test classes to easily get information
from text files.  The two main pieces of functionality of a parser are for
reading configuration files and standard output from simulations.
'''
class Parser(object):
    
    ''' Constructor '''
    def __init__(self):
        self.configParser = ConfigParser.ConfigParser()
        self.benchData, self.modelData = dict(), dict()
        self.nOutputParsed = 0
        self.nConfigParsed, self.nConfigMatched = 0, 0

        # Build an empty ordered dictionary so that the output prints in a nice order
        self.stdOutData = OrderedDict()
        for var in util.variables.parserVars: self.stdOutData[var] = None

    '''
    Get some key details about what was parsed
    
    @return the number of output and configuration files parsed and 
            how many configurations matched the benchmarks
    '''
    def getParserSummary(self):
        return self.nOutputParsed, self.nConfigMatched, self.nConfigParsed

    '''
    Parse through all of the configuration files from a model and benchmark
    
    Parses all of the files in the given directories and stores them as
    nested dictionaries.  The general structure of the dictionaries are
    {filename : {sectionHeaders : {variables : values}}}.  These can be
    looped through for processing using the algorithm listed at the top 
    of this file.
    
    @param modelDir: the directory for the model configuration files
    @param benchDir: the directory for the benchmark configuration files
    @returns modelData, benchData: the nested dictionaries corresponding
             to the files found in the input directories
    '''
    def parseConfigurations(self, modelDir, benchDir, regex):
        # Make sure the locations exist, and if not return blank sets
        if not (os.path.exists(modelDir) and os.path.exists(benchDir)):
            return dict(), dict()
        modelFiles = [fn.split(os.sep)[-1] for fn in glob.glob(modelDir + os.sep + "*" + regex)]
        benchFiles = [fn.split(os.sep)[-1] for fn in glob.glob(benchDir + os.sep + "*" + regex)]
        self.nConfigParsed += len(modelFiles)

        # Pull in the information from the model run
        for modelF in modelFiles:
            modelFile = modelDir + os.sep + modelF
            modelFileData = OrderedDict()
            self.configParser.read(modelFile)

            # Go through each header section (ones that look like [section])
            for section in self.configParser.sections():
                subDict = OrderedDict()

                # Go through each item in the section and put {var : val} into subDict
                for entry in self.configParser.items(section):
                    subDict[entry[0]] = entry[1].split('#')[0] 

                # Map the sub-dictionary to the section 
                modelFileData[section] = subDict.copy()

            # Associate the data to the file
            self.modelData[modelF] = modelFileData

        # Pull in the information from the benchmark 
        for benchF in benchFiles:
            benchFile = benchDir + os.sep + benchF
            benchFileData = OrderedDict()
            self.configParser.read(benchFile)

            # Go through each header section (ones that look like [section])
            for section in self.configParser.sections():
                subDict = OrderedDict()

                # Go through each item in the section and put {var : val} into subDict
                for entry in self.configParser.items(section):
                    subDict[entry[0]] = entry[1].split('#')[0] 

                # Map the sub-dictionary to the section 
                benchFileData[section] = subDict.copy()

            # Associate the data with the file
            self.benchData[benchF] = benchFileData

        # Check to see if the files match
        # TODO: This is unwieldy - can do a better job when I'm thinking better -arbennett
        for file in modelFiles:
            configMatched = True
            for section, vars in self.modelData[file].iteritems():
                for var, val in self.modelData[file][section].iteritems():
                    if file in benchFiles and section in self.benchData[file] and var in self.benchData[file][section]:
                        if val != self.benchData[file][section][var]:
                            configMatched = False
                    else:
                        configMatched = False
            if configMatched: self.nConfigMatched += 1

        return self.modelData, self.benchData

    '''    
    Searches through a standard output file looking key pieces of
    data about the run.  Records the dycore type, the number of 
    processors used, the average convergence rate, and number of 
    timesteps
    
    @param modelDir: the directory with files to parse through
    @param regex: A pattern to match the std output files with
    @returns a mapping of the various parameters to their values from the file
    '''
    def parseStdOutput(self, modelDir, regex):
        # Set up variables that we can use to map data and information
        dycoreTypes = {"0" : "Glide", "1" : "Glam", "2" : "Glissade", "3" : "AlbanyFelix", "4" : "BISICLES"}
        try:
            files = os.listdir(modelDir)
        except:
            files = []
            print("    Could not find model data in" + modelDir)
        files = filter(re.compile(regex).search, files)
        outdata = []

        for fileName in files:
            # Initialize a new set of data
            numberProcs = 0
            currentStep = 0
            avgItersToConverge = 0
            iterNumber = 0
            convergedIters = []
            itersToConverge = []
            self.stdOutData = OrderedDict()

            # Open up the file
            logfile = open(modelDir + os.sep + fileName, 'r')
            self.nOutputParsed += 1

            # Go through and build up information about the simulation
            for line in logfile:
                #Determine the dycore type
                if ('CISM dycore type' in line):
                    if line.split()[-1] == '=':
                        self.stdOutData['Dycore Type'] = dycoreTypes[next(logfile).strip()]
                    else:
                        self.stdOutData['Dycore Type'] = dycoreTypes[line.split()[-1]]

                # Calculate the total number of processors used
                if ('total procs' in line):
                    numberProcs += int(line.split()[-1])

                # Grab the current timestep
                if ('Nonlinear Solver Step' in line):
                    currentStep = int(line.split()[4])
                if ('Compute ice velocities, time = ' in line):
                    currentStep = float(line.split()[-1])

                # Get the number of iterations per timestep
                if ('"SOLVE_STATUS_CONVERGED"' in line):
                    splitLine = line.split()
                    itersToConverge.append(int(splitLine[splitLine.index('"SOLVE_STATUS_CONVERGED"') + 2]))

                if ("Compute dH/dt" in line):
                    itersToConverge.append(int(iterNumber))

                # If the timestep converged mark it with a positive
                if ('Converged!' in line):
                    convergedIters.append(currentStep)

                # If the timestep didn't converge mark it with a negative
                if ('Failed!' in line):
                    convergedIters.append(-1*currentStep)

                splitLine = line.split()
                if len(splitLine) > 0:
                    iterNumber = splitLine[0]

            # Calculate the average number of iterations it took to converge
            if (len(itersToConverge) > 0):
                avgItersToConverge = float(sum(itersToConverge)) / len(itersToConverge)

            # Record some of the data in the self.stdOutData
            self.stdOutData['Number of processors'] = numberProcs
            self.stdOutData['Number of timesteps'] = int(currentStep)
            if avgItersToConverge > 0:
                self.stdOutData['Average iterations to converge'] = avgItersToConverge 
            elif int(currentStep) == 0:
                self.stdOutData['Number of timesteps'] = 1
                self.stdOutData['Average iterations to converge'] = iterNumber

            if not self.stdOutData.has_key('Dycore Type') or self.stdOutData['Dycore Type'] == None: 
                self.stdOutData['Dycore Type'] = 'Unavailable'
            for key in self.stdOutData.keys():
                if self.stdOutData[key] == None:
                    self.stdOutData[key] = 'N/A'

            outdata.append(self.stdOutData)

        return zip(files, outdata)

    ''' 
    Search through gptl timing files 
    
    @param basePath: the directory to look for timing files in
    @returns a summary of the timing data that was parsed
    '''
    def parseTimingSummaries(self, basePath, testName, resolution):
        if not os.path.exists(basePath):
            return []
        times = dict()
        timingFiles = glob.glob(basePath + os.sep + "timing"+ os.sep + testName.lower() + '-t[0-9].' + resolution + ".p[0-9][0-9][0-9].results") 
        timingFiles += (glob.glob(basePath + os.sep + "timing"+ os.sep + testName.lower() + '-t[0-9].' + resolution + ".p[0-9][0-9][0-9].cism_timing_stats") )

        for filePath in timingFiles:
            run = filePath.split(os.sep)[-1].split('.')[2][1:]
            if not times.has_key(run): times[run] = []
            if not os.path.exists(filePath): continue
            
            # Open the file and grab the data outs
            file = open(filePath, 'r')
            for line in file:
                # If the line is empty just go to the next
                if line.split() == []:
                    continue
                
                # If this is a big machine this is how we find the time
                if line.split()[0] == 'cism':
                    times[run].append(float(line.split()[5]))
                    break
                
                # Otherwise it's found here
                if line.split()[0] == filePath.split(os.sep)[-1].replace('results', 'config'):
                    times[run].append(float(line.split()[1]))
            
            # Record the mean, max, and min times found
            times[run] = [np.mean(times[run]), np.max(times[run]), np.min(times[run])]
        return times

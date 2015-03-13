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
import fnmatch
import ConfigParser

import livv
from collections import OrderedDict
from numpy import Infinity, mean

## The generalized parser for processing text files associated with a test case
#
#  The parser class is to be used within test classes to easily get information
#  from text files.  The two main pieces of functionality of a parser are for
#  reading configuration files and standard output from simulations.
#
class Parser(object):

    ## Constructor
    #
    def __init__(self):
        self.configParser = ConfigParser.ConfigParser()
        self.benchData = dict()
        self.modelData = dict()
        self.nOutputParsed = 0
        self.nConfigParsed = 0
        self.nConfigMatched = 0


    ## Get some details about what was parsed
    #
    #  @return the number of output and configuration files parsed and 
    #          how many configurations matched the benchmarks
    #
    def getParserSummary(self):
        return self.nOutputParsed, self.nConfigMatched, self.nConfigParsed


    ## Parse through all of the configuration files from a model and benchmark
    #
    #  Parses all of the files in the given directories and stores them as
    #  nested dictionaries.  The general structure of the dictionaries are
    #  {filename : {sectionHeaders : {variables : values}}}.  These can be
    #  looped through for processing using the algorithm listed at the top 
    #  of this file.
    #
    #  input:
    #    @param modelDir: the directory for the model configuration files
    #    @param benchDir: the directory for the benchmark configuration files
    #
    #  output:
    #    @returns modelData, benchData: the nested dictionaries corresponding
    #      to the files found in the input directories
    #
    def parseConfigurations(self, modelDir, benchDir):
        # Make sure the locations exist, and if not return blank sets
        if not (os.path.exists(modelDir) and os.path.exists(benchDir)):
            return dict(), dict()

        # Pull the files, while filtering out "hidden" ones
        modelFiles = [f for f in os.listdir(modelDir) if not f.startswith('.')]
        benchFiles = [f for f in os.listdir(benchDir) if not f.startswith('.')]
        sameList = set(modelFiles).intersection(benchFiles)
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

        # Return both of the datasets
        return self.modelData, self.benchData


    ## Scrapes a standard output file for some standard information
    #
    #  Searches through a standard output file looking for various
    #  bits of information about the run.  
    #
    #  input:
    #    @param file: the file to parse through
    #
    #  output:
    #    @param testDict: a mapping of the various parameters to
    #      their values from the file
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
            self.nOutputParsed += 1
        except:
            print "ERROR: Could not read " + file
            return

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


    ## Search through gptl timing files
    #
    #
    def parseTimingSummaries(self, basePath):
        dycores = ["glide", "glissade"] #, "glam", "albany", "bisicles"]
        timingSummary = dict()

        for dycore in dycores:
            timingDetails = dict()
            veloDriverList, diagSolveList, simpleGlideList, ioWriteList = [], [], [], []

            # Find all of the timing files
            regex = re.compile("out.*." + dycore + ".timing.*")
            subDirs = filter(regex.search, os.listdir(basePath))
            nTimingFiles = 0
            for dir in subDirs:
                if "cism_timing_stats" in os.listdir(basePath + os.sep + dir):
                    nTimingFiles += 1


            # Make sure that there are enough files to parse 
            if nTimingFiles < 9:
                print("        Could not generate " + dycore + " timing summary.  Need to have at least 10 samples, but only found " + str(len(subDirs)) + "!")
                # Build the output data-structure
                timingDetails['Simple Glide'] = None
                timingDetails['Velocity Driver'] = None
                timingDetails['Initial Diagonal Solve'] = None
                timingDetails['IO Writeback'] = None
                timingSummary[dycore] = timingDetails
            else: 
                # Go through each subdirectory and parse the cism_timing_stats file
                for dir in subDirs:
                    # Tell the user if the file doesn't exist
                    if not os.path.exists(basePath + os.sep + dir + os.sep + "cism_timing_stats"):
                        timingDetails[basePath + os.sep + dir + os.sep + "cism_timing_stats"] = None
                        print("    Could not find timing summary for " + dir)
                    else:
                        timingFile = open(basePath + os.sep + dir + os.sep + "cism_timing_stats", 'r')
                        timingHeaders = []
                        for line in timingFile:
                            if line.startswith("name"):
                                timingHeaders = line.replace('(','').replace(')','').split()
                            elif "cism" in line:
                                splitLine = line.split()
                                simpleGlideList.append(float(splitLine[5]))
                            elif "initial_diag_var_solve" in line:
                                splitLine = line.split()
                                diagSolveList.append(float(splitLine[5]))
                            elif "_velo_driver" in line:
                                splitLine = line.split()
                                veloDriverList.append(float(splitLine[5]))
                            elif "io_writeall" in line:
                                splitLine = line.split()
                                ioWriteList.append(float(splitLine[5]))

                # Make sure that something is in the lists so that data can be calculated
                lists = [veloDriverList, diagSolveList, simpleGlideList, ioWriteList]
                for list in lists:
                    if len(list) == 0: list.append(0)

                # Build the output data-structure
                timingDetails['Simple Glide'] = [mean(simpleGlideList), min(simpleGlideList), max(simpleGlideList)]
                timingDetails['Velocity Driver'] = [mean(veloDriverList), min(veloDriverList), max(veloDriverList)]
                timingDetails['Initial Diagonal Solve'] = [mean(diagSolveList), min(diagSolveList), max(diagSolveList)]
                timingDetails['IO Writeback'] = [mean(ioWriteList), min(ioWriteList), max(ioWriteList)]
                timingSummary[dycore] = timingDetails

                # Print out a table with average, min, and max of the variables
                print ""
                print "                    \tAvg \t\t Min \t\t Max"
                print("                    --------------------------------------------------")
                print "          SimGlide  | {:15} | {:15} | {:15}".format(str(mean(simpleGlideList)), str(min(simpleGlideList)), str(max(simpleGlideList)))
                print "          VelDrive  | {:15} | {:15} | {:15}".format(str(mean(veloDriverList)), str(min(veloDriverList)), str(max(veloDriverList)))
                print "          DiagSolv  | {:15} | {:15} | {:15}".format(str(mean(diagSolveList)), str(min(diagSolveList)), str(max(diagSolveList)))
                print "          ioWrite   | {:15} | {:15} | {:15}".format(str(mean(ioWriteList)), str(min(ioWriteList)), str(max(ioWriteList)))
                print ""

        return timingSummary
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
import fnmatch
import ConfigParser

import util.variables
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

        # Build an empty ordered dictionary so that the output prints in a nice order
        self.stdOutData = OrderedDict()
        for var in util.variables.parserVars: self.stdOutData[var] = None

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
    def parseConfigurations(self, modelDir, benchDir, regex):
        # Make sure the locations exist, and if not return blank sets
        if not (os.path.exists(modelDir) and os.path.exists(benchDir)):
            return dict(), dict()

        # Pull the files, while filtering out "hidden" ones
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
    #    @param stdOutData: a mapping of the various parameters to
    #      their values from the file
    #
    def parseStdOutput(self, modelDir, regex):
        # Set up variables that we can use to map data and information
        dycoreTypes = {"0" : "Glide", "1" : "Glam", "2" : "Glissade", "3" : "AlbanyFelix", "4" : "BISICLES"}


        # Scrape the details from each of the files and store some data for later
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


    ## Search through gptl timing files
    #
    def parseTimingSummaries(self, basePath):
        timingSummary = dict()
        if not os.path.exists(basePath):
            return timingSummary

        for dycore in util.variables.dycores:
            timingDetails = dict()
            veloDriverList, diagSolveList, simpleGlideList, ioWriteList = [], [], [], []
            numberProcessors = 0

            # Find all of the timing files
            regex = re.compile("out.*." + dycore + ".timing..*")
            if os.path.exists(basePath):
                subDirs = filter(regex.search, os.listdir(basePath))
            else:
                subDirs = []
            nTimingFiles = 0
            for dir in subDirs:
                if "cism_timing_stats" in os.listdir(basePath + os.sep + dir):
                    nTimingFiles += 1


            # Make sure that there are enough files to parse 
            if nTimingFiles < 9:
                print("        Could not generate " + dycore + " timing summary.  Need to have at least 10 samples, but only found " + str(nTimingFiles) + "!")
                # Build the output data-structure
                for var in util.variables.timingVars:
                    timingDetails[var] = {}
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
                                simpleGlideList.append(float(splitLine[4]))                                
                            elif "simple glide" in line:
                                splitLine = line.split()
                                numberProcessors = int(splitLine[2])
                                simpleGlideList.append(float(splitLine[5]))
                            elif "initial_diag_var_solve" in line:
                                splitLine = line.split()
                                diagSolveList.append(float(splitLine[4]))
                            elif "_velo_driver" in line:
                                splitLine = line.split()
                                veloDriverList.append(float(splitLine[4]))
                            elif "io_writeall" in line:
                                splitLine = line.split()
                                ioWriteList.append(float(splitLine[4]))

                
                # Scale the times to be per processor
                for list in [veloDriverList, diagSolveList, simpleGlideList, ioWriteList]:
                    list[:] = [x/numberProcessors for x in list]
                
                # Make sure that something is in the lists so that data can be calculated
                lists = [veloDriverList, diagSolveList, simpleGlideList, ioWriteList]
                for list in lists:
                    if len(list) == 0: list.append(0)

                # Build the output data-structure
                timingDetails['Processor Count'] = numberProcessors
                timingDetails['Simple Glide'] = [mean(simpleGlideList), min(simpleGlideList), max(simpleGlideList)]
                timingDetails['Velocity Driver'] = [mean(veloDriverList), min(veloDriverList), max(veloDriverList)]
                timingDetails['Initial Diagonal Solve'] = [mean(diagSolveList), min(diagSolveList), max(diagSolveList)]
                timingDetails['IO Writeback'] = [mean(ioWriteList), min(ioWriteList), max(ioWriteList)]
                timingSummary[dycore] = timingDetails

                # Print out a table with average, min, and max of the variables
                print "          Dycore: " + dycore
                print "          Number of processors: " + str(numberProcessors)
                print "                    \tAvg \t\t Min \t\t Max"
                print("                    --------------------------------------------------")
                print "          SimGlide  | {:15} | {:15} | {:15}".format(str(mean(simpleGlideList)), str(min(simpleGlideList)), str(max(simpleGlideList)))
                print "          VelDrive  | {:15} | {:15} | {:15}".format(str(mean(veloDriverList)), str(min(veloDriverList)), str(max(veloDriverList)))
                print "          DiagSolv  | {:15} | {:15} | {:15}".format(str(mean(diagSolveList)), str(min(diagSolveList)), str(max(diagSolveList)))
                print "          ioWrite   | {:15} | {:15} | {:15}".format(str(mean(ioWriteList)), str(min(ioWriteList)), str(max(ioWriteList)))
                print ""

        return timingSummary

'''
Master module for performance test cases

Created on Dec 8, 2014

@author: arbennett
'''

import re
import os
import sys
import itertools

import livv
from bin.VV_test import AbstractTest
from bin.VV_dome import Dome
from bin.VV_gis import Gis
from bin.VV_parser import Parser

## Main class for handling performance test cases.
#
#  The performance test cases inherit functionality from AbstractTest for checking
#  bit-for-bittedness as well as for parsing standard output from a model run.
#
class Performance(AbstractTest):

    ## Constructor
    #
    def __init__(self):
        super(self.__class__, self).__init__()

        # Describe what the dome tests are all about
        self.name = "performance"
        self.description = "Tests the performance of various test cases." 


    ## Returns the name of the test
    #
    #  output:
    #    @returns name : performance
    #
    def getName(self):
        return self.name


    ## Runs the performance specific test case.
    #
    #  When running a test this call will record the specific test case
    #  being run.  Each specific test case string is mapped to the
    #  method that will be used to run the actual test case.
    #
    #  input:
    #    @param testCase : the string indicator of the test to run
    #
    def run(self, testCase):
        # Common run     
        self.testsRun.append(testCase)

        # Map the case names to the case functions
        splitCase = ["".join(x) for _, x in itertools.groupby(testCase, key=str.isdigit)]
        perfType = splitCase[0]
        resolution = "".join(splitCase[1:])
        callDict = {'dome' : self.runDomePerformance,
                    'gis_' : self.runGisPerformance}

        # Call the correct function
        if callDict.has_key(perfType):
            callDict[perfType](resolution)
        else: 
            print("  Could not find test code for performance test: " + testCase)

        # More common postprocessing
        return


    #
    #  DUMMY METHODS FOLLOW
    #
    def runDomePerformance(self, resolution):
        print("  Dome " + resolution + " performance tests in progress....")  

        # Search for the std output files
        perfDir = livv.performanceDir + os.sep + "dome" + resolution + os.sep + livv.dataDir 
        perfBenchDir = livv.performanceDir + os.sep + "bench" + os.sep + "dome" + resolution + os.sep + livv.dataDir
        files = os.listdir(perfDir)
        test = re.compile("^out." + resolution + ".((glide)|(glissade))$")
        files = filter(test.search, files)

        # Process the configure files
        configPath = os.sep + ".." + os.sep + "configure_files"
        domeParser = Parser()
        self.modelConfigs['dome' + resolution], self.benchConfigs['dome' + resolution] = \
                domeParser.parseConfigurations(perfDir + configPath, perfBenchDir + configPath)

        # Scrape the details from each of the files and store some data for later
        perfDetails, perfFiles = [], []
        for file in files:
            perfDetails.append(domeParser.parseOutput(perfDir + os.sep +  file))
            perfFiles.append(file)
        self.fileTestDetails["dome" + resolution] = zip(perfFiles, perfDetails)
        self.bitForBitDetails["dome" + resolution]= dict()

        # Go through and pull in the timing data
        domeParser.parseTimingSummaries(perfDir)

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = domeParser.getParserSummary()

        # Create the plots
        numberPlots = 0 #self.plotPerformance(resolution)

        numberBitMatches, numberBitTests = 0, 0

        self.summary['dome' + resolution] = [numberPlots, numberOutputFiles,
                                             numberConfigMatches, numberConfigTests,
                                             numberBitMatches, numberBitTests]

    def runGisPerformance(self, resolution):
        print("  Greenland Ice Sheet " + resolution + " performance  tests in progress....")  

        # Search for the std output files
        perfDir = livv.performanceDir + os.sep + "gis_" + resolution + os.sep + livv.dataDir 
        perfBenchDir = livv.performanceDir + os.sep + "bench" + os.sep + 'gis_' + resolution + os.sep + livv.dataDir
        if os.path.exists(perfDir) and os.path.exists(perfBenchDir):
            files = os.listdir(perfDir)
            test = re.compile("^out.gis." + resolution + ".((albany)|(glissade))$")
            files = filter(test.search, files)            
        else:
            files = []
            print("    Could not find model and benchmark directories for gis_" + resolution +".")

        # Process the configure files
        configPath = os.sep + ".." + os.sep + "configure_files"
        domeParser = Parser()
        self.modelConfigs['gis_' + resolution], self.benchConfigs['gis_' + resolution] = \
                domeParser.parseConfigurations(perfDir + configPath, perfBenchDir + configPath)

        # Scrape the details from each of the files and store some data for later
        perfDetails, perfFiles = [], []
        for file in files:
            perfDetails.append(domeParser.parseOutput(perfDir + os.sep +  file))
            perfFiles.append(file)
        self.fileTestDetails['gis_' + resolution] = zip(perfFiles, perfDetails)

        self.bitForBitDetails['gis_' + resolution]= dict()

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = domeParser.getParserSummary()

        # Create the plots
        numberPlots = 0 #self.plotPerformance(resolution)

        numberBitMatches, numberBitTests = 0, 0

        self.summary['gis_' + resolution] = [numberPlots, numberOutputFiles,
                                             numberConfigMatches, numberConfigTests,
                                             numberBitMatches, numberBitTests]


    def summary(self):
        print("    This is a placeholder....")

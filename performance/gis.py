'''
Master module for dome test cases.  Inherits methods from the AbstractTest
class from the Test module.  Dome specific verification are performed by calling
the run() method, which passes the necessary information to the runDome()
method.

Created on Dec 8, 2014

@author: arbennett
'''

import re
import os
import subprocess
import itertools

# Map of the options to the test cases
cases = {'none' : [],
         'small' : ['gis_4km'],
         'medium' : ['gis_2km'],
         'large' : ['gis_1km'],
         'scaling' : ['gis_4km', 'gis_2km', 'gis_1km', 'scalingGIS']
        }


def choices():
    return list( cases.keys() )

def choose(key):
    return cases[key]


import livv
from base import AbstractTest
from util.parser import Parser

## Main class for handling dome test cases.
#
#  The dome test cases inherit functionality from AbstractTest for checking 
#  bit-for-bittedness as well as for parsing standard output from a model run.
#  This class handles evolving and diagnostic variations of the dome case.
#
class Test(AbstractTest):

    ## Constructor
    #
    def __init__(self):
        super(self.__class__, self).__init__()

        # Describe what the dome verification are all about
        self.name = "gis"
        self.description = "A placeholder description"


    ## Returns the name of the test
    #
    #  output:
    #    @returns name : Dome
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
        # Map the case names to the case functions
        self.testsRun.append(testCase)
        splitCase = ["".join(x) for _, x in itertools.groupby(testCase, key=str.isdigit)]
        if len(splitCase) == 1: 
            splitCase = filter(None, re.split("([A-Z][^A-Z]*)", testCase))
        perfType = splitCase[0]
        resolution = "".join(splitCase[1:])
        callDict = {'gis_' : self.runGisPerformance,
                    'scaling' : self.runScaling}

        # Call the correct function
        if callDict.has_key(perfType):
            callDict[perfType](resolution)
        else: 
            print("  Could not find test code for performance test: " + testCase)



    ## Greenland Ice Sheet Performance Testing
    #
    #  input:
    #    @param resolution : the resolution of the test data
    #
    def runGisPerformance(self, resolution):
        print("")
        print("  Greenland Ice Sheet " + resolution + " performance  verification in progress....")

        # The locations for the data
        perfDir = livv.performanceDir + os.sep + "gis_" + resolution + os.sep + livv.dataDir
        perfBenchDir = livv.performanceDir + os.sep + "bench" + os.sep + 'gis_' + resolution + os.sep + livv.dataDir

        # Make sure that there is some data
        if not (os.path.exists(perfDir) and os.path.exists(perfBenchDir)):
            print("    Could not find data for GIS " + resolution + " verification!  Tried to find data in:")
            print("      " + perfDir)
            print("      " + perfBenchDir)
            print("    Continuing with next test....")
            return 1

        # Search for the std output files
        files = os.listdir(perfDir)
        test = re.compile("^out.gis." + resolution + ".((albany)|(glissade))$")
        files = filter(test.search, files)

        # Process the configure files
        configPath = os.sep + ".." + os.sep + "configure_files"
        gisParser = Parser()
        self.modelConfigs['gis_' + resolution], self.benchConfigs['gis_' + resolution] = \
                gisParser.parseConfigurations(perfDir + configPath, perfBenchDir + configPath)

        # Scrape the details from each of the files and store some data for later
        perfDetails, perfFiles = [], []
        for file in files:
            perfDetails.append(gisParser.parseOutput(perfDir + os.sep +  file))
            perfFiles.append(file)
        self.fileTestDetails['gis_' + resolution] = zip(perfFiles, perfDetails)

        # Go through and pull in the timing data
        print("")
        print("        Model Timing Summary:")
        print("      --------------------------------------------------------------------")
        self.modelTimingData['gis_' + resolution] = gisParser.parseTimingSummaries(perfDir)
        print("")
        print("        Benchmark Timing Summary:")
        print("      --------------------------------------------------------------------")
        self.benchTimingData['gis_' + resolution] = gisParser.parseTimingSummaries(perfBenchDir)

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = gisParser.getParserSummary()

        # Create the plots
        numberPlots = 0 #self.plotPerformance(resolution)

        numberBitMatches, numberBitTests = 0, 0

        self.summary['gis_' + resolution] = [numberPlots, numberOutputFiles,
                                             numberConfigMatches, numberConfigTests,
                                             numberBitMatches, numberBitTests]
        

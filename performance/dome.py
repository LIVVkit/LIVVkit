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
         'small' : ['dome60'],
         'medium' : ['dome120'],
         'large' : ['dome240'],
         'scaling' : ['dome60', 'dome120', 'dome240', 'dome500', 'scalingDome'],
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
        self.name = "dome"
        self.description = "3-D paraboloid dome of ice with a circular, 60 km" + \
                      " diameter base sitting on a flat bed. The horizontal" + \
                      " spatial resolution studies are 2 km, 1 km, 0.5 km" + \
                      " and 0.25 km, and there are 10 vertical levels. For this" + \
                      " set of experiments a quasi no-slip basal condition in" + \
                      " imposed by setting. A zero-flux boundary condition is" + \
                      " applied to the dome margins. "


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
        callDict = {'dome' : self.runDomePerformance,
                    'scaling' : self.runScaling}

        # Call the correct function
        if callDict.has_key(perfType):
            callDict[perfType](resolution)
        else: 
            print("  Could not find test code for performance test: " + testCase)



    ## Dome Performance Testing
    #
    #  input:
    #    @param resolution: the size of the test being analyzed
    #
    def runDomePerformance(self, resolution):
        print("")
        print("  Dome " + resolution + " performance verification in progress....")  

        # Search for the std output files
        perfDir = livv.performanceDir + os.sep + "dome" + resolution + os.sep + livv.dataDir 
        perfBenchDir = livv.performanceDir + os.sep + "bench" + os.sep + "dome" + resolution + os.sep + livv.dataDir

        if not (os.path.exists(perfDir) and os.path.exists(perfBenchDir)):
            print("    Could not find data for Dome " + resolution + " verification!  Tried to find data in:")
            print("      " + perfDir)
            print("      " + perfBenchDir)
            print("    Continuing with next test....")
            return 1

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

        # Go through and pull in the timing data
        print("")
        print("        Model Timing Summary:")
        print("      --------------------------------------------------------------------")
        self.modelTimingData['dome' + resolution] = domeParser.parseTimingSummaries(perfDir)
        print("")
        print("        Benchmark Timing Summary:")
        print("      --------------------------------------------------------------------")
        self.benchTimingData['dome' + resolution] = domeParser.parseTimingSummaries(perfBenchDir)

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = domeParser.getParserSummary()

        # Create the plots
        numberPlots = 0 #self.plotPerformance(resolution)

        numberBitMatches, numberBitTests = 0, 0

        self.summary['dome' + resolution] = [numberPlots, numberOutputFiles,
                                             numberConfigMatches, numberConfigTests,
                                             numberBitMatches, numberBitTests]
        

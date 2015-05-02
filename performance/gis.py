'''
Master module for GIS test cases.  Inherits methods from the AbstractTest
class from the Test module.  GIS specific verification are performed by calling
the run() method, which passes the necessary information to the runGisPerformance()
method.

Created on Dec 8, 2014

@author: arbennett
'''

import re
import os
import glob
import subprocess
import itertools

# Map of the options to the test cases
cases = {'none' : [],
         'dome' : [],
         'gis' : ['gis'],
         'all'  : ['gis']
        }

def choices():
    return list( cases.keys() )

def choose(key):
    return cases[key]


import livv
from base import AbstractTest
from util.parser import Parser

## Main class for handling gis performance validation.
#
#  The dome test cases inherit functionality from AbstractTest for
#  generating scaling plots and generating the output webpage.
#
class Test(AbstractTest):

    ## Constructor
    #
    def __init__(self):
        super(self.__class__, self).__init__()

        # Describe what the dome verification are all about
        self.name = "gis"
        self.description = "A placeholder description"


    ## Runs the performance specific test cases
    #
    #  When running a test this call will record the specific test case
    #  being run.  Each specific test case string is run via the 
    #  runGisPerformance function.  All of the data pulled is then
    #  assimilated via the runScaling method defined in the base class
    #
    def run(self):
        cases = glob.glob(livv.performanceDir + os.sep + "gis_*")

        for case in cases:
            res = re.findall(r'\d+', case)[0]
            self.testsRun.append('gis' + res + 'km')
            self.runGisPerformance(res + 'km')
        
        self.testsRun.append('scaling')
        self.runScaling('gis')
        return


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

        # Process the configure files
        configPath = os.sep + ".." + os.sep + "configure_files"
        gisParser = Parser()
        self.modelConfigs['gis_' + resolution], self.benchConfigs['gis_' + resolution] = \
                gisParser.parseConfigurations(perfDir + configPath, perfBenchDir + configPath)

        # Scrape the details from each of the files and store some data for later
        self.fileTestDetails['gis_' + resolution] = gisParser.parseStdOutput(perfDir, "^out.gis." + resolution + ".((albany)|(glissade))$")

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
        

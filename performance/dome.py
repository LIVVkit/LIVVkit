'''
Master module for dome test cases.  Inherits methods from the AbstractTest
class from the Test module.  Dome specific verification are performed by calling
the run() method, which passes the necessary information to the runDomePerformance()
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
         'gis' : [],
         'dome' : ['dome'],
         'all'  : ['dome']
        }

# Return a list of options
def choices():
    return list( cases.keys() )

# Return the tests associated with an option
def choose(key):
    return cases[key] if cases.has_key(key) else None


import livv
from base import AbstractTest
from util.parser import Parser

## Main class for handling dome performance validation
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
        self.name = "dome"
        self.description = "3-D paraboloid dome of ice with a circular, 60 km" + \
                      " diameter base sitting on a flat bed. The horizontal" + \
                      " spatial resolution studies are 2 km, 1 km, 0.5 km" + \
                      " and 0.25 km, and there are 10 vertical levels. For this" + \
                      " set of experiments a quasi no-slip basal condition in" + \
                      " imposed by setting. A zero-flux boundary condition is" + \
                      " applied to the dome margins. "

    ## Runs the performance specific test cases.
    #
    #  When running a test this call will record the specific test case
    #  being run.  Each specific test case string is run via the 
    #  runDomePerformance function.  All of the data pulled is then
    #  assimilated via the runScaling method defined in the base class
    #
    def run(self):
        cases = glob.glob(livv.performanceDir + os.sep + "dome*")
        
        for case in cases:
            res = re.findall(r'\d+', case)[0]
            self.runDomePerformance(res)
        
        self.testsRun.append('Performance')
        self.runScaling('dome')
        return


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

        # Process the configure files
        configPath = os.sep + ".." + os.sep + "configure_files"
        domeParser = Parser()
        self.modelConfigs['dome' + resolution], self.benchConfigs['dome' + resolution] = \
                domeParser.parseConfigurations(perfDir + configPath, perfBenchDir + configPath)

        # Scrape the details from each of the files and store some data for later
        self.fileTestDetails["dome" + resolution] = domeParser.parseStdOutput(perfDir, "^out." + resolution + ".((glide)|(glissade))$")

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

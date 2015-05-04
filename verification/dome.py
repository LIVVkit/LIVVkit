'''
Master module for dome test cases.  Inherits methods from the AbstractTest
class from the base module.  Dome specific verification is performed by calling
the run() method, which passes the necessary information to the runDome()
method.

Created on Dec 8, 2014

@author: arbennett
'''

import re
import os
import subprocess

from verification.base import AbstractTest
from util.parser import Parser
import util.variables

# # Main class for handling dome test cases.
#
#  The dome test cases inherit functionality from AbstractTest for checking 
#  bit-for-bittedness from a model run. This class handles evolving and \
#  diagnostic variations of the dome case.
#
class Test(AbstractTest):

    # # Constructor
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


    # # Runs the dome specific test case.  
    #
    #  When running a test this call will record the specific test case 
    #  being run.  Each specific test case string is mapped to the 
    #  method that will be used to run the actual test case.
    #
    #  input:
    #    @param testCase : the string indicator of the test to run
    #
    def run(self):
        return

        # Make sure LIVV can find the data
        modelDir = util.variables.inputDir + os.sep + "dome"
        benchDir = util.variables.benchmarkDir + os.sep + "dome"
        if not (os.path.exists(modelDir) and os.path.exists(benchDir)):
            print("    Could not find data for dome" + resolution + " " + type + " verification!  Tried to find data in:")
            print("      " + modelDir)
            print("      " + benchDir)
            print("    Continuing with next test....")
            self.bitForBitDetails['dome' + resolution + os.sep + type] = {'Data not found': ['SKIPPED', '0.0']}
            return 1  # zero returns a problem        
        self.runDome(resolution, type, modelDir, benchDir)


    # # Perform V&V on the evolving dome case
    #
    #  Runs the dome evolving V&V for a given resolution.  First parses through all 
    #  of the standard output files for the given test case, then finishes up by 
    #  doing bit for bit comparisons with the benchmark files.
    #
    #  input:
    #    @param resolution: The resolution of the test cases to look in.
    #                       (eg resolution == 30 -> reg_test/dome30/evolving)
    #    @param type: The type of test case (evolving, diagnostic, etc)
    #    @param modelDir: the location of the model run data
    #    @param benchDir: the location of the benchmark data
    #
    def runDome(self, resolution, type, modelDir, benchDir):
        # Process the configure files
        print("  Dome " + type + " test in progress....")
        configPath = os.sep + ".." + os.sep + "configure_files"
        domeParser = Parser()
        self.modelConfigs['dome' + resolution + os.sep + type], self.benchConfigs['dome' + resolution + os.sep + type] = \
                domeParser.parseConfigurations(modelDir + configPath, benchDir + configPath)

        # Parse standard out
        self.fileTestDetails["dome" + resolution + os.sep + type] = domeParser.parseStdOutput(modelDir,".*((small)|(large))_proc")
        
        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = domeParser.getParserSummary()

        # Create the plots
        numberPlots = 0  # self.plotEvolving(resolution)

        # Run bit for bit test
        numberBitMatches, numberBitTests = 0, 0
        self.bitForBitDetails['dome' + resolution + os.sep + type] = self.bit4bit(self.name, modelDir, benchDir)
        for key, value in self.bitForBitDetails['dome' + resolution + os.sep + type].iteritems():
            print ("    {:<40} {:<10}".format(key, value[0]))
            if value[0] == "SUCCESS": numberBitMatches += 1
            numberBitTests += 1

        self.summary['dome' + resolution + os.sep + type] = [numberPlots, numberOutputFiles,
                                                             numberConfigMatches, numberConfigTests,
                                                             numberBitMatches, numberBitTests]

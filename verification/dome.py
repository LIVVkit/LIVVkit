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
import glob
import subprocess

from verification.base import AbstractTest
from util.parser import Parser
import util.variables

## Main class for handling dome test cases.
#
#  The dome test cases inherit functionality from AbstractTest for checking 
#  bit-for-bittedness from a model run. This class handles evolving and \
#  diagnostic variations of the dome case.
#
class Test(AbstractTest):

    ## Constructor
    def __init__(self):
        super(self.__class__, self).__init__()
        self.name = "Dome"
        self.description = "3-D paraboloid dome of ice with a circular, 60 km" + \
                      " diameter base sitting on a flat bed. The horizontal" + \
                      " spatial resolution studies are 2 km, 1 km, 0.5 km" + \
                      " and 0.25 km, and there are 10 vertical levels. For this" + \
                      " set of experiments a quasi no-slip basal condition in" + \
                      " imposed by setting. A zero-flux boundary condition is" + \
                      " applied to the dome margins. "


    ## Runs the dome specific test case.  
    #
    #  TODO: Write new documentation
    #
    def run(self):
        # Make sure LIVV can find the data
        modelDir = util.variables.inputDir + os.sep + "dome"
        benchDir = util.variables.benchmarkDir + os.sep + "dome"
        if not (os.path.exists(modelDir) and os.path.exists(benchDir)):
            print("    Could not find data for dome" + resolution + " " + type + " verification!  Tried to find data in:")
            print("      " + modelDir)
            print("      " + benchDir)
            print("    Continuing with next test....")
            return

        resolutions = sorted(set(fn.split('.')[1] for fn in os.listdir(modelDir)))
        self.runDome(resolutions[0], modelDir, benchDir)
        self.testsRun.append("Dome " + resolutions[0])


    ## Perform V&V on the evolving dome case
    #
    #  Runs the dome evolving V&V for a given resolution.  First parses through all 
    #  of the standard output files for the given test case, then finishes up by 
    #  doing bit for bit comparisons with the benchmark files.
    #
    #  input:
    #    @param resolution: The resolution of the test cases to look in.
    #                       (eg resolution == 30 -> reg_test/dome30/evolving)
    #    @param modelDir: the location of the model run data
    #    @param benchDir: the location of the benchmark data
    #
    def runDome(self, resolution, modelDir, benchDir):
        # Process the configure files
        print("  Dome " + resolution + " test in progress....")
        domeParser = Parser()
        self.modelConfigs['Dome ' + resolution], self.benchConfigs['Dome ' + resolution] = \
                domeParser.parseConfigurations(modelDir, benchDir, "*" + resolution + ".config")

        # Parse standard out
        self.fileTestDetails["Dome " + resolution] = domeParser.parseStdOutput(modelDir,"dome." + resolution + ".config.oe")

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = domeParser.getParserSummary()

        # Run bit for bit test
        numberBitMatches, numberBitTests = 0, 0
        self.bitForBitDetails['Dome ' + resolution] = self.bit4bit('dome', modelDir, benchDir, resolution)
        for key, value in self.bitForBitDetails['Dome ' + resolution].iteritems():
            print ("    {:<40} {:<10}".format(key, value[0]))
            if value[0] == "SUCCESS": numberBitMatches += 1
            numberBitTests += 1

        self.summary['Dome ' + resolution] = [numberOutputFiles,
                                             numberConfigMatches, numberConfigTests,
                                             numberBitMatches, numberBitTests]

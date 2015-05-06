'''
Master module for stream test cases.  Inherits methods from the AbstractTest
class from the base module.  Stream specific verification is performed by calling
the run() method, which passes the necessary information to the runStream()
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

## Main class for handling stream test cases.
#
#  The stream test cases inherit functionality from AbstractTest for checking 
#  bit-for-bittedness from a model run. This class handles evolving and \
#  diagnostic variations of the stream case.
#
class Test(AbstractTest):

    ## Constructor
    def __init__(self):
        super(self.__class__, self).__init__()
        self.name = "Stream"
        self.description = "Description of stream"


    ## Runs the stream specific test case.  
    #
    #  TODO: Write new documentation
    #
    def run(self):
        modelDir = util.variables.inputDir + os.sep + "stream"
        benchDir = util.variables.benchmarkDir + os.sep + "stream"
        if not (os.path.exists(modelDir) and os.path.exists(benchDir)):
            print("    Could not find data for stream" + resolution + " " + type + " verification!  Tried to find data in:")
            print("      " + modelDir)
            print("      " + benchDir)
            print("    Continuing with next test....")
            return
        resolutions = sorted(set(fn.split('.')[1] for fn in os.listdir(modelDir)))
        self.runStream(resolutions[0], modelDir, benchDir)
        self.testsRun.append("Stream " + resolutions[0])


    ## Perform V&V on the stream case
    #
    #  Runs the stream evolving V&V for a given resolution.  First parses through all 
    #  of the standard output files for the given test case, then finishes up by 
    #  doing bit for bit comparisons with the benchmark files.
    #
    #  input:
    #    @param resolution: The resolution of the test cases to look in.
    #                       (eg resolution == 30 -> reg_test/stream30/evolving)
    #    @param modelDir: the location of the model run data
    #    @param benchDir: the location of the benchmark data
    #
    def runStream(self, resolution, modelDir, benchDir):
        # Process the configure files
        print("  Stream " + resolution + " test in progress....")
        streamParser = Parser()
        self.modelConfigs['Stream ' + resolution], self.benchConfigs['Stream ' + resolution] = \
                streamParser.parseConfigurations(modelDir, benchDir, "*" + resolution + ".config")

        # Parse standard out
        self.fileTestDetails["Stream " + resolution] = streamParser.parseStdOutput(modelDir,"stream." + resolution + ".config.oe")

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = streamParser.getParserSummary()

        # Run bit for bit test
        numberBitMatches, numberBitTests = 0, 0
        self.bitForBitDetails['Stream ' + resolution] = self.bit4bit('stream', modelDir, benchDir, resolution)
        for key, value in self.bitForBitDetails['Stream ' + resolution].iteritems():
            print ("    {:<40} {:<10}".format(key, value[0]))
            if value[0] == "SUCCESS": numberBitMatches += 1
            numberBitTests += 1

        self.summary['Stream ' + resolution] = [numberOutputFiles,
                                             numberConfigMatches, numberConfigTests,
                                             numberBitMatches, numberBitTests]

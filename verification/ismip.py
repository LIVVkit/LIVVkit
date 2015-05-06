'''
Master module for Ismip verification.  Inherits methods from the AbstractTest
class from the base module.  ISMIP specific verification is performed by calling
the run() method, which passes the necessary information to the runIsmip()
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

## Main class for handling Ismip test cases.
#
#  The Ismip test cases inherit functionality from AbstractTest for checking 
#  bit-for-bittedness and generating webpages with results.
#  This class handles the Ismip-hom a and c verification for resolutions of 20km and 80km.
#
class Test(AbstractTest):

    ## Constructor
    #
    def __init__(self):
        super(self.__class__, self).__init__()

        self.name = "ismip"
        self.description = "The Ice Sheet Model Intercomparison Project for Higher-Order Models (ISMIP-HOM) " + \
                           "prescribes a set of experiments meant to test the implementation of higher-order" + \
                           " physics.  For more information, see <a href=http://homepages.ulb.ac.be/~fpattyn/ismip/>" +\
                           "http://homepages.ulb.ac.be/~fpattyn/ismip/</a> \n" + \
                           " Simulates steady ice flow over a surface with periodic boundary conditions"


    ## Runs the ismip specific test case.
    #
    #  When running a test this call will record the specific test case
    #  being run.  Each specific test case string is mapped to the
    #  method that will be used to run the actual test case.
    #
    #  input:
    #    @param test : the string indicator of the test to run
    #
    def run(self):
        modelDir = util.variables.inputDir + os.sep + 'ismip-hom'
        benchDir = util.variables.benchmarkDir + os.sep + 'ismip-hom'
        if not (os.path.exists(modelDir) and os.path.exists(benchDir)):
            print("    Could not find data for ismip-hom verification!  Tried to find data in:")
            print("      " + modelDir)
            print("      " + benchDir)
            print("    Continuing with next test....")
            return
        testTypes = sorted(set(fn.split('.')[0].split('-')[-1] for fn in os.listdir(modelDir)))
        for test in testTypes:
            resolutions = sorted(set(fn.split(os.sep)[-1].split('.')[1]  \
                            for fn in glob.glob(modelDir + os.sep + 'ismip-hom-' + test + "*")))
            for resolution in resolutions:
                self.runIsmip(modelDir, benchDir, test, resolution)
                self.testsRun.append(test.capitalize() + " " + resolution)


    ## Perform V&V on an ismip-hom test case
    #
    #  Runs the ismip V&V for a given case and resolution.  First parses through all
    #  of the standard output files for the given test case and finishes up by 
    #  doing bit for bit comparisons with the benchmark files.
    #
    #  input:
    #    @param testDir: The path to the test data
    #    @param benchDir: The path to the benchmark data
    #    @param type: Which version of the ismip-hom test should be run
    #    @param resolution: The resolution of the test cases to look in.
    # 
    def runIsmip(self, testDir, benchDir, type, resolution):
        print("  ISMIP-HOM-" + type.capitalize() + " " + resolution + " test in progress....")
        testName = type.capitalize() + " " + resolution

        # Process the configure files
        ismipParser = Parser()
        self.modelConfigs[testName], self.benchConfigs[testName] = \
            ismipParser.parseConfigurations(testDir, benchDir, "ismip-hom-" + type + "." + resolution + ".config")

        # Scrape the details from each of the files and store some data for later
        self.fileTestDetails[testName] = ismipParser.parseStdOutput(testDir, "ismip-hom-" + type + "." + resolution + ".config.oe")

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = ismipParser.getParserSummary()

        # Run bit for bit test
        numberBitTests, numberBitMatches = 0, 0
        self.bitForBitDetails[testName] = self.bit4bit('ismip-hom-' + type, testDir, benchDir, resolution)
        for key, value in self.bitForBitDetails[testName].iteritems():
            print ("    {:<40} {:<10}".format(key,value[0]))
            if value[0] == "SUCCESS": numberBitMatches+=1
            numberBitTests+=1

        # Record the summary
        self.summary[testName] = [numberOutputFiles,
                                  numberConfigMatches, numberConfigTests,
                                  numberBitMatches, numberBitTests]

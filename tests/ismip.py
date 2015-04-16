'''
Master module for Ismip tests.  

Created on Dec 8, 2014

@author: arbennett
'''

import re
import os
import subprocess


cases = {'none'  : [],
         'small' : ['ismip-hom-a/80km', 'ismip-hom-c/80km'],
         'large' : ['ismip-hom-a/20km', 'ismip-hom-c/20km'],
         'all'   : ['ismip-hom-a/20km', 'ismip-hom-c/20km', 'ismip-hom-a/80km', 'ismip-hom-c/80km']}

def choices():
    return list( cases.keys() )

def choose(key):
    return cases[key]


import livv
from tests.test import AbstractTest
from util.parser import Parser

## Main class for handling Ismip test cases.
#
#  The Ismip test cases inherit functionality from AbstractTest for checking 
#  bit-for-bittedness as well as for parsing standard output from a model run.
#  This class handles the Ismip-hom a and c tests for resolutions of 20km and 80km.
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

    ## Return the name of the test
    #
    #  output:
    #    @returns name : ismip
    #
    def getName(self):
        return self.name


    ## Runs the ismip specific test case.
    #
    #  When running a test this call will record the specific test case
    #  being run.  Each specific test case string is mapped to the
    #  method that will be used to run the actual test case.
    #
    #  input:
    #    @param test : the string indicator of the test to run
    #
    def run(self, test):
        # Common run
        self.testsRun.append(test)

        # Make sure LIVV can find the data
        testDir = livv.inputDir + os.sep + test + os.sep + livv.dataDir 
        benchDir = livv.benchmarkDir + os.sep + test + os.sep + livv.dataDir
        if not (os.path.exists(testDir) and os.path.exists(benchDir)):
            print("    Could not find data for " + testDir + " tests!  Tried to find data in:")
            print("      " + testDir)
            print("      " + benchDir)
            print("    Continuing with next test....")
            self.bitForBitDetails[test] = {'Data not found': ['SKIPPED', '0.0']}
            return 1 # zero returns a problem

        # Pull some data about the test case
        splitCase = test.split('/')
        aOrC = splitCase[0][-1]
        resolution = splitCase[-1]

        # Pass it onto the specific run
        self.runIsmip(testDir, benchDir, aOrC, resolution)


    ## Perform V&V on an ismip-hom test case
    #
    #  Runs the ismip V&V for a given case and resolution.  First parses through all
    #  of the standard output files for the given test case, then generates plots via
    #  the plot function.  Finishes up by doing bit for bit comparisons with
    #  the benchmark files.
    #
    #  input:
    #    @param testDir: The path to the test data
    #    @param benchDir: The path to the benchmark data
    #    @param aOrC: Whether we are running ismip-hom-a or ismip-hom-c
    #    @param resolution: The resolution of the test cases to look in.
    #                       (eg resolution == 30 -> reg_test/dome30/diagnostic)
    # 
    def runIsmip(self, testDir, benchDir, aOrC, resolution):
        print("  Ismip-hom-" + aOrC + os.sep + resolution + " test in progress....")
        testName = 'ismip-hom-' + aOrC + os.sep + resolution

        # Process the configure files
        configPath = os.sep + ".." + os.sep + "configure_files"
        ismipParser = Parser()
        self.modelConfigs[testName], self.benchConfigs[testName] = \
            ismipParser.parseConfigurations(testDir + configPath, benchDir + configPath)

        # Scrape the details from each of the files and store some data for later
        test = re.compile(".*out.*[0-9]")
        try:
            files = os.listdir(testDir)
        except:
            print("    Could not find model and benchmark directories for " + testName)
            files = []
        files = filter(test.search, files)
        ismipDetails, ismipFiles = [], []
        for file in files:
            ismipDetails.append(ismipParser.parseOutput(testDir + '/' + file))
            ismipFiles.append(file)
        self.fileTestDetails[testName] = zip(ismipFiles, ismipDetails)

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = ismipParser.getParserSummary()

        # Create the plots & record the number generated
        numberPlots = 0 # self.plot(aOrC,resolution[:2])

        # Run bit for bit test
        numberBitTests, numberBitMatches = 0, 0
        self.bitForBitDetails[testName] = self.bit4bit(os.sep + testName, testDir, benchDir)
        for key, value in self.bitForBitDetails[testName].iteritems():
            print ("    {:<40} {:<10}".format(key,value[0]))
            if value[0] == "SUCCESS": numberBitMatches+=1
            numberBitTests+=1

        # Record the summary
        self.summary[testName] = [numberPlots, numberOutputFiles,
                                  numberConfigMatches, numberConfigTests,
                                  numberBitMatches, numberBitTests]

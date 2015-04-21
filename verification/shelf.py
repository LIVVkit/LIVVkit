'''
Master module for shelf test cases

Created on Dec 8, 2014

@author: arbennett
'''

import re
import os
import subprocess

# the test cases that can be run
cases = {'none' : [],
         'confined' : ['confined-shelf'],
         'circular' : ['circular-shelf'],
         'all' : ['confined-shelf', 'circular-shelf']}

def choices():
    return list( cases.keys() )

def choose(key):
    return cases[key]


import livv
from verification.base import AbstractTest
from util.parser import Parser

# # Main class for handling shelf test cases.
#
#  The shelf test cases inherit functionality from AbstractTest for checking 
#  bit-for-bittedness as well as for parsing standard output from a model run.
#  This class handles the confined and circular variations of the shelf cases.
#
class Test(AbstractTest):

    ## Constructor
    #
    def __init__(self):
        super(self.__class__, self).__init__()

        self.name = "shelf"
        self.description = "A blank description"


    ## Return the name of the test
    #
    #  output:
    #    @returns name : shelf
    #
    def getName(self):
        return self.name


    ## Runs the shelf specific test case.  
    #
    #  When running a test this call will record the specific test case 
    #  being run.
    #
    #  input:
    #    @param test : the string indicator of the test to run
    #
    def run(self, test):
        # Make sure LIVV can find the data
        self.testsRun.append(test)
        testDir = livv.inputDir + os.sep + test + os.sep + livv.dataDir 
        benchDir = livv.benchmarkDir + os.sep + test + os.sep + livv.dataDir 
        if not (os.path.exists(testDir) and os.path.exists(benchDir)):
            print("    Could not find data for " + test + " verification!  Tried to find data in:")
            print("      " + testDir)
            print("      " + benchDir)
            print("    Continuing with next test....")
            self.bitForBitDetails[test] = {'Data not found': ['SKIPPED', '0.0']}
            return 1 # zero returns a problem
        self.runShelf(test, testDir, benchDir)


    ## Perform V&V on the a shelf case
    #
    #  input:
    #    @param type: The type of shelf test (circular, confined, etc)
    #    @param testDir: The path to the test data
    #    @param benchDir: The path to the benchmark data
    #
    def runShelf(self, type, testDir, benchDir):
        # Parse the configure files
        print("  " + type + " test in progress....")
        configPath = os.sep + ".." + os.sep + "configure_files"
        shelfParser = Parser()
        self.modelConfigs[type], self.benchConfigs[type] = \
            shelfParser.parseConfigurations(testDir + configPath, benchDir + configPath)

        # Scrape the details from each of the files and store some data for later
        try:
            files = os.listdir(testDir)
        except:
            print("    Could not find model and benchmark directories for " + type)
            files = []
        test = re.compile(type + ".*out.*")
        files = filter(test.search, files)
        shelfFiles, shelfDetails = [], []
        for file in files:
            shelfDetails.append(shelfParser.parseOutput(testDir + "/" + file))
            shelfFiles.append(file)
        self.fileTestDetails[type] = zip(shelfFiles, shelfDetails)

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = shelfParser.getParserSummary()

        # Create the plots
        numberPlots = 0 # self.plotConfined(testDir, benchDir, shelfFiles)

        # Run bit for bit test
        numberBitTests, numberBitMatches = 0, 0
        self.bitForBitDetails[type] = self.bit4bit('/' + type, testDir, benchDir)
        for key, value in self.bitForBitDetails[type].iteritems():
            print ("    {:<40} {:<10}".format(key, value[0]))
            if value[0] == "SUCCESS": numberBitMatches+=1
            numberBitTests+=1

        # Record the summary
        self.summary[type] = [numberPlots, numberOutputFiles,
                              numberConfigMatches, numberConfigTests,
                              numberBitMatches, numberBitTests]

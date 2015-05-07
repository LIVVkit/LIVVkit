'''
Master module for shelf test cases  Inherits methods from the AbstractTest
class from the base module.  Shelf specific verification is performed by calling
the run() method, which gathers & passes the necessary information to the runShelf()
method.

Created on Dec 8, 2014

@author: arbennett
'''
import os
import glob

from verification.base import AbstractTest
from util.parser import Parser
import util.variables

'''
Main class for handling shelf test cases.

The shelf test cases inherit functionality from AbstractTest for checking 
bit-for-bittedness as well as for parsing standard output from a model run.
This class handles the confined and circular variations of the shelf cases.
'''
class Test(AbstractTest):

    ## Constructor
    def __init__(self):
        super(self.__class__, self).__init__()
        self.name = "Shelf"
        self.description = "A blank description"
  
    '''
    Runs all of the available shelf tests.  Looks in the model and
    benchmark directories for different variations, and then runs
    the runShelf() method with the correct information
    '''
    def run(self):
        modelDir = util.variables.inputDir + os.sep + 'shelf'
        benchDir = util.variables.benchmarkDir + os.sep + 'shelf'
        if not (os.path.exists(modelDir) and os.path.exists(benchDir)):
            print("    Could not find data for shelf verification!  Tried to find data in:")
            print("      " + modelDir)
            print("      " + benchDir)
            print("    Continuing with next test....")
            return
        testTypes = sorted(set(fn.split('.')[0].split('-')[-1] for fn in os.listdir(modelDir)))
        for test in testTypes:
            resolutions = sorted(set(fn.split(os.sep)[-1].split('.')[1]  \
                            for fn in glob.glob(modelDir + os.sep + 'shelf-' + test + "*")))
            for resolution in resolutions:
                self.runShelf(test, resolution, modelDir, benchDir)
                self.testsRun.append(test.capitalize() + " " + resolution)

    '''
    Perform verification analysis on the a shelf case
    
     @param type: The type of shelf test (circular, confined, etc)
     @param resolution: The size of the shelf test (0041, 0043, etc)
     @param testDir: The path to the test data
     @param benchDir: The path to the benchmark data
    '''
    def runShelf(self, testCase, resolution, testDir, benchDir):
        print("  " + testCase.capitalize() + " shelf " + resolution + " test in progress....")
        testName = testCase.capitalize() + " " + resolution
        shelfParser = Parser()

        # Parse the configure files
        self.modelConfigs[testName], self.benchConfigs[testName] = \
            shelfParser.parseConfigurations(testDir, benchDir, "shelf-" + testCase + "." + resolution + ".config")

        # Scrape the details from each of the files and store some data for later
        self.fileTestDetails[testName] = shelfParser.parseStdOutput(testDir, "shelf-" + testCase + "." + resolution + ".config.oe")
        numberOutputFiles, numberConfigMatches, numberConfigTests = shelfParser.getParserSummary()

        # Run bit for bit test
        numberBitTests, numberBitMatches = 0, 0
        self.bitForBitDetails[testName] = self.bit4bit('shelf-' + testCase, testDir, benchDir, resolution)
        for key, value in self.bitForBitDetails[testName].iteritems():
            print ("    {:<40} {:<10}".format(key, value[0]))
            if value[0] == "SUCCESS": numberBitMatches+=1
            numberBitTests+=1

        self.summary[testName] = [numberOutputFiles, numberConfigMatches, numberConfigTests,
                                  numberBitMatches, numberBitTests]

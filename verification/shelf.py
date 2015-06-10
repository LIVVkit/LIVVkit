# Copyright (c) 2015, UT-BATTELLE, LLC
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


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
        self.modelDir = util.variables.inputDir + os.sep + 'shelf'
        self.benchDir = util.variables.benchmarkDir + os.sep + 'shelf'
        self.description = "Simulates two shelf conditions, confined and " + \
                            "circular.  The confined shelf is an idealized 500m " + \
                            "ice shelf in a confined, rectangular embayment.  The " + \
                            "circular shelf is a 1000 m thick circular shelf grounded " + \
                            "at the center."
  
    '''
    Runs all of the available shelf tests.  Looks in the model and
    benchmark directories for different variations, and then runs
    the runShelf() method with the correct information
    '''
    def run(self):
        if not (os.path.exists(self.modelDir) and os.path.exists(self.benchDir)):
            print("    Could not find data for shelf verification!  Tried to find data in:")
            print("      " + self.modelDir)
            print("      " + self.benchDir)
            print("    Continuing with next test....")
            return
        testTypes = sorted(set(fn.split('.')[0].split('-')[-1] for fn in os.listdir(self.modelDir)))
        for test in testTypes:
            resolutions = sorted(set(fn.split(os.sep)[-1].split('.')[1]  \
                            for fn in glob.glob(self.modelDir + os.sep + 'shelf-' + test + "*.config")))
            for resolution in resolutions:
                self.runShelf(test, resolution, self.modelDir, self.benchDir)
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
            shelfParser.parseConfigurations(testDir, benchDir, "shelf-" + testCase + "." + resolution + ".*.config")

        # Scrape the details from each of the files and store some data for later
        self.fileTestDetails[testName] = shelfParser.parseStdOutput(testDir, "shelf-" + testCase + "." + resolution + ".*.config.oe")
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

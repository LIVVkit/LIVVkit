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
Master module for ISMIP verification.  Inherits methods from the AbstractTest
class from the base module.  ISMIP specific verification is performed by calling
the run() method, which gathers and passes the necessary information to the 
runIsmip() method.

Created on Dec 8, 2014

@author: arbennett
'''

import os
import glob

from verification.base import AbstractTest
from util.parser import Parser
import util.variables

def getName(): return "Ismip"

'''
Main class for handling Ismip test cases.

The Ismip test cases inherit functionality from AbstractTest for checking 
bit-for-bittedness and generating webpages with results.
'''
class Test(AbstractTest):

    ''' Constructor '''
    def __init__(self):
        super(self.__class__, self).__init__()
        self.name = "ismip"
        self.modelDir = util.variables.inputDir + os.sep + 'ismip-hom'
        self.benchDir = util.variables.benchmarkDir + os.sep + 'ismip-hom'
        self.description = "The Ice Sheet Model Intercomparison Project for Higher-Order Models (ISMIP-HOM) " + \
                           "prescribes a set of experiments meant to test the implementation of higher-order" + \
                           " physics.  For more information, see <a href=http://homepages.ulb.ac.be/~fpattyn/ismip/>" +\
                           "http://homepages.ulb.ac.be/~fpattyn/ismip/</a> \n" + \
                           " Simulates steady ice flow over a surface with periodic boundary conditions"

    '''
    Runs all of the available ISMIP tests.  Looks in the model and
    benchmark directories for different variations, and then runs
    the runIsmip() method with the correct information
    '''
    def run(self, verSummary, output):
        if not (os.path.exists(self.modelDir) and os.path.exists(self.benchDir)):
            output.put("    Could not find data for ismip-hom verification!  Tried to find data in:")
            output.put("      " + self.modelDir)
            output.put("      " + self.benchDir)
            output.put("    Continuing with next test....")
            return
        testTypes = sorted(set(fn.split('.')[0].split('-')[-1] for fn in os.listdir(self.modelDir)))
        for test in testTypes:
            resolutions = sorted(set(fn.split(os.sep)[-1].split('.')[1]  \
                            for fn in glob.glob(self.modelDir + os.sep + 'ismip-hom-' + test + "*.config")))
            for resolution in resolutions:
                self.runIsmip(test, resolution, self.modelDir, self.benchDir, output)
                self.testsRun.append(test.capitalize() + " " + resolution)
        verSummary[self.name.lower()] = self.summary
        output.put("")
    
    '''
    Runs the ismip V&V for a given case and resolution.  First parses through all
    of the standard output  & config files for the given test case and finishes up by 
    doing bit for bit comparisons with the benchmark files.

    @param type: Which version of the ismip-hom test should be run
    @param resolution: The resolution of the test cases to look in.    
    @param testDir: The path to the test data
    @param benchDir: The path to the benchmark data
    '''
    def runIsmip(self, testCase, resolution, testDir, benchDir, output):
        output.put("  ISMIP-HOM-" + testCase.capitalize() + " " + resolution + " test in progress....")
        testName = testCase.capitalize() + " " + resolution

        # Process the configure files
        ismipParser = Parser()
        self.modelConfigs[testName], self.benchConfigs[testName] = \
            ismipParser.parseConfigurations(testDir, benchDir, "ismip-hom-" + testCase + "." + resolution + ".*.config")

        # Scrape the details from each of the files and store some data for later
        self.fileTestDetails[testName] = ismipParser.parseStdOutput(testDir, "ismip-hom-" + testCase + "." + resolution + ".*.config.oe")

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = ismipParser.getParserSummary()

        # Run bit for bit test
        numberBitTests, numberBitMatches = 0, 0
        self.bitForBitDetails[testName] = self.bit4bit('ismip-hom-' + testCase, testDir, benchDir, resolution)
        for key, value in self.bitForBitDetails[testName].iteritems():
            output.put("    {:<40} {:<10}".format(key,value[0]))
            if value[0] == "SUCCESS": numberBitMatches+=1
            numberBitTests+=1

        self.summary[testName] = [numberOutputFiles, numberConfigMatches, numberConfigTests,
                                  numberBitMatches, numberBitTests]

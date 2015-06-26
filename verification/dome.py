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


"""
Master module for dome test cases.  Inherits methods from the AbstractTest
class from the base module.  Dome specific verification is performed by calling
the run() method, which gathers & passes the necessary information to the runDome()
method.

Created on Dec 8, 2014

@author: arbennett
"""
import os
import fnmatch

from verification.base import AbstractTest
from util.parser import Parser
import util.variables

def getName(): return "Dome"

"""
Main class for handling dome verification tests

The dome test cases inherit functionality from AbstractTest for checking 
bit-for-bittedness from a model run. This class handles evolving and \
diagnostic variations of the dome case.
"""
class Test(AbstractTest):

    """ Constructor """
    def __init__(self):
        super(self.__class__, self).__init__()
        self.name = "Dome"
        self.modelDir = util.variables.inputDir + os.sep + "dome"
        self.benchDir = util.variables.benchmarkDir + os.sep + "dome"
        self.description = "3-D paraboloid dome of ice with a circular, 60 km" + \
                      " diameter base sitting on a flat bed.  For this" + \
                      " set of experiments a quasi no-slip basal condition in" + \
                      " imposed by setting. A zero-flux boundary condition is" + \
                      " applied to the dome margins. "

    """
    Runs all of the available dome tests.  Looks in the model and
    benchmark directories for different variations, and then runs
    the runDome() method with the correct information
    """
    def run(self, verSummary, output):

        if not (os.path.exists(self.modelDir) and os.path.exists(self.benchDir)):
            output.put("    Could not find data for dome verification!  Tried to find data in:")
            output.put("      " + self.modelDir)
            output.put("      " + self.benchDir)
            output.put("    Continuing with next test....")
            return
        resolutions = set()
        modelConfigFiles = fnmatch.filter(os.listdir(self.modelDir), 'dome*.config')
        for mcf in modelConfigFiles:
            resolutions.add( mcf.split('.')[1] )
        resolutions = sorted( resolutions )
        
        for res in resolutions:
            self.runDome(res, self.modelDir, self.benchDir, output)
            self.testsRun.append("Dome " + res)
        self.generate()
        verSummary[self.name.lower()] = self.summary
        output.put("")

    """
    Runs the dome V&V for a given resolution.  First parses through all 
    of the standard output & config files for the given test case, then finishes up by 
    doing bit for bit comparisons with the benchmark files.
    
    @param resolution: The resolution of the test cases to look in.
    @param modelDir: the location of the model run data
    @param benchDir: the location of the benchmark data
    """
    def runDome(self, resolution, modelDir, benchDir, output):
        output.put("  Dome " + resolution + " test in progress....")
        domeParser = Parser()
        
        # Process the configure files
        self.modelConfigs['Dome ' + resolution], self.benchConfigs['Dome ' + resolution] = \
                domeParser.parseConfigurations(modelDir, benchDir, "*" + resolution + ".*.config")

        # Parse standard out
        self.fileTestDetails["Dome " + resolution] = domeParser.parseStdOutput(modelDir,"dome." + resolution + ".*.config.oe")

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = domeParser.getParserSummary()

        # Run bit for bit test
        numberBitMatches, numberBitTests = 0, 0
        self.bitForBitDetails['Dome ' + resolution] = self.bit4bit('dome', modelDir, benchDir, resolution)
        for key, value in self.bitForBitDetails['Dome ' + resolution].iteritems():
            output.put("    {:<40} {:<10}".format(key, value[0]))
            if value[0] == "SUCCESS": numberBitMatches += 1
            numberBitTests += 1

        self.summary['Dome ' + resolution] = [numberOutputFiles, numberConfigMatches, numberConfigTests,
                                              numberBitMatches, numberBitTests]

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
Master module for dome performance test cases.  Inherits methods from the Abstract_test
class from the Test module.  Dome specific performance tests are performed by calling
the run() method, which passes the necessary information to the run_domePerformance()
method.

Created on Dec 8, 2014

@author: arbennett
"""
import os
import fnmatch

from performance.base import AbstractTest
from util.parser import Parser
import util.variables

def get_name():  return "Dome"


class Test(AbstractTest):
    """
    Main class for handling dome performance validation
    
    The dome test cases inherit functionality from Abstract_test for
    generating scaling plots and generating the output webpage.
    """

    def __init__(self):
        """ Constructor """
        super(self.__class__, self).__init__()
        self.name = "Dome"
        self.model_dir = util.variables.input_dir + os.sep + "dome"
        self.bench_dir = util.variables.benchmark_dir + os.sep + "dome"
        self.description = "3-D paraboloid dome of ice with a circular, 60 km" + \
                      " diameter base sitting on a flat bed. The horizontal" + \
                      " spatial resolution studies are 2 km, 1 km, 0.5 km" + \
                      " and 0.25 km, and there are 10 vertical levels. For this" + \
                      " set of experiments a quasi no-slip basal condition in" + \
                      " imposed by setting. A zero-flux boundary condition is" + \
                      " applied to the dome margins. "


    def run(self):
        """
        Runs the performance specific test cases.
        
        When running a test this call will record the specific test case
        being run.  Each specific test case string is run via the 
        run_domePerformance function.  All of the data pulled is then
        assimilated via the run_scaling method defined in the base class
        """
        if not (os.path.exists(self.model_dir) and os.path.exists(self.bench_dir)):
            print("    Could not find data for dome verification!  Tried to find data in:")
            print("      " + self.model_dir)
            print("      " + self.bench_dir)
            print("    Continuing with next test....")
            return
        resolutions = set()
        model_configFiles = fnmatch.filter(os.listdir(self.model_dir), 'dome*.config')
        for mcf in model_configFiles:
            resolutions.add( mcf.split('.')[1] )
        resolutions = sorted( resolutions )
        
        for resolution in resolutions:
            self.run_dome(resolution, self.model_dir, self.bench_dir)
            #self.tests_run.append("Dome " + resolution)
        self.run_scaling('dome', resolutions)
        self.tests_run.append('Scaling')


    def run_dome(self, resolution, perf_dir, perf_benchDir):
        """
        Run an instance of dome performance testing
        
        Args:
            resolution: the size of the test being analyzed
            perf_dir: the location of the performance data
            perf_benchDir: the location of the benchmark performance data
        """
        print("  Dome " + resolution + " performance testing in progress....")

        # Process the configure files
        dome_parser = Parser()
        self.model_configs['Dome ' + resolution], self.bench_configs['Dome ' + resolution] = \
                dome_parser.parse_configurations(perf_dir, perf_benchDir, "*" + resolution + "*.config")

        # Scrape the details from each of the files and store some data for later
        self.file_testDetails["Dome " + resolution] = dome_parser.parse_stdOutput(perf_dir, "dome." + resolution + ".*.config.oe")

        # Go through and pull in the timing data
        self.model_timingData['dome' + resolution] = dome_parser.parse_timingSummaries(perf_dir, 'dome', resolution)
        self.bench_timingData['dome' + resolution] = dome_parser.parse_timingSummaries(perf_benchDir, 'dome', resolution)

        # Record the data from the parser
        number_outputFiles, number_configMatches, number_configTests = dome_parser.get_parserSummary()

        self.summary['dome' + resolution] = [number_outputFiles, number_configMatches, number_configTests]

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
Master module for shelf test cases  Inherits methods from the Abstract_test
class from the base module.  Shelf specific verification is performed by calling
the run() method, which gathers & passes the necessary information to the run_shelf()
method.

Created on Dec 8, 2014

@author: arbennett
"""
import os
import glob

from verification.base import AbstractTest
from util.parser import Parser
import util.variables

def get_name(): return "Shelf"

class Test(AbstractTest):
    """
    Main class for handling shelf test cases.
    
    The shelf test cases inherit functionality from Abstract_test for checking 
    bit-for-bittedness as well as for parsing standard output from a model run.
    This class handles the confined and circular variations of the shelf cases.
    """

    def __init__(self):
        """ Constructor """
        super(self.__class__, self).__init__()
        self.name = "Shelf"
        self.model_dir = util.variables.input_dir + os.sep + 'shelf'
        self.bench_dir = util.variables.benchmark_dir + os.sep + 'shelf'
        self.description = "Simulates two shelf conditions, confined and " + \
                            "circular.  The confined shelf is an idealized 500m " + \
                            "ice shelf in a confined, rectangular embayment.  The " + \
                            "circular shelf is a 1000 m thick circular shelf grounded " + \
                            "at the center."
  

    def run(self, ver_summary, output):
        """
        Runs all of the available shelf tests.  Looks in the model and
        benchmark directories for different variations, and then runs
        the run_shelf() method with the correct information.
        
        Args:
            ver_summary: multiprocessing dict to store summaries for each run
            output: multiprocessing queue to store information to print to stdout
        """
        if not (os.path.exists(self.model_dir) and os.path.exists(self.bench_dir)):
            output.put("    Could not find data for shelf verification!  Tried to find data in:")
            output.put("      " + self.model_dir)
            output.put("      " + self.bench_dir)
            output.put("    Continuing with next test....")
            return
        test_types = sorted(set(fn.split('.')[0].split('-')[-1] for fn in os.listdir(self.model_dir)))
        for test in test_types:
            resolutions = sorted(set(fn.split(os.sep)[-1].split('.')[1]  \
                            for fn in glob.glob(self.model_dir + os.sep + 'shelf-' + test + "*.config")))
            for resolution in resolutions:
                self.run_shelf(test, resolution, self.model_dir, self.bench_dir, output)
                self.tests_run.append(test.capitalize() + " " + resolution)
        self.generate()
        ver_summary[self.name.lower()] = self.summary
        output.put("")


    def run_shelf(self, test_case, resolution, test_dir, bench_dir, output):
        """
        Perform verification analysis on the a shelf case
        
        Args:
            test_case: The type of shelf test (circular, confined, etc)
            resolution: The size of the shelf test (0041, 0043, etc)
            test_dir: The path to the test data
            bench_dir: The path to the benchmark data
            output: multiprocessing queue to store information to print to stdout
        """
        output.put("  " + test_case.capitalize() + " shelf " + resolution + " test in progress....")
        test_name = test_case.capitalize() + " " + resolution
        shelf_parser = Parser()

        # Parse the configure files
        self.model_configs[test_name], self.bench_configs[test_name] = \
            shelf_parser.parse_configurations(test_dir, bench_dir, "shelf-" + test_case + "." + resolution + ".*.config")

        # Scrape the details from each of the files and store some data for later
        self.file_testDetails[test_name] = shelf_parser.parse_stdOutput(test_dir, "shelf-" + test_case + "." + resolution + ".*.config.oe")
        number_outputFiles, number_configMatches, number_configTests = shelf_parser.get_parserSummary()

        # Run bit for bit test
        number_bitTests, number_bitMatches = 0, 0
        self.bit_forBit_details[test_name] = self.bit4bit('shelf-' + test_case, test_dir, bench_dir, resolution)
        for key, value in self.bit_forBit_details[test_name].iteritems():
            output.put("    {:<40} {:<10}".format(key, value[0]))
            if value[0] == "SUCCESS": number_bitMatches += 1
            number_bitTests += 1

        self.summary[test_name] = [number_outputFiles, number_configMatches, number_configTests,
                                  number_bitMatches, number_bitTests]

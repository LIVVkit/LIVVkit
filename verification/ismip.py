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
Master module for ISMIP verification.  Inherits methods from the Abstract_test
class from the base module.  ISMIP specific verification is performed by calling
the run() method, which gathers and passes the necessary information to the 
run_ismip() method.

Created on Dec 8, 2014

@author: arbennett
"""

import os
import glob
import fnmatch
import multiprocessing

from verification.base import AbstractTest
from util.parser import Parser
import util.variables

def get_name(): return "Ismip"

class Test(AbstractTest):
    """
    Main class for handling Ismip test cases.
    
    The Ismip test cases inherit functionality from AbstractTest for checking 
    bit-for-bittedness and generating webpages with results.
    """

    def __init__(self):
        """ Constructor """
        super(self.__class__, self).__init__()
        self.name = "ismip"
        self.model_dir = util.variables.input_dir + os.sep + 'ismip-hom'
        self.bench_dir = util.variables.benchmark_dir + os.sep + 'ismip-hom'
        self.description = "The Ice Sheet Model Intercomparison Project for Higher-Order Models (ISMIP-HOM) " + \
                           "prescribes a set of experiments meant to test the implementation of higher-order" + \
                           " physics.  For more information, see <a href=http://homepages.ulb.ac.be/~fpattyn/ismip/>" +\
                           "http://homepages.ulb.ac.be/~fpattyn/ismip/</a> \n" + \
                           " Simulates steady ice flow over a surface with periodic boundary conditions"


    def run(self, ver_summary, output):
        """
        Runs all of the available ISMIP tests.  Looks in the model and
        benchmark directories for different variations, and then runs
        the run_ismip() method with the correct information
                
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
        test_types = sorted(set('.'.join(fn.split('-')[-1].split('.')[0:2]) for fn in fnmatch.filter(os.listdir(self.model_dir), 'ismip-hom-*')))
        self.tests_run = [" ".join(test.capitalize().split('.')) for test in test_types] 

        process_handles = [multiprocessing.Process(target=self.run_ismip, args=(tt,self.model_dir,self.bench_dir,output)) for tt in test_types]
        
        for p in process_handles:
            p.start()

        for p in process_handles:
            p.join()
        
        self.convert_dicts()
        self.generate()
        ver_summary[self.name.lower()] = self.summary
    

    def run_ismip(self, test_case, test_dir, bench_dir, output):
        """
        Runs the ismip V&V for a given case and resolution.  First parses through all
        of the standard output  & config files for the given test case and finishes up by 
        doing bit for bit comparisons with the benchmark files.
    
        Args:
            test_case: Which version of the ismip-hom test should be run
            resolution: The resolution of the test cases to look in.    
            test_dir: The path to the test data
            bench_dir: The path to the benchmark data
            output: multiprocessing queue to store information to print to stdout
        """
        test_name = " ".join(test_case.capitalize().split('.'))

        # Process the configure files
        ismip_parser = Parser()
        self.test_configs[test_name], self.bench_configs[test_name] = \
            ismip_parser.parse_configurations(test_dir, bench_dir, "ismip-hom-" + test_case + ".*.config")

        # Scrape the details from each of the files and store some data for later
        self.test_details[test_name] = ismip_parser.parse_std_output(test_dir, "ismip-hom-" + test_case + ".*.config.oe")
        self.bench_details[test_name] = ismip_parser.parse_std_output(bench_dir, "ismip-hom-" + test_case + ".*.config.oe")

        # Record the data from the parser
        number_outputFiles, number_configMatches, number_configTests = ismip_parser.get_parserSummary()

        # Run bit for bit test
        number_bitTests, number_bitMatches = 0, 0
        self.bit_for_bit_details[test_name] = self.bit4bit('ismip-hom-' + test_case.split('.')[0], test_dir, bench_dir, test_case.split('.')[-1])
        for key, value in self.bit_for_bit_details[test_name].iteritems():
            if value[0] == "SUCCESS": number_bitMatches+=1
            number_bitTests+=1

        self.summary[test_name] = [number_outputFiles, number_configMatches, number_configTests,
                                  number_bitMatches, number_bitTests]

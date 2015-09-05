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
Master module for dome test cases.  Inherits methods from the Abstract_test
class from the base module.  Dome specific verification is performed by calling
the run() method, which gathers & passes the necessary information to the run_dome()
method.

Created on Dec 8, 2014

@author: arbennett
"""
import os
import fnmatch
import multiprocessing

from verification.base import AbstractTest
from util.parser import Parser
import util.variables

def get_name(): return "Dome"


class Test(AbstractTest):
    """
    Main class for handling dome verification tests
    
    The dome test cases inherit functionality from AbstractTest for checking 
    bit-for-bittedness from a model run. This class handles evolving and \
    diagnostic variations of the dome case.
    """
    
    def __init__(self):
        """ Constructor """
        super(self.__class__, self).__init__()
        self.name = "Dome"
        self.model_dir = util.variables.input_dir + os.sep + "dome"
        self.bench_dir = util.variables.benchmark_dir + os.sep + "dome"
        self.description = "3-D paraboloid dome of ice with a circular, 60 km" + \
                      " diameter base sitting on a flat bed.  For this" + \
                      " set of experiments a quasi no-slip basal condition in" + \
                      " imposed by setting. A zero-flux boundary condition is" + \
                      " applied to the dome margins. "


    def run(self, ver_summary, output):
        """
        Runs all of the available dome tests.  Looks in the model and
        benchmark directories for different variations, and then runs
        the run_dome() method with the correct information
        
        Args:
            ver_summary: multiprocessing dict to store summaries for each run
            output: multiprocessing queue to store information to print to stdout
        """
        if not (os.path.exists(self.model_dir) and os.path.exists(self.bench_dir)):
            output.put("    Could not find data for dome verification!  Tried to find data in:")
            output.put("      " + self.model_dir)
            output.put("      " + self.bench_dir)
            output.put("    Continuing with next test....")
            return
        resolutions = set()
        model_configFiles = fnmatch.filter(os.listdir(self.model_dir), 'dome*.config')
        for mcf in model_configFiles:
            resolutions.add( mcf.split('.')[1] )
        resolutions = sorted( resolutions )
        
        self.tests_run = ["Dome " + res for res in resolutions]
        process_handles = [multiprocessing.Process(target=self.run_dome, args=(res,self.model_dir,self.bench_dir,output)) for res in resolutions]
        
        for p in process_handles:
            p.start()

        for p in process_handles:
            p.join()
        
        self.convert_dicts()
        self.generate()
        ver_summary[self.name.lower()] = self.summary


    def run_dome(self, resolution, model_dir, bench_dir, output):
        """
        Runs the dome V&V for a given resolution.  First parses through all 
        of the standard output & config files for the given test case, then finishes up by 
        doing bit for bit comparisons with the benchmark files.
        
        Args:
            resolution: The resolution of the test cases to look in.
            model_dir: the location of the model run data
            bench_dir: the location of the benchmark data
            output: multiprocessing queue to store information to print to stdout
        """
        dome_parser = Parser()
        
        # Process the configure files
        self.test_configs['Dome ' + resolution], self.bench_configs['Dome ' + resolution] = \
                dome_parser.parse_configurations(model_dir, bench_dir, "*" + resolution + ".*.config")

        # Parse standard out
        self.test_details["Dome " + resolution] = dome_parser.parse_std_output(model_dir,"dome." + resolution + ".*.config.oe")
        self.bench_details["Dome " + resolution] = dome_parser.parse_std_output(bench_dir,"dome." + resolution + ".*.config.oe")      

        # Record the data from the parser
        number_outputFiles, number_configMatches, number_configTests = dome_parser.get_parserSummary()

        # Run bit for bit test
        number_bitMatches, number_bitTests = 0, 0
        self.bit_for_bit_details['Dome ' + resolution] = self.bit4bit('dome', model_dir, bench_dir, resolution)
        for key, value in self.bit_for_bit_details['Dome ' + resolution].iteritems():
            if value[0] == "SUCCESS": number_bitMatches += 1
            number_bitTests += 1

        self.summary['Dome ' + resolution] = [number_outputFiles, number_configMatches, number_configTests,
                                              number_bitMatches, number_bitTests]

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
Master module for stream test cases.  Inherits methods from the Abstract_test
class from the base module.  Stream specific verification is performed by calling
the run() method, which gathers & passes the necessary information to the run_stream()
method.

Created on May 6, 2015

@author: arbennett
"""
import os
import fnmatch

from verification.base import AbstractTest
from util.parser import Parser
import util.variables

def get_name(): return "Stream"

class Test(AbstractTest):
    """
    Main class for handling stream test cases.
    
    The stream test cases inherit functionality from AbstractTest for checking 
    bit-for-bittedness from a model run. This class handles evolving and \
    diagnostic variations of the stream case.
    """

    def __init__(self):
        """ Constructor """
        super(self.__class__, self).__init__()
        self.name = "Stream"
        self.model_dir = util.variables.input_dir + os.sep + "stream"
        self.bench_dir = util.variables.benchmark_dir + os.sep + "stream"
        self.description = "The stream test case simulates flow over an" + \
                            " idealized ice stream underlain by a subglacial" + \
                            " till with a known and specified yield stress distribution. "


    def run(self, ver_summary, output):
        """
        Runs all of the available stream tests.  Looks in the model and
        benchmark directories for different variations, and then runs
        the run_stream() method with the correct information
        
        Args:
            ver_summary: multiprocessing dict to store summaries for each run
            output: multiprocessing queue to store information to print to stdout
        """
        if not (os.path.exists(self.model_dir) and os.path.exists(self.bench_dir)):
            output.put("    Could not find data for stream  verification!  Tried to find data in:")
            output.put("      " + self.model_dir)
            output.put("      " + self.bench_dir)
            output.put("    Continuing with next test....")
            return

        resolutions = set()
        model_configFiles = fnmatch.filter(os.listdir(self.model_dir), 'stream*.config')
        for mcf in model_configFiles:
            resolutions.add( mcf.split('.')[1] )
        resolutions = sorted( resolutions )
                
        self.run_stream(resolutions[0], self.model_dir, self.bench_dir, output)
        self.tests_run.append("Stream " + resolutions[0])
        self.generate()
        ver_summary[self.name.lower()] = self.summary
        output.put("")
        

    def run_stream(self, resolution, model_dir, bench_dir, output):
        """
        Runs the stream V&V for a given resolution.  First parses through all 
        of the standard output & config files for the given test case, then finishes up by 
        doing bit for bit comparisons with the benchmark files.
        
        Args:
            resolution: The resolution of the test cases to look in.
            model_dir: the location of the model run data
            bench_dir: the location of the benchmark data
            output: multiprocessing queue to store information to print to stdout
        """
        # Process the configure files
        output.put("  Stream " + resolution + " test in progress....")
        stream_parser = Parser()
        self.model_configs['Stream ' + resolution], self.bench_configs['Stream ' + resolution] = \
                stream_parser.parse_configurations(model_dir, bench_dir, "*" + resolution + ".*.config")

        # Parse standard out
        self.file_test_details["Stream " + resolution] = stream_parser.parse_stdOutput(model_dir,"stream." + resolution + ".*.config.oe")

        # Record the data from the parser
        number_outputFiles, number_configMatches, number_configTests = stream_parser.get_parserSummary()

        # Run bit for bit test
        number_bitMatches, number_bitTests = 0, 0
        self.bit_for_bit_details['Stream ' + resolution] = self.bit4bit('stream', model_dir, bench_dir, resolution)
        for key, value in self.bit_for_bit_details['Stream ' + resolution].iteritems():
            output.put("    {:<40} {:<10}".format(key, value[0]))
            if value[0] == "SUCCESS": number_bitMatches += 1
            number_bitTests += 1

        self.summary['Stream ' + resolution] = [number_outputFiles,
                                             number_configMatches, number_configTests,
                                             number_bitMatches, number_bitTests]

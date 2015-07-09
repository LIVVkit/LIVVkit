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
Master module for GIS test cases.  Inherits methods from the Abstract_test
class from the Test module.  GIS specific verification are performed by calling
the run() method, which passes the necessary information to the run_gisPerformance()
method.

Created on Dec 8, 2014

@author: arbennett
"""
import os

import util.variables
from base import AbstractTest
from util.parser import Parser

def get_name(): return "Greenland Ice Sheet"


class Test(AbstractTest):
    """
    Main class for handling Greenland Ice Sheet performance validation.
    
    The Greenland Ice Sheet test cases inherit functionality from AbstractTest for
    generating scaling plots and generating the output webpage.
    """

    def __init__(self):
        """ Constructor """
        super(self.__class__, self).__init__()
        self.name = "gis"
        self.model_dir = util.variables.input_dir + os.sep + "gis"
        self.bench_dir = util.variables.benchmark_dir + os.sep + 'gis'
        self.description = "A placeholder description"

    def run(self):
        """
        This method will record the specific test cases
        being run.  Each specific test case string is run via the 
        run_gisPerformance function.  All of the data pulled is then
        assimilated via the run_scaling method defined in the base class
        """
        print("This is a placeholder")


    def run_gisPerformance(self, resolution):
        """
        Greenland Ice Sheet Performance Testing
        
        Args:
            resolution : the resolution of the test data
        """
        print(os.linesep + "  Greenland Ice Sheet " + resolution + " performance testing in progress....")

        # Make sure that there is some data
        if not (os.path.exists(self.model_dir) and os.path.exists(self.bench_dir)):
            print("    Could not find data for GIS " + resolution + " verification!  Tried to find data in:")
            print("      " + self.model_dir)
            print("      " + self.bench_dir)
            print("    Continuing with next test....")
            return

        # Process the configure files
        gis_parser = Parser()
        self.model_configs['gis_' + resolution], self.bench_configs['gis_' + resolution] = \
                gis_parser.parse_configurations(self.model_dir, self.bench_dir)

        # Scrape the details from each of the files and store some data for later
        self.file_test_details['gis_' + resolution] = gis_parser.parse_stdOutput(self.model_dir, "^out.gis." + resolution + ".((albany)|(glissade))$")

        # Go through and pull in the timing data
        print("    Model Timing Summary:")
        self.model_timing_data['gis' + resolution] = gis_parser.parse_timingSummaries(self.model_dir)
        print("    Benchmark Timing Summary:")
        self.bench_timing_data['gis' + resolution] = gis_parser.parse_timingSummaries(self.bench_dir)

        # Record the data from the parser
        number_outputFiles, number_configMatches, number_configTests = gis_parser.get_parserSummary()

        self.summary['gis_' + resolution] = [number_outputFiles, number_configMatches, number_configTests]

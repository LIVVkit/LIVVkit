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
Verification Test Base Module
The Abstract_test class defines several methods that each test class must implement, 
as well as provides bit for bit and html generating capabilities which are inherited
by all derived test classes.

@author: arbennett
"""

import sys
import os
import re
from netCDF4 import Dataset
import glob
import numpy
import jinja2
import multiprocessing
from abc import ABCMeta, abstractmethod 

from plots import nclfunc
from util.parser import Parser
import util.variables

def good_time_dim(file_name):
    """
    Check netCDF files time dimension for emptyness. This likely
    indicates the run did not complete.
    """    
    nc_file = Dataset(file_name, 'r')
    times = False
    if len(nc_file.dimensions['time']) > 0:
        # empty, unlimited dims will be length 0
        times = True
    nc_file.close()
    return times


class AbstractTest(object):
    """
    AbstractTest provides a description of how a verification test should 
    work in LIVV.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        """ Constructor """   
        self.name = "default"
        self.model_dir, self.bench_dir = "", ""
        self.tests_run = []
        self.manager = multiprocessing.Manager()
        self.bit_for_bit_details = self.manager.dict()
        self.plot_details = self.manager.dict()
        self.test_details = self.manager.dict()
        self.bench_details = self.manager.dict()
        self.test_configs = self.manager.dict() 
        self.bench_configs = self.manager.dict()
        self.summary = self.manager.dict()


    @abstractmethod
    def collect_cases(self):
        """ Create a list the cases available """
        pass


    def convert_dicts(self):
        """ 
        Convert all of the multiprocessing datastructures to 
        the basic Python versions.  This is done so that
        Jinja2 can parse through them easily.
        """
        self.bit_for_bit_details = dict(self.bit_for_bit_details)
        self.plot_details = dict(self.plot_details)
        self.test_details = dict(self.test_details)
        self.bench_details = dict(self.bench_details)
        self.test_configs = dict(self.test_configs)
        self.bench_configs = dict(self.bench_configs)
        self.summary = dict(self.summary)


    def run(self, ver_summary, output):
        """
        Runs all of the available verification tests of a specific type.  
        Looks in the model and benchmark directories for different variations,
        and then runs the run_case() method with the correct information
        
        Args:
            ver_summary: multiprocessing dict to store summaries for each run
            output: multiprocessing queue to store information to print to stdout
        """
        if not (os.path.exists(self.model_dir) and os.path.exists(self.bench_dir)):
            output.put("    Could not find data for " + self.name + " verification!  Tried to find data in:")
            output.put("      " + self.model_dir)
            output.put("      " + self.bench_dir)
            output.put("    Continuing with next test....")
            return

        self.collect_cases()
        process_handles = [multiprocessing.Process(target=self.run_case, args=(tc,output)) for tc in self.tests_run]
        
        for p in process_handles:
            p.start()

        for p in process_handles:
            p.join()
        
        self.convert_dicts()
        self.generate()
        ver_summary[self.name.lower()] = self.summary


    def run_case(self, test_case, output):
        """
        Runs the V&V for a given case.  First parses through all of the standard 
        output  & config files for the given test case and finishes up by doing 
        bit for bit comparisons with the benchmark files.
    
        Args:
            test_case: Which version of the  test should be run
            output: multiprocessing queue to store information to print to stdout
        """
        test_name = "Dome " + test_case 

        # Process the configure files
        parser = Parser()
        self.test_configs[test_case], self.bench_configs[test_case] = \
            parser.parse_configurations(self.model_dir, self.bench_dir, self.name + "*" + test_case + ".*.config")

        # Scrape the details from each of the files and store some data for later
        self.test_details[test_case] = parser.parse_std_output(self.model_dir, self.name + "*(.|-)" + test_case + ".*.config.oe")
        self.bench_details[test_case] = parser.parse_std_output(self.bench_dir, self.name + "*(.|-)" + test_case + ".*.config.oe")

        # Record the data from the parser
        number_outputFiles, number_configMatches, number_configTests = parser.get_parserSummary()

        # Run bit for bit test
        number_bitTests, number_bitMatches = 0, 0
        self.bit_for_bit_details[test_case] = self.bit4bit(self.name + "*" + test_case, test_case)
        for key, value in self.bit_for_bit_details[test_case].iteritems():
            if value[0] == "SUCCESS": number_bitMatches+=1
            number_bitTests+=1

        self.summary[test_case] = [number_outputFiles, number_configMatches, number_configTests,
                                  number_bitMatches, number_bitTests]


    def bit4bit(self, test, resolution):
        """
        Tests all models and benchmarks against each other in a bit for bit fashion.
        
        Args:
            test: the test case to check bittedness
            resolution: the size of the test being run
        Returns:
            [change, err] where change in {0,1} and err is a list of the status and some metrics
        """
        # Mapping of result codes to results
        numpy.set_printoptions(threshold='nan')
        result = {-1 : 'N/A', 0 : 'SUCCESS', 1 : 'FAILURE'}
        bit_dict = dict()

        if not (os.path.exists(self.model_dir) or os.path.exists(self.bench_dir)):
            return {'No matching benchmark and data files found': ['SKIPPED','0.0']}
        
        # Get the intersection of the two file lists
        regex = self.name + '*(.|-)' + resolution + '.*.out.nc'
        test_files = [fn.split(os.sep)[-1] for fn in filter(re.compile(regex).search, os.listdir(self.model_dir))]
        bench_files = [fn.split(os.sep)[-1] for fn in filter(re.compile(regex).search, os.listdir(self.bench_dir))]
        same_list = set(test_files).intersection(bench_files)
        if len(same_list) == 0:
            return {'No matching benchmark and data files found': ['SKIPPED','0.0']}

        # Go through and check if any differences occur
        for same in list(same_list):
            change = 0
            plot_vars = dict()
            test_file = self.model_dir + os.sep + same
            bench_file = self.bench_dir + os.sep + same

            # check for empty time dimensions
            good_bench = good_time_dim(bench_file)
            good_test = good_time_dim(test_file)
            
            if (not good_bench) and (not good_test):
                bit_dict[same] =  ['EMPTY TIME','benchmark and test']
            elif not good_bench:
                bit_dict[same] =  ['EMPTY TIME','benchmark']
            elif not good_test:
                bit_dict[same] =  ['EMPTY TIME','test']
            else:
                # Create a difference file with ncdiff
                test= Dataset(test_file, 'r')
                test_data = test.variables
                bench = Dataset(bench_file,'r')
                bench_data = bench.variables

                # Check if any data in thk has changed, if it exists
                if 'thk' in test_data and 'thk' in bench_data and \
                        test_data['thk'].size != 0 and bench_data['thk'].size != 0:
                    data = test_data['thk'][:] - bench_data['thk'][:]
                    if data.any():
                        # Record the maximum difference and root mean square of the error 
                        max = numpy.amax( numpy.absolute(data) )
                        rmse = numpy.sqrt(numpy.sum( numpy.square(data).flatten() ) / data.size )
                        plot_vars['thk'] = [max, rmse]
                        change = 1

                # Check if any data in velnorm has changed, if it exists
                if 'velnorm' in test_data and 'velnorm' in bench_data and \
                        test_data['velnorm'].size != 0 and bench_data['velnorm'].size != 0:
                    data = test_data['velnorm'][:] - bench_data['velnorm'][:]
                    if data.any():
                        # Record the maximum difference and root mean square of the error 
                        max = numpy.amax( numpy.absolute(data) )
                        rmse = numpy.sqrt(numpy.sum( numpy.square(data).flatten() ) / data.size )
                        plot_vars['velnorm'] = [max, rmse]
                        change = 1

                test.close()
                bench.close()
                bit_dict[same] = [result[change],  plot_vars]
                # Generate the plots for each of the failed variables
                for var in plot_vars.keys():
                    out_file = util.variables.index_dir + os.sep + "verification" + os.sep + \
                               self.name.capitalize() + os.sep + "imgs" + os.sep + "bit4bit" + \
                               os.sep + test_file.split(os.sep)[-1] + "." + var + ".png"
                    nclfunc.plot_diff(var, test_file, bench_file, out_file)
        return bit_dict


    def generate(self):
        """ 
        The generate method will create a {{test}}.html page in the output directory.
        This page will contain a detailed list of the results from LIVV.  Details
        from the run are pulled from two locations.  Global definitions that are 
        displayed on every page, or used for navigation purposes are imported
        from the main livv.py module.  All test specific information is supplied
        via class variables.
        
        @note Paths that are contained in template_vars should not be using os.sep
              since they are for html.
        """
        template_loader = jinja2.FileSystemLoader(searchpath=util.variables.template_dir)
        template_env = jinja2.Environment(loader=template_loader, extensions=["jinja2.ext.do",])
        template_file = "/verification_test.html"
        template = template_env.get_template(template_file)
        index_dir = ".."
        css_dir = index_dir + "/css"
        img_dir = index_dir + "/imgs"
        test_imgDir = index_dir + os.sep + "verification" + os.sep + \
                      self.name.capitalize() + os.sep + "imgs"
        test_images = [os.path.basename(img) for img in glob.glob(test_imgDir + os.sep + "*.png")]
        test_images.append([os.path.basename(img) for img in glob.glob(test_imgDir + "*.jpg")])
        test_images.append([os.path.basename(img) for img in glob.glob(test_imgDir + "*.svg")])
        template_vars = {"timestamp" : util.variables.timestamp,
                        "user" : util.variables.user,
                        "comment" : util.variables.comment,
                        "test_name" : self.name.capitalize(),
                        "index_dir" : index_dir,
                        "css_dir" : css_dir,
                        "img_dir" : img_dir,
                        "test_imgDir" : test_imgDir,
                        "test_description" : self.description,
                        "tests_run" : self.tests_run,
                        "test_header" : util.variables.parser_vars,
                        "bit_for_bit_details" : self.bit_for_bit_details,
                        "test_details" : self.test_details,
                        "bench_details" : self.bench_details,
                        "plot_details" : self.plot_details,
                        "test_configs" : self.test_configs,
                        "bench_configs" : self.bench_configs,
                        "test_images" : test_images}
        output_text = template.render( template_vars )
        page = open(util.variables.index_dir + os.sep + "verification" + os.sep + self.name.lower() + '.html', "w")
        page.write(output_text)
        page.close()


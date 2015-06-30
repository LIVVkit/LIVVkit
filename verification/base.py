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

Created on Dec 8, 2014

@author: arbennett
"""

import sys
import os
import subprocess
from netCDF4 import Dataset
import glob
import numpy
import jinja2
from abc import ABCMeta, abstractmethod 

from plots import nclfunc
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
    AbstractTest provides a description of how a test should work in LIVV.
    
    Each test within LIVV needs to be able to run specific test code, and
    generate its output.  Tests inherit a common method of checking for 
    bit-for-bittedness
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        """ Constructor """   
        self.name = "default"
        self.model_dir, self.bench_dir = "", ""
        self.tests_run = []
        self.bit_for_bit_details = dict()
        self.plot_details = dict()
        self.file_test_details = dict()
        self.model_configs, self.bench_configs = dict(), dict()
        self.summary = dict()


    @abstractmethod
    def run(self, test):
        """ Definition for the general test run """
        pass


    def bit4bit(self, test, test_dir, bench_dir, resolution):
        """
        Tests all models and benchmarks against each other in a bit for bit fashion.
        
        Args:
            test: the test case to check bittedness
            test_dir: the path to the model data
            bench_dir: the path to the benchmark data
            resolution: the size of the test being run
        Returns:
            [change, err] where change in {0,1} and err is a list of the status and some metrics
        """
        # Mapping of result codes to results
        numpy.set_printoptions(threshold='nan')
        result = {-1 : 'N/A', 0 : 'SUCCESS', 1 : 'FAILURE'}
        bit_dict = dict()

        if not (os.path.exists(test_dir) or os.path.exists(bench_dir)):
            return {'No matching benchmark and data files found': ['SKIPPED','0.0']}
        
        # Get the intersection of the two file lists
        test_files = [fn.split(os.sep)[-1] for fn in glob.glob(test_dir + os.sep + test + '.' + resolution + '*.out.nc')]
        bench_files = [fn.split(os.sep)[-1] for fn in glob.glob(bench_dir + os.sep + test + '.' + resolution + '*.out.nc')]
        same_list = set(test_files).intersection(bench_files)
        if len(same_list) == 0:
            return {'No matching benchmark and data files found': ['SKIPPED','0.0']}

        # Go through and check if any differences occur
        for same in list(same_list):
            change = 0
            plot_vars = dict()
            test_file = test_dir + os.sep + same
            bench_file = bench_dir + os.sep + same

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
                comline = ['ncdiff', test_file, bench_file, test_dir + os.sep + 'temp.nc', '-O']
                try:
                    subprocess.check_call(comline)
                except Exception as e:
                    print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                          + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                    try:
                        exit(e.returncode)
                    except AttributeError:
                        exit(e.errno)
                diff_data = Dataset(test_dir + os.sep + 'temp.nc', 'r')
                diff_vars = diff_data.variables.keys()

                # Check if any data in thk has changed, if it exists
                if 'thk' in diff_vars and diff_data.variables['thk'].size != 0:
                    data = diff_data.variables['thk'][:]
                    if data.any():
                        # Record the maximum difference and root mean square of the error 
                        max = numpy.amax( numpy.absolute(data) )
                        rmse = numpy.sqrt(numpy.sum( numpy.square(data).flatten() ) / data.size )
                        plot_vars['thk'] = [max, rmse]
                        change = 1

                # Check if any data in velnorm has changed, if it exists
                if 'velnorm' in diff_vars and diff_data.variables['velnorm'].size != 0:
                    data = diff_data.variables['velnorm'][:]
                    if data.any():
                        # Record the maximum difference and root mean square of the error 
                        max = numpy.amax( numpy.absolute(data) )
                        rmse = numpy.sqrt(numpy.sum( numpy.square(data).flatten() ) / data.size )
                        plot_vars['velnorm'] = [max, rmse]
                        change = 1

                # Remove the temp file
                try:
                    os.remove(test_dir + os.sep + 'temp.nc')
                except OSError as e:
                    print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                          + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                    exit(e.errno)
                bit_dict[same] = [result[change],  plot_vars]

                # Generate the plots for each of the failed variables
                for var in plot_vars.keys():
                    out_file = util.variables.img_dir + os.sep + self.name + os.sep + "bit4bit" + os.sep + test_file.split(os.sep)[-1] + "." + var + ".png"
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
        test_imgDir = util.variables.img_dir + os.sep + self.name
        test_images = [os.path.basename(img) for img in glob.glob(test_imgDir + os.sep + "*.png")]
        test_images.append([os.path.basename(img) for img in glob.glob(test_imgDir + "*.jpg")])
        test_images.append([os.path.basename(img) for img in glob.glob(test_imgDir + "*.svg")])
        template_vars = {"timestamp" : util.variables.timestamp,
                        "user" : util.variables.user,
                        "comment" : util.variables.comment,
                        "test_name" : self.name,
                        "index_dir" : index_dir,
                        "css_dir" : css_dir,
                        "img_dir" : img_dir,
                        "test_description" : self.description,
                        "tests_run" : self.tests_run,
                        "test_header" : util.variables.parser_vars,
                        "bit_for_bit_details" : self.bit_for_bit_details,
                        "test_details" : self.file_test_details,
                        "plot_details" : self.plot_details,
                        "model_configs" : self.model_configs,
                        "bench_configs" : self.bench_configs,
                        "test_images" : test_images}
        output_text = template.render( template_vars )
        page = open(util.variables.index_dir + os.sep + "verification" + os.sep + self.name.lower() + '.html', "w")
        page.write(output_text)
        page.close()

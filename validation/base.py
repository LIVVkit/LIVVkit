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
Validation Test Base Module
The Abstract_test class defines several methods that each test class must implement.

Created on Apr 24, 2015

@author: arbennett
"""
import os
import glob
import jinja2
from abc import ABCMeta, abstractmethod

import util.variables

# A mapping of the options to the test cases that can be run
cases = {'none' : [],
         'gis' : ['gis'],
         'all' : ['gis']}

""" Return a list of options """
def choices(): return list( cases.keys() )

""" Return the tests associated with an option """
def choose(key): return cases[key] if cases.has_key(key) else None

"""
Provide base functionality for a Validation test

Each test within LIVV needs to be able to run specific test code, and
generate its output.
"""
class Abstract_test(object):
    __metaclass__ = ABCMeta

    """ Constructor """
    def __init__(self):
        self.name = 'na'
        self.tests_run = []
        self.summary = dict()
        self.plot_details = dict()
        self.file_test_details = dict()
        
    """ Definition for the general test run """
    @abstractmethod
    def run(self, test):
        pass

    """
    Creates the output test page
    
    The generate method will create a {{test}}.html page in the output directory.
    This page will contain a detailed list of the results from LIVV.  Details
    from the run are pulled from two locations.  Global definitions that are 
    displayed on every page, or used for navigation purposes are imported
    from the main livv.py module.  All test specific information is supplied
    via class variables.
    
    @note Paths that are contained in template_vars should not be using os.sep
          since they are for html.
    """
    def generate(self):
        # Set up jinja related variables
        template_loader = jinja2.File_systemLoader(searchpath=util.variables.template_dir)
        template_env = jinja2.Environment(loader=template_loader, extensions=["jinja2.ext.do",])
        template_file = "/validation_test.html"
        template = template_env.get_template(template_file)

        # Set up relative paths
        index_dir = ".."
        css_dir = index_dir + "/css"
        img_dir = index_dir + "/imgs"

        # Grab all of our images
        test_imgDir = util.variables.img_dir + os.sep + self.name
        test_images = [os.path.basename(img) for img in glob.glob(test_imgDir + os.sep + "*.png")]
        test_images.append([os.path.basename(img) for img in glob.glob(test_imgDir + os.sep +"*.jpg")])
        test_images.append([os.path.basename(img) for img in glob.glob(test_imgDir + os.sep +"*.svg")])

        # Set up the template variables  
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
                        "test_details" : self.file_test_details,
                        "plot_details" : self.plot_details,
                        "model_configs" : self.model_configs,
                        "bench_configs" : self.bench_configs,
                        "model_timing_data" : self.model_timing_data,
                        "bench_timing_data" : self.bench_timing_data,
                        "test_images" : test_images}
        output_text = template.render( template_vars )
        page = open(util.variables.index_dir + os.sep + "performance" + os.sep + self.name.lower() + '.html', "w")
        page.write(output_text)
        page.close()


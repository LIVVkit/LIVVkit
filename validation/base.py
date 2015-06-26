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
The AbstractTest class defines several methods that each test class must implement.

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
class AbstractTest(object):
    __metaclass__ = ABCMeta

    """ Constructor """
    def __init__(self):
        self.name = 'na'
        self.testsRun = []
        self.summary = dict()
        self.plotDetails = dict()
        self.fileTestDetails = dict()
        
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
    
    @note Paths that are contained in templateVars should not be using os.sep
          since they are for html.
    """
    def generate(self):
        # Set up jinja related variables
        templateLoader = jinja2.FileSystemLoader(searchpath=util.variables.templateDir)
        templateEnv = jinja2.Environment(loader=templateLoader, extensions=["jinja2.ext.do",])
        templateFile = "/validation_test.html"
        template = templateEnv.get_template(templateFile)

        # Set up relative paths
        indexDir = ".."
        cssDir = indexDir + "/css"
        imgDir = indexDir + "/imgs"

        # Grab all of our images
        testImgDir = util.variables.imgDir + os.sep + self.name
        testImages = [os.path.basename(img) for img in glob.glob(testImgDir + os.sep + "*.png")]
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + os.sep +"*.jpg")])
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + os.sep +"*.svg")])

        # Set up the template variables  
        templateVars = {"timestamp" : util.variables.timestamp,
                        "user" : util.variables.user,
                        "comment" : util.variables.comment,
                        "testName" : self.name,
                        "indexDir" : indexDir,
                        "cssDir" : cssDir,
                        "imgDir" : imgDir,
                        "testDescription" : self.description,
                        "testsRun" : self.testsRun,
                        "testHeader" : util.variables.parserVars,
                        "testDetails" : self.fileTestDetails,
                        "plotDetails" : self.plotDetails,
                        "modelConfigs" : self.modelConfigs,
                        "benchConfigs" : self.benchConfigs,
                        "modelTimingData" : self.modelTimingData,
                        "benchTimingData" : self.benchTimingData,
                        "testImages" : testImages}
        outputText = template.render( templateVars )
        page = open(util.variables.indexDir + os.sep + "performance" + os.sep + self.name.lower() + '.html', "w")
        page.write(outputText)
        page.close()


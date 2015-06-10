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


'''
Verification Test Base Module
The AbstractTest class defines several methods that each test class must implement, 
as well as provides bit for bit and html generating capabilities which are inherited
by all derived test classes.

Created on Dec 8, 2014

@author: arbennett
'''

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

# A mapping of the options to the test cases that can be run
cases = {'none' : [],
         'ismip' : ['ismip'],
         'dome' : ['dome'],
         'shelf' : ['shelf'],
         'stream' : ['stream'],
         'all' : ['dome', 'ismip', 'shelf', 'stream']}

''' Return a list of options '''
def choices(): return list( cases.keys() )

''' Return the tests associated with an option '''
def choose(key): return cases[key] if cases.has_key(key) else None

'''
AbstractTest provides a description of how a test should work in LIVV.

Each test within LIVV needs to be able to run specific test code, and
generate its output.  Tests inherit a common method of checking for 
bit-for-bittedness
'''
class AbstractTest(object):
    __metaclass__ = ABCMeta

    ''' Constructor '''
    def __init__(self):
        self.name = "default"
        self.modelDir, self.benchDir = "", ""
        self.testsRun = []
        self.bitForBitDetails = dict()
        self.plotDetails = dict()
        self.fileTestDetails = dict()
        self.modelConfigs, self.benchConfigs = dict(), dict()
        self.summary = dict()


    ''' Definition for the general test run '''
    @abstractmethod
    def run(self, test):
        pass

    '''
    Tests all models and benchmarks against each other in a bit for bit fashion.
    If any differences are found the method will return 1, otherwise 0.
    
    @param test: the test case to check bittedness
    @param testDir: the path to the model data
    @param benchDir: the path to the benchmark data
    @param resolution: the size of the test being run
    @returns [change, err] where change in {0,1} and result in {'N/A', 'SUCCESS', 'FAILURE'}
    '''
    def bit4bit(self, test, testDir, benchDir, resolution):
        # Mapping of result codes to results
        numpy.set_printoptions(threshold='nan')
        result = {-1 : 'N/A', 0 : 'SUCCESS', 1 : 'FAILURE'}
        bitDict = dict()

        # First, make sure that there is test data, otherwise not it.
        if not (os.path.exists(testDir) or os.path.exists(benchDir)):
            return {'No matching benchmark and data files found': ['SKIPPED','0.0']}
        
        # Get the intersection of the two file lists
        testFiles = [fn.split(os.sep)[-1] for fn in glob.glob(testDir + os.sep + test + '.' + resolution + '.*.out.nc')]
        benchFiles = [fn.split(os.sep)[-1] for fn in glob.glob(benchDir + os.sep + test + '.' + resolution + '.*.out.nc')]
        sameList = set(testFiles).intersection(benchFiles)

        # If the intersection is empty just return a blank entry
        if len(sameList) == 0:
            print("  Benchmark and model data not available for " + test)
            return {'No matching benchmark and data files found': ['SKIPPED','0.0']}
        else:
            print("  Running bit for bit verification of " + test + "....")

        # Go through and check if any differences occur
        for same in list(sameList):
            change = 0
            plotVars = dict()
            testFile = testDir + os.sep + same
            benchFile = benchDir + os.sep + same

            # Create a difference file with ncdiff
            comline = ['ncdiff', testFile, benchFile, testDir + os.sep + 'temp.nc', '-O']
            try:
                subprocess.check_call(comline)
            except Exception as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                      + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                try:
                    exit(e.returncode)
                except AttributeError:
                    exit(e.errno)
            diffData = Dataset(testDir + os.sep + 'temp.nc', 'r')
            diffVars = diffData.variables.keys()

            # Check if any data in thk has changed, if it exists
            if 'thk' in diffVars and diffData.variables['thk'].size != 0:
                data = diffData.variables['thk'][:]
                if data.any():
                    # Record the maximum difference and root mean square of the error 
                    max = numpy.amax( numpy.absolute(data) )
                    rmse = numpy.sqrt(numpy.sum( numpy.square(data).flatten() ) / data.size )
                    plotVars['thk'] = [max, rmse]
                    change = 1

            # Check if any data in velnorm has changed, if it exists
            if 'velnorm' in diffVars and diffData.variables['velnorm'].size != 0:
                data = diffData.variables['velnorm'][:]
                if data.any():
                    # Record the maximum difference and root mean square of the error 
                    max = numpy.amax( numpy.absolute(data) )
                    rmse = numpy.sqrt(numpy.sum( numpy.square(data).flatten() ) / data.size )
                    plotVars['velnorm'] = [max, rmse]
                    change = 1

            # Remove the temp file
            try:
                os.remove(testDir + os.sep + 'temp.nc')
            except OSError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                      + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.errno)
            bitDict[same] = [result[change],  plotVars]

            # Generate the plots for each of the failed variables
            for var in plotVars.keys():
                outFile = util.variables.imgDir + os.sep + self.name + os.sep + "bit4bit" + os.sep + testFile.split(os.sep)[-1] + "." + var + ".png"
                nclfunc.plot_diff(var, testFile, benchFile, outFile)
        return bitDict

    ''' 
    The generate method will create a {{test}}.html page in the output directory.
    This page will contain a detailed list of the results from LIVV.  Details
    from the run are pulled from two locations.  Global definitions that are 
    displayed on every page, or used for navigation purposes are imported
    from the main livv.py module.  All test specific information is supplied
    via class variables.
    
    @note Paths that are contained in templateVars should not be using os.sep
          since they are for html.
    '''
    def generate(self):
        # Set up jinja related variables
        templateLoader = jinja2.FileSystemLoader(searchpath=util.variables.templateDir)
        templateEnv = jinja2.Environment(loader=templateLoader, extensions=["jinja2.ext.do",])
        templateFile = "/verification_test.html"
        template = templateEnv.get_template(templateFile)

        # Set up relative paths
        indexDir = ".."
        cssDir = indexDir + "/css"
        imgDir = indexDir + "/imgs"

        # Grab all of our images
        testImgDir = util.variables.imgDir + os.sep + self.name
        testImages = [os.path.basename(img) for img in glob.glob(testImgDir + os.sep + "*.png")]
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + "*.jpg")])
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + "*.svg")])

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
                        "bitForBitDetails" : self.bitForBitDetails,
                        "testDetails" : self.fileTestDetails,
                        "plotDetails" : self.plotDetails,
                        "modelConfigs" : self.modelConfigs,
                        "benchConfigs" : self.benchConfigs,
                        "testImages" : testImages}
        outputText = template.render( templateVars )
        page = open(util.variables.indexDir + os.sep + "verification" + os.sep + self.name.lower() + '.html', "w")
        page.write(outputText)
        page.close()

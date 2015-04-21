'''
Contains two classes for generalized testing in LIVV.

The AbstractTest class defines several methods that each test class must implement, 
as well as provides bit for bit and stdout parsing capabilities which are inherited
by all derived test classes.  

The TestSummary is a dummy class that is used to generate the index of the output.
It implements a method called webSetup that creates the index with a short summary
of the execution stats.  All other methods are dummies.  Further implementations
similar to TestSummary are discouraged to avoid breaking the AbstractTest template.

Created on Dec 8, 2014

@author: arbennett
'''

import sys
import re
import os
import subprocess
import shutil
from netCDF4 import Dataset
import matplotlib.pyplot as pyplot
import glob
import numpy
import jinja2
from abc import ABCMeta, abstractmethod
import livv

from plots import nclfunc

## AbstractTest provides a description of how a test should work in LIVV.
#
#  Each test within LIVV needs to be able to run specific test code, and
#  generate its output.  Tests inherit a common method of checking for 
#  bit-for-bittedness as well for parsing the standard output of model output
#
class AbstractTest(object):
    __metaclass__ = ABCMeta

    ## Constructor
    #
    def __init__(self):
        self.testsRun = []
        self.bitForBitDetails = dict()
        self.plotDetails = dict()
        self.fileTestDetails = dict()
        self.modelConfigs, self.benchConfigs = dict(), dict()
        self.summary = dict()

    ## Should return the name of the test
    #
    @abstractmethod
    def getName(self):
        pass

    ## Definition for the general test run
    #
    #  input:
    #    @param test : the string indicator of the test to run
    #
    @abstractmethod
    def run(self, test):
        pass

    ## Get a summary of the verification that have been run 
    #
    #  Output:
    #    @return a dictionary of the testcases that holds various statistics
    #
    def getSummary(self):
        return self.summary

    ## Tests all models and benchmarks against each other in a bit for bit fashion.
    #  If any differences are found the method will return 1, otherwise 0.
    #
    #  Input:
    #    @param test: the test case to check bitness
    #    @param testDir: the path to the model data
    #    @param benchDir: the path to the benchmark data
    #
    #  Output:
    #    @returns [change, err] where change in {0,1}
    #
    def bit4bit(self, test, testDir, benchDir):
        # Mapping of result codes to results
        numpy.set_printoptions(threshold='nan')
        result = {-1 : 'N/A', 0 : 'SUCCESS', 1 : 'FAILURE'}
        bitDict = dict()

        # First, make sure that there is test data, otherwise not it.
        if not (os.path.exists(testDir) or os.path.exists(benchDir)):
            return {'No matching benchmark and data files found': ['SKIPPED','0.0']}

        # Get all of the .nc files in the model & benchmark directories
        regex = re.compile('^[^\.].*?.nc')
        testFiles = filter(regex.search, os.listdir(testDir))
        benchFiles = filter(regex.search, os.listdir(benchDir))

        # Get the intersection of the two file lists
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

            # check if they match
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

            # Grab the output of ncdiff
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

            # Record the status and details of the test
            bitDict[same] = [result[change],  plotVars]

            # Generate the plots for each of the failed variables
            for var in plotVars.keys():
                outFile = livv.imgDir + os.sep + self.getName() + os.sep + "bit4bit" + os.sep + testFile.split(os.sep)[-1] + "." + var + ".png"
                nclfunc.plot_diff(var, testFile, benchFile, outFile)

        return bitDict


    ## Creates the output test page
    #
    #  The generate method will create a {{test}}.html page in the output directory.
    #  This page will contain a detailed list of the results from LIVV.  Details
    #  from the run are pulled from two locations.  Global definitions that are 
    #  displayed on every page, or used for navigation purposes are imported
    #  from the main livv.py module.  All dome specific information is supplied
    #  via class variables.
    #
    #  \note Paths that are contained in templateVars should not be using os.sep
    #        since they are for html.
    #
    def generate(self):
        # Set up jinja related variables
        templateLoader = jinja2.FileSystemLoader(searchpath=livv.templateDir)
        templateEnv = jinja2.Environment(loader=templateLoader, extensions=["jinja2.ext.do",])
        templateFile = "/test.html"
        template = templateEnv.get_template(templateFile)

        # Set up relative paths
        indexDir = ".."
        cssDir = indexDir + "/css"
        imgDir = indexDir + "/imgs"

        # Grab all of our images
        testImgDir = livv.imgDir + os.sep + self.getName()
        testImages = [os.path.basename(img) for img in glob.glob(testImgDir + os.sep + "*.png")]
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + "*.jpg")])
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + "*.svg")])

        # Set up the template variables  
        templateVars = {"timestamp" : livv.timestamp,
                        "user" : livv.user,
                        "comment" : livv.comment,
                        "testName" : self.getName(),
                        "indexDir" : livv.indexDir,
                        "cssDir" : cssDir,
                        "testDescription" : self.description,
                        "testsRun" : self.testsRun,
                        "testHeader" : livv.parserVars,
                        "bitForBitDetails" : self.bitForBitDetails,
                        "testDetails" : self.fileTestDetails,
                        "plotDetails" : self.plotDetails,
                        "modelConfigs" : self.modelConfigs,
                        "benchConfigs" : self.benchConfigs,
                        "imgDir" : imgDir,
                        "testImages" : testImages}
        outputText = template.render( templateVars )
        page = open(livv.indexDir + os.sep + "verification" + os.sep + self.getName() + '.html', "w")
        page.write(outputText)
        page.close()




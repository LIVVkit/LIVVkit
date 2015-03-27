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

    ## Get a summary of the tests that have been run 
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

        if len(sameList) == 0:
            print("  Benchmark and model data not available for " + test)
            return {'No matching benchmark and data files found': ['SKIPPED','0.0']}
        else:
            print("  Running bit for bit tests of " + test + "....")


        # Go through and check if any differences occur
        for same in list(sameList):
            change = 0
            difference = [0.0, 0.0, 0.0, 0.0] # thk max abs, thk RMS, velnorm max abs, velnorm RMS
            plotVars = []
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
                    difference[0] = numpy.amax( numpy.absolute(data) )
                    difference[1] = numpy.sqrt(numpy.sum( numpy.square(data).flatten() ) / data.size )
                    plotVars.append('thk')
                    change = 1

            # Check if any data in velnorm has changed, if it exists
            if 'velnorm' in diffVars and diffData.variables['velnorm'].size != 0:
                data = diffData.variables['velnorm'][:]
                if data.any():
                    difference[2] = numpy.amax( numpy.absolute(data) )
                    difference[3] = numpy.sqrt(numpy.sum( numpy.square(data).flatten() ) / data.size )
                    plotVars.append('velnorm')
                    change = 1

            
            # Remove the temp file
            try:
                os.remove(testDir + os.sep + 'temp.nc')
            except OSError as e:
                print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                      + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
                exit(e.errno)

            bitDict[same] = [result[change], 
                             "{:.4g}".format(difference[0]),
                             "{:.4g}".format(difference[1]),
                             "{:.4g}".format(difference[2]),
                             "{:.4g}".format(difference[3])
                            ]
            
            # If there were any differences plot them out
            if change:
                self.plotDifferences(plotVars, testFile, benchFile)

        return bitDict


    ## plotDifferences
    #
    #  When a bit4bit test fails the differences between the datasets need to be
    #  printed out so that a user can inspect them.
    #
    #  input:
    #    @param plotVars: the variables which differ between datasets
    #    @param testFile: path to the model output NetCDF file
    #    @param benchFile: path to the benchmark output NetCDF file
    #
    def plotDifferences(self, plotVars, testFile, benchFile):
        for var in plotVars:
            outFile = livv.imgDir + os.sep + self.getName() + os.sep + "bit4bit" + os.sep + testFile.split(os.sep)[-1] + "." + var + ".png"
           
            nclfunc.plot_diff(var, testFile, benchFile, outFile)

            

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
        imgDir = indexDir + "/imgs/"

        # Grab all of our images
        testImgDir = livv.imgDir + os.sep + self.getName()
        testImages = [os.path.basename(img) for img in glob.glob(testImgDir + os.sep + "*.png")]
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + "/*.jpg")])
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + "/*.svg")])

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
        page = open(livv.testDir + '/' + self.getName() + '.html', "w")
        page.write(outputText)
        page.close()


## TestSummary provides LIVV the ability to assemble the overview and main page.
#
#  The TestSummary class does not strictly fall under the category of a test
#  but can take advantage of the infrastructure that the AbstractTest class
#  provides.
#
class TestSummary(AbstractTest):


    ## Constructor
    #
    def __init__(self):
        return

    ## Return the name of the test
    # 
    def getName(self):
        return "test summary"

    ## Prepare the index of the website.
    #
    #  input:
    #    @param testsRun: the top level names of each of the tests run
    #
    def webSetup(self, testsRun):
        # Check if we need to back up an old run
        if os.path.exists(livv.indexDir):
            response = raw_input("Found a duplicate of the output directory.  Would you like to create a backup before overwriting? (y/n)")
            if response in ["yes", "Yes", "YES", "YEs", "y", "Y"]:
                if os.path.exists(livv.indexDir + "_backup"):
                    shutil.rmtree(livv.indexDir + "_backup")
                shutil.copytree(livv.indexDir, livv.indexDir + "_backup")
            else:
                shutil.rmtree(livv.indexDir)

        # Create directory structure
        for siteDir in [livv.indexDir, livv.testDir]:
            if not os.path.exists(siteDir):
                os.mkdir(siteDir);

        # Copy over css && imgs directories from source
        if os.path.exists(livv.indexDir + "/css"): shutil.rmtree(livv.indexDir + "/css")
        shutil.copytree(livv.websiteDir + "/css", livv.indexDir + "/css")
        if os.path.exists(livv.indexDir + "/imgs"): shutil.rmtree(livv.indexDir + "/imgs")
        shutil.copytree(livv.websiteDir + "/imgs", livv.indexDir + "/imgs")

        # Set up imgs directory to have sub-directories for each test
        for test in testsRun:
            if not os.path.exists(livv.imgDir + os.sep + test + os.sep + "bit4bit"):
                os.makedirs(livv.imgDir + os.sep + test + os.sep + "bit4bit")


    def generate(self, testsRun, testMapping, testSummary):
        # Where to look for page templates
        templateLoader = jinja2.FileSystemLoader(searchpath=livv.templateDir)
        templateEnv = jinja2.Environment(loader=templateLoader)

        # Create the index page
        templateFile = "/index.html"
        template = templateEnv.get_template(templateFile)

        templateVars = {"indexDir" : livv.indexDir,
                        "testsRun" : testsRun,
                        "testMapping" : testMapping,
                        "testSummary" : testSummary,
                        "timestamp" : livv.timestamp,
                        "user" : livv.user,
                        "comment" : livv.comment,
                        "cssDir" : "css", 
                        "imgDir" : "imgs"}

        # Write out the index page
        outputText = template.render(templateVars)
        page = open(livv.indexDir + "/index.html", "w")
        page.write(outputText)
        page.close()

    # Override the abstract methods with empty calls    
    def run(self, test):
        pass


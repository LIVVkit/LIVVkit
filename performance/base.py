'''
The AbstractTest class defines several methods that each test class must implement

Created on Apr 21, 2015

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

## Provide base functionality for a Performance test
#
#  Each test within LIVV needs to be able to run specific test code, and
#  generate its output.  Tests inherit a common method of generating 
#  scaling plots
#
class AbstractTest(object):
    __metaclass__ = ABCMeta

    ## Constructor
    #
    def __init__(self):
        self.name = "default"
        self.testsRun = []

        # Summary of plots generated
        self.plotDetails = dict()

        # Mapping of tests to files
        self.fileTestDetails = dict()

        # Summary of the configuration files parsed
        self.modelConfigs, self.benchConfigs = dict(), dict()

        # Summary of the timing data parsed
        self.modelTimingData, self.benchTimingData = dict(), dict()

        # A list of some key indicators 
        self.summary = dict()

    ## Definition for the general test run
    #
    #  input:
    #    @param test : the string indicator of the test to run
    #
    @abstractmethod
    def run(self, test):
        pass

    ## Generate scaling plots
    #
    #  Generates scaling plots for each variable and dycore combination of a given
    #  type.
    #
    #  input:
    #    @param type : the overarching test category to generate scaling plots for (ie dome/gis)
    #
    def runScaling(self, type):
        typeString = 'scaling' + type
        self.modelTimingData[typeString] = dict()
        self.benchTimingData[typeString] = dict()
        imagesGenerated = []
        print("")
        print("  Generating scaling plots for " + type + "....")
        type = type.lower() + '_' if typeString == "scalingGIS" else type.lower()
        tests = filter(re.compile(type + ".*").search, self.modelTimingData.keys())
        resolutions = sorted([int(re.findall(r'\d+', s)[0]) for s in tests])

        # Generate all of the plots
        for var in livv.timingVars:
            for dycore in livv.dycores:
                mins, avgs, maxs, ress = [], [], [], []
                for res in sorted(resolutions):
                    # Fix string for Greenland runs
                    test = type + str(res) + 'km' if typeString == 'scalingGIS' else type + str(res)
                    # Add the data if it's available
                    if self.modelTimingData[test] != {} and \
                            self.modelTimingData[test][dycore] != {} and \
                            self.modelTimingData[test][dycore][var] != {} and \
                            len(self.modelTimingData[test][dycore][var]) == 3:
                        avgs.append(self.modelTimingData[test][dycore][var][0])
                        mins.append(self.modelTimingData[test][dycore][var][1])
                        maxs.append(self.modelTimingData[test][dycore][var][2])
                        ress.append(res)

                # If there is any data to plot, do it now
                if len(ress) != 0:
                    fig, ax = pyplot.subplots(1)
                    pyplot.title((type + " " + " scaling plot for " + var + "(" + dycore + ")").title())
                    pyplot.xlabel("Problem Size")
                    pyplot.ylabel("Time per processor (s)")
                    pyplot.xticks()
                    pyplot.yticks()
                    ax.plot(ress, avgs, color='black', ls='--')
                    ax.fill_between(ress, mins, maxs, alpha=0.25)
                    pyplot.savefig(livv.imgDir + os.sep + self.name + os.sep + type + "_" + dycore + "_" + var + "_" + "_scaling" + ".png")
                    imagesGenerated.append( [type + "_" + dycore + "_" + var + "_" + "_scaling" + ".png", "Scaling plot for " + dycore + " " + var])

        # Record the plots
        self.plotDetails[typeString] = imagesGenerated


    ## Creates the output test page
    #
    #  The generate method will create a {{test}}.html page in the output directory.
    #  This page will contain a detailed list of the results from LIVV.  Details
    #  from the run are pulled from two locations.  Global definitions that are 
    #  displayed on every page, or used for navigation purposes are imported
    #  from the main livv.py module.  All test specific information is supplied
    #  via class variables.
    #
    #  \note Paths that are contained in templateVars should not be using os.sep
    #        since they are for html.
    #
    def generate(self):
        # Set up jinja related variables
        templateLoader = jinja2.FileSystemLoader(searchpath=livv.templateDir)
        templateEnv = jinja2.Environment(loader=templateLoader, extensions=["jinja2.ext.do",])
        templateFile = "/performance_test.html"
        template = templateEnv.get_template(templateFile)

        # Set up relative paths
        indexDir = ".."
        cssDir = indexDir + "/css"
        imgDir = indexDir + "/imgs"

        # Grab all of our images
        testImgDir = livv.imgDir + os.sep + self.name
        testImages = [os.path.basename(img) for img in glob.glob(testImgDir + os.sep + "*.png")]
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + os.sep +"*.jpg")])
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + os.sep +"*.svg")])

        # Set up the template variables  
        templateVars = {"timestamp" : livv.timestamp,
                        "user" : livv.user,
                        "comment" : livv.comment,
                        "testName" : self.name,
                        "indexDir" : indexDir,
                        "cssDir" : cssDir,
                        "imgDir" : imgDir,
                        "testDescription" : self.description,
                        "testsRun" : self.testsRun,
                        "testHeader" : livv.parserVars,
                        "testDetails" : self.fileTestDetails,
                        "plotDetails" : self.plotDetails,
                        "modelConfigs" : self.modelConfigs,
                        "benchConfigs" : self.benchConfigs,
                        "modelTimingData" : self.modelTimingData,
                        "benchTimingData" : self.benchTimingData,
                        "testImages" : testImages}
        outputText = template.render( templateVars )
        page = open(livv.indexDir + os.sep + "performance" + os.sep + self.name + '.html', "w")
        page.write(outputText)
        page.close()

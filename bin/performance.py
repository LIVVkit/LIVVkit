'''
Master module for performance test cases

Created on Dec 8, 2014

@author: arbennett
'''

import re
import os
import sys
import glob
import itertools
import jinja2
import matplotlib.pyplot as pyplot

import livv
from bin.test import AbstractTest
from bin.parser import Parser


## A mapping between the options available at runtime and the test cases to run
#
cases = {'none' : [],
         'small' : ['dome60', 'gis_4km'],
         'medium' : ['dome120', 'gis_2km'],
         'large' : ['dome240', 'gis_1km'],
         'scalingDome' : ['dome60', 'dome120', 'dome240', 'dome500', 'scalingDome'],
         'scalingGIS' : ['gis_4km', 'gis_2km', 'gis_1km', 'scalingGIS'],
         'scalingAll' : ['dome60', 'dome120', 'dome240', 'dome500', 'scalingDome', 'gis_4km', 'gis_2km', 'gis_1km', 'scalingGIS']
        }

## Get the available options for performance testing
#
def choices():
    return list( cases.keys() )

## Get the tests that will be run for performance testing
#
def choose(key):
    return cases[key]

## Main class for handling performance test cases.
#
#  The performance test cases inherit functionality from AbstractTest for checking
#  bit-for-bittedness as well as for parsing standard output from a model run.
#
class Test(AbstractTest):

    ## Constructor
    #
    def __init__(self):
        super(self.__class__, self).__init__()

        # Structure for these is:
        #  {*TimingData : {testName : {dycoreType : {solverVariable : [avg, min, max] } } } } 
        self.modelTimingData = dict()
        self.benchTimingData = dict()

        # Describe what the performance tests are all about
        self.name = "performance"
        self.description = "Tests the performance of various test cases." 


    ## Returns the name of the test
    #
    #  output:
    #    @returns name : performance
    #
    def getName(self):
        return self.name


    ## Runs the performance specific test case.
    #
    #  When running a test this call will record the specific test case
    #  being run.  Each specific test case string is mapped to the
    #  method that will be used to run the actual test case.
    #
    #  input:
    #    @param testCase : the string indicator of the test to run
    #
    def run(self, testCase):
        # Map the case names to the case functions
        self.testsRun.append(testCase)
        splitCase = ["".join(x) for _, x in itertools.groupby(testCase, key=str.isdigit)]
        if len(splitCase) == 1: 
            splitCase = filter(None, re.split("([A-Z][^A-Z]*)", testCase))
        perfType = splitCase[0]
        resolution = "".join(splitCase[1:])
        callDict = {'dome' : self.runDomePerformance,
                    'gis_' : self.runGisPerformance,
                    'scaling' : self.runScaling}

        # Call the correct function
        if callDict.has_key(perfType):
            callDict[perfType](resolution)
        else: 
            print("  Could not find test code for performance test: " + testCase)


    ## Dome Performance Testing
    #
    #  input:
    #    @param resolution: the size of the test being analyzed
    #
    def runDomePerformance(self, resolution):
        print("")
        print("  Dome " + resolution + " performance tests in progress....")  

        # Search for the std output files
        perfDir = livv.performanceDir + os.sep + "dome" + resolution + os.sep + livv.dataDir 
        perfBenchDir = livv.performanceDir + os.sep + "bench" + os.sep + "dome" + resolution + os.sep + livv.dataDir

        if not (os.path.exists(perfDir) and os.path.exists(perfBenchDir)):
            print("    Could not find data for Dome " + resolution + " tests!  Tried to find data in:")
            print("      " + perfDir)
            print("      " + perfBenchDir)
            print("    Continuing with next test....")
            return 1

        files = os.listdir(perfDir)
        test = re.compile("^out." + resolution + ".((glide)|(glissade))$")
        files = filter(test.search, files)

        # Process the configure files
        configPath = os.sep + ".." + os.sep + "configure_files"
        domeParser = Parser()
        self.modelConfigs['dome' + resolution], self.benchConfigs['dome' + resolution] = \
                domeParser.parseConfigurations(perfDir + configPath, perfBenchDir + configPath)

        # Scrape the details from each of the files and store some data for later
        perfDetails, perfFiles = [], []
        for file in files:
            perfDetails.append(domeParser.parseOutput(perfDir + os.sep +  file))
            perfFiles.append(file)
        self.fileTestDetails["dome" + resolution] = zip(perfFiles, perfDetails)
        self.bitForBitDetails["dome" + resolution]= dict()

        # Go through and pull in the timing data
        print("")
        print("        Model Timing Summary:")
        print("      --------------------------------------------------------------------")
        self.modelTimingData['dome' + resolution] = domeParser.parseTimingSummaries(perfDir)
        print("")
        print("        Benchmark Timing Summary:")
        print("      --------------------------------------------------------------------")
        self.benchTimingData['dome' + resolution] = domeParser.parseTimingSummaries(perfBenchDir)

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = domeParser.getParserSummary()

        # Create the plots
        numberPlots = 0 #self.plotPerformance(resolution)

        numberBitMatches, numberBitTests = 0, 0

        self.summary['dome' + resolution] = [numberPlots, numberOutputFiles,
                                             numberConfigMatches, numberConfigTests,
                                             numberBitMatches, numberBitTests]


    ## Greenland Ice Sheet Performance Testing
    #
    #  input:
    #    @param resolution : the resolution of the test data
    #
    def runGisPerformance(self, resolution):
        print("")
        print("  Greenland Ice Sheet " + resolution + " performance  tests in progress....")

        # The locations for the data
        perfDir = livv.performanceDir + os.sep + "gis_" + resolution + os.sep + livv.dataDir
        perfBenchDir = livv.performanceDir + os.sep + "bench" + os.sep + 'gis_' + resolution + os.sep + livv.dataDir

        # Make sure that there is some data
        if not (os.path.exists(perfDir) and os.path.exists(perfBenchDir)):
            print("    Could not find data for GIS " + resolution + " tests!  Tried to find data in:")
            print("      " + perfDir)
            print("      " + perfBenchDir)
            print("    Continuing with next test....")
            return 1

        # Search for the std output files
        files = os.listdir(perfDir)
        test = re.compile("^out.gis." + resolution + ".((albany)|(glissade))$")
        files = filter(test.search, files)

        # Process the configure files
        configPath = os.sep + ".." + os.sep + "configure_files"
        gisParser = Parser()
        self.modelConfigs['gis_' + resolution], self.benchConfigs['gis_' + resolution] = \
                gisParser.parseConfigurations(perfDir + configPath, perfBenchDir + configPath)

        # Scrape the details from each of the files and store some data for later
        perfDetails, perfFiles = [], []
        for file in files:
            perfDetails.append(gisParser.parseOutput(perfDir + os.sep +  file))
            perfFiles.append(file)
        self.fileTestDetails['gis_' + resolution] = zip(perfFiles, perfDetails)
        self.bitForBitDetails['gis_' + resolution]= dict()

        # Go through and pull in the timing data
        print("")
        print("        Model Timing Summary:")
        print("      --------------------------------------------------------------------")
        self.modelTimingData['gis_' + resolution] = gisParser.parseTimingSummaries(perfDir)
        print("")
        print("        Benchmark Timing Summary:")
        print("      --------------------------------------------------------------------")
        self.benchTimingData['gis_' + resolution] = gisParser.parseTimingSummaries(perfBenchDir)

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = gisParser.getParserSummary()

        # Create the plots
        numberPlots = 0 #self.plotPerformance(resolution)

        numberBitMatches, numberBitTests = 0, 0

        self.summary['gis_' + resolution] = [numberPlots, numberOutputFiles,
                                             numberConfigMatches, numberConfigTests,
                                             numberBitMatches, numberBitTests]


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

        for var in livv.timingVars:
            for dycore in livv.dycores:
                mins, avgs, maxs, ress = [], [], [], []
                bmins, bavgs, bmaxs, bress = [], [], [], []
                for res in sorted(resolutions):
                    test = type + str(res) + 'km' if typeString == 'scalingGIS' else type + str(res)
                    if self.modelTimingData[test] != {} and \
                            self.modelTimingData[test][dycore] != {} and \
                            self.modelTimingData[test][dycore][var] != {} and \
                            len(self.modelTimingData[test][dycore][var]) == 3:
                        avgs.append(self.modelTimingData[test][dycore][var][0])
                        mins.append(self.modelTimingData[test][dycore][var][1])
                        maxs.append(self.modelTimingData[test][dycore][var][2])
                        ress.append(res)
                if len(ress) != 0:
                    fig, ax = pyplot.subplots(1)
                    pyplot.title((type + " " + " scaling plot for " + var + "(" + dycore + ")").title())
                    pyplot.xlabel("Problem Size")
                    pyplot.ylabel("Time (s)")
                    pyplot.xticks()
                    pyplot.yticks()
                    ax.plot(ress, avgs, color='black', ls='--')
                    ax.fill_between(ress, mins, maxs, alpha=0.25)
                    pyplot.savefig(livv.imgDir + os.sep + self.getName() + os.sep + type + "_" + dycore + "_" + var + "_" + "_scaling" + ".png")
                    imagesGenerated.append( [type + "_" + dycore + "_" + var + "_" + "_scaling" + ".png", "Scaling plot for " + dycore + " " + var])
        self.plotDetails[typeString] = imagesGenerated

    ## This is a placeholder
    #
    def summary(self):
        print("    This is a placeholder....")


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
        templateFile = "/perf_test.html"
        template = templateEnv.get_template(templateFile)

        # Set up relative paths
        indexDir = ".."
        cssDir = indexDir + "/css"
        imgDir = indexDir + "/imgs"

        # Grab all of our images
        testImgDir = livv.imgDir + os.sep + self.getName()
        testImages = [os.path.basename(img) for img in glob.glob(testImgDir + os.sep + "*.png")]
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + os.sep +"*.jpg")])
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + os.sep +"*.svg")])

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
                        "testDetails" : self.fileTestDetails,
                        "plotDetails" : self.plotDetails,
                        "modelConfigs" : self.modelConfigs,
                        "benchConfigs" : self.benchConfigs,
                        "modelTimingData" : self.modelTimingData,
                        "benchTimingData" : self.benchTimingData,
                        "imgDir" : imgDir,
                        "testImages" : testImages}
        outputText = template.render( templateVars )
        page = open(livv.testDir + '/' + self.getName() + '.html', "w")
        page.write(outputText)
        page.close()

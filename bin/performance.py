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


##
#
cases = {'none' : [],
         'small' : ['dome60', 'gis_4km'],
         'medium' : ['dome120', 'gis_2km'],
         'large' : ['dome240', 'gis_1km'],
         'scaling' : ['dome60', 'dome120', 'dome240', 'dome500', 'dome1000', 'scalingDome']
        }

##
#
def choices():
    return list( cases.keys() )

##
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
        # Common run     
        self.testsRun.append(testCase)

        # Map the case names to the case functions
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

        # More common postprocessing
        return


    ## Dome Performance Testing
    #
    #
    def runDomePerformance(self, resolution):
        print("")
        print("  Dome " + resolution + " performance tests in progress....")  

        # Search for the std output files
        perfDir = livv.performanceDir + os.sep + "dome" + resolution + os.sep + livv.dataDir 
        perfBenchDir = livv.performanceDir + os.sep + "bench" + os.sep + "dome" + resolution + os.sep + livv.dataDir
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
    #  
    #
    #  input:
    #    @param resolution : the resolution of the test data
    #
    def runGisPerformance(self, resolution):
        print("")
        print("  Greenland Ice Sheet " + resolution + " performance  tests in progress....")

        # Search for the std output files
        perfDir = livv.performanceDir + os.sep + "gis_" + resolution + os.sep + livv.dataDir
        perfBenchDir = livv.performanceDir + os.sep + "bench" + os.sep + 'gis_' + resolution + os.sep + livv.dataDir
        if os.path.exists(perfDir) and os.path.exists(perfBenchDir):
            files = os.listdir(perfDir)
            test = re.compile("^out.gis." + resolution + ".((albany)|(glissade))$")
            files = filter(test.search, files)
        else:
            files = []
            print("    Could not find model and benchmark directories for gis_" + resolution +".")

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
        self.modelTimingData['scaling' + type] = dict()
        self.benchTimingData['scaling' + type] = dict()
        type = type.lower()
        print("")
        print("  Generating scaling plots for " + type + "....")
        tests = filter(re.compile(type + ".*").search, self.modelTimingData.keys())
        resolutions = sorted([int(re.findall(r'\d+', s)[0]) for s in tests])
        for var in livv.timingVars:
            for dycore in livv.dycores:
                mins, avgs, maxs = [], [], []
                for res in resolutions:
                    test = type + str(res)
                    if self.modelTimingData[test][dycore][var] != None and len(self.modelTimingData[test][dycore][var]) == 3:
                        avgs.append(self.modelTimingData[test][dycore][var][0])
                        mins.append(self.modelTimingData[test][dycore][var][1])
                        maxs.append(self.modelTimingData[test][dycore][var][2])
                    else:
                        avgs.append(0.0)
                        mins.append(0.0)
                        maxs.append(0.0)
                fig, ax = pyplot.subplots(1)
                ax.plot(resolutions, avgs, color='black', ls='--')
                ax.fill_between(resolutions, mins, maxs, alpha=0.25)
                pyplot.savefig(livv.imgDir + os.sep + self.getName() + os.sep + type + "_" + dycore + "_" + var + "_" + "_scaling" + ".png")


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

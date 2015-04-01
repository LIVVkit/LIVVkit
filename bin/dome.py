'''
Master module for dome test cases

Created on Dec 8, 2014

@author: arbennett
'''

import re
import os
import subprocess


cases = {'none'   : [],
         'diagnostic' : ['dome30/diagnostic'],
         'evolving'  : ['dome30/evolving'],
         'all'    : ['dome30/diagnostic', 'dome30/evolving'],}

def choices():
    return list( cases.keys() )

def choose(key):
    return cases[key]


import livv
from bin.test import AbstractTest
from bin.parser import Parser

## Main class for handling dome test cases.
#
#  The dome test cases inherit functionality from AbstractTest for checking 
#  bit-for-bittedness as well as for parsing standard output from a model run.
#  This class handles evolving and diagnostic variations of the dome case.
#
class Test(AbstractTest):

    ## Constructor
    #
    def __init__(self):
        super(self.__class__, self).__init__()

        # Describe what the dome tests are all about
        self.name = "dome"
        self.description = "3-D paraboloid dome of ice with a circular, 60 km" + \
                      " diameter base sitting on a flat bed. The horizontal" + \
                      " spatial resolution studies are 2 km, 1 km, 0.5 km" + \
                      " and 0.25 km, and there are 10 vertical levels. For this" + \
                      " set of experiments a quasi no-slip basal condition in" + \
                      " imposed by setting. A zero-flux boundary condition is" + \
                      " applied to the dome margins. "


    ## Returns the name of the test
    #
    #  output:
    #    @returns name : Dome
    #
    def getName(self):
        return self.name


    ## Runs the dome specific test case.  
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
        splitCase = testCase.split('/')
        type, resolution = splitCase[-1], splitCase[0][4:]

        # Make sure LIVV can find the data
        modelDir = livv.inputDir + os.sep + "dome" + resolution + os.sep + type + os.sep + livv.dataDir
        benchDir = livv.benchmarkDir + os.sep + "dome" + resolution + os.sep + type + os.sep + livv.dataDir
        if not (os.path.exists(modelDir) and os.path.exists(benchDir)):
            print("    Could not find data for dome" + resolution + " " + type + " tests!  Tried to find data in:")
            print("      " + modelDir)
            print("      " + benchDir)
            print("    Continuing with next test....")
            self.bitForBitDetails['dome' + resolution + os.sep + type] = {'Data not found': ['SKIPPED', '0.0']}
            return 1 # zero returns a problem        
        self.runDome(resolution, type, modelDir, benchDir)


    ## Perform V&V on the evolving dome case
    #
    #  Runs the dome evolving V&V for a given resolution.  First parses through all 
    #  of the standard output files for the given test case, then generates plots via
    #  the plotEvolving function.  Finishes up by doing bit for bit comparisons with
    #  the benchmark files.
    #
    #  input:
    #    @param resolution: The resolution of the test cases to look in.
    #                       (eg resolution == 30 -> reg_test/dome30/evolving)
    #    @param type: The type of test case (evolving, diagnostic, etc)
    #    @param modelDir: the location of the model run data
    #    @param benchDir: the location of the benchmark data
    #
    def runDome(self, resolution, type, modelDir, benchDir):
        # Process the configure files
        print("  Dome " + type + " test in progress....")
        configPath = os.sep + ".." + os.sep + "configure_files"
        domeParser = Parser()
        self.modelConfigs['dome' + resolution + os.sep + type], self.benchConfigs['dome' + resolution + os.sep + type] = \
                domeParser.parseConfigurations(modelDir + configPath, benchDir + configPath)

        # Scrape the details from each of the files and store some data for later
        try:
            files = os.listdir(modelDir)
        except:
            print("    Could not find model and benchmark directories for dome" + resolution + "/" + type)
            files = []
        test = re.compile(".*((small)|(large))_proc")
        files = filter(test.search, files)
        domeDetails, domeFiles = [], []
        for file in files:
            domeDetails.append(domeParser.parseOutput(modelDir + os.sep +  file))
            domeFiles.append(file)
        self.fileTestDetails["dome" + resolution + os.sep + type] = zip(domeFiles, domeDetails)

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = domeParser.getParserSummary()

        # Create the plots
        numberPlots = 0 #self.plotEvolving(resolution)

        # Run bit for bit test
        numberBitMatches, numberBitTests = 0, 0
        self.bitForBitDetails['dome' + resolution + os.sep + type] = self.bit4bit(self.getName(), modelDir, benchDir)
        for key, value in self.bitForBitDetails['dome' + resolution + os.sep + type].iteritems():
            print ("    {:<40} {:<10}".format(key,value[0]))
            if value[0] == "SUCCESS": numberBitMatches+=1
            numberBitTests+=1

        self.summary['dome' + resolution + os.sep + type] = [numberPlots, numberOutputFiles,
                                                             numberConfigMatches, numberConfigTests,
                                                             numberBitMatches, numberBitTests]

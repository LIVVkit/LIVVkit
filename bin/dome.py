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
        # Common run     
        self.testsRun.append(testCase)

        # Map the case names to the case functions
        splitCase = testCase.split('/')
        type = splitCase[-1]
        resolution = splitCase[0][4:]
        callDict = {'diagnostic' : self.runDiagnostic,
                    'evolving' : self.runEvolving}

        # Make sure LIVV can find the data
        testDir = livv.inputDir + os.sep + "dome" + resolution + os.sep + type + os.sep + livv.dataDir 
        benchDir = livv.benchmarkDir + os.sep + "dome" + resolution + os.sep + type + os.sep + livv.dataDir
        if not (os.path.exists(testDir) and os.path.exists(benchDir)):
            print("    Could not find data for dome" + resolution + " " + type + " tests!  Tried to find data in:")
            print("      " + testDir)
            print("      " + benchDir)
            print("    Continuing with next test....")
            self.bitForBitDetails['dome' + resolution + os.sep + type] = {'Data not found': ['SKIPPED', '0.0']}
            return 1 # zero returns a problem        

        # Call the correct function
        if callDict.has_key(type):
            callDict[type](resolution, testDir, benchDir)
        else: 
            print("  Could not find test code for dome test: " + testCase)


    ## Perform V&V on the diagnostic dome case
    #
    #  Runs the dome diagnostic V&V for a given resolution.  First parses through all 
    #  of the standard output files for the given test case, then generates plots via
    #  the plotDiagnostic function.  Finishes up by doing bit for bit comparisons with
    #  the benchmark files.
    #
    #  input:
    #    @param resolution: The resolution of the test cases to look in. 
    #                       (eg resolution == 30 -> reg_test/dome30/diagnostic)
    # 
    def runDiagnostic(self, resolution, testDir, benchDir):
        print("  Dome Diagnostic test in progress....")

        diagnosticDir = livv.inputDir + os.sep + "dome" + resolution + os.sep + "diagnostic" + os.sep + livv.dataDir
        diagnosticBenchDir = livv.benchmarkDir + os.sep + "dome" + resolution + os.sep + "diagnostic" + os.sep + livv.dataDir

        # Process the configure files
        configPath = os.sep + ".." + os.sep + "configure_files"
        domeParser = Parser()
        self.modelConfigs['dome' + resolution + os.sep + "diagnostic"], self.benchConfigs['dome' + resolution + os.sep + "diagnostic"] = \
            domeParser.parseConfigurations(diagnosticDir + configPath, diagnosticBenchDir + configPath)

        # Search for the standard output files
        try:
            files = os.listdir(diagnosticDir)
        except:
            print("    Could not find model and benchmark directories for dome" + resolution + "/diagnostic")
            files = []
        test = re.compile(".*[0-9]proc")
        files = filter(test.search, files)

        # Scrape the details from each of the files and store some data for later
        diagnosticDetails, diagnosticFiles = [], []
        for file in files:
            diagnosticDetails.append(domeParser.parseOutput(diagnosticDir + os.sep +  file))
            diagnosticFiles.append(file)
        self.fileTestDetails["dome" + resolution + os.sep + "diagnostic"] = zip(diagnosticFiles, diagnosticDetails)

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = domeParser.getParserSummary()

        # Create the plots and record the number of plots
        numberPlots = 0 #self.plotDiagnostic(resolution)

        # Run bit for bit tests
        numberBitTests, numberBitMatches = 0, 0
        self.bitForBitDetails['dome' + resolution + os.sep + 'diagnostic'] = self.bit4bit(self.getName(), testDir, benchDir)
        for key, value in self.bitForBitDetails['dome' + resolution + os.sep + 'diagnostic'].iteritems():
            print ("    {:<40} {:<10}".format(key,value[0]))
            if value[0] == "SUCCESS": numberBitMatches+=1
            numberBitTests+=1

        self.summary['dome' + resolution + os.sep + 'diagnostic'] = [numberPlots, numberOutputFiles,
                                                                     numberConfigMatches, numberConfigTests,
                                                                     numberBitMatches, numberBitTests]


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
    # 
    def runEvolving(self, resolution, testDir, benchDir):
        print("  Dome Evolving test in progress....")  

        # Search for the std output files
        evolvingDir = livv.inputDir + os.sep + "dome" + resolution + os.sep + "evolving" + os.sep + livv.dataDir 
        evolvingBenchDir = livv.benchmarkDir + os.sep + "dome" + resolution + os.sep + "evolving" + os.sep + livv.dataDir

        try:
            files = os.listdir(evolvingDir)
        except:
            print("    Could not find model and benchmark directories for dome" + resolution + "/evolving")
            files = []
        test = re.compile(".*((small)|(large))_proc")
        files = filter(test.search, files)

        # Process the configure files
        configPath = os.sep + ".." + os.sep + "configure_files"
        domeParser = Parser()
        self.modelConfigs['dome' + resolution + os.sep + "evolving"], self.benchConfigs['dome' + resolution + os.sep + "evolving"] = \
                domeParser.parseConfigurations(evolvingDir + configPath, evolvingBenchDir + configPath)

        # Scrape the details from each of the files and store some data for later
        evolvingDetails, evolvingFiles = [], []
        for file in files:
            evolvingDetails.append(domeParser.parseOutput(evolvingDir + os.sep +  file))
            evolvingFiles.append(file)
        self.fileTestDetails["dome" + resolution + os.sep + "evolving"] = zip(evolvingFiles, evolvingDetails)

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = domeParser.getParserSummary()

        # Create the plots
        numberPlots = 0 #self.plotEvolving(resolution)

        # Run bit for bit test
        numberBitMatches, numberBitTests = 0, 0
        self.bitForBitDetails['dome' + resolution + os.sep +'evolving'] = self.bit4bit(self.getName(), testDir, benchDir)
        for key, value in self.bitForBitDetails['dome' + resolution + os.sep + 'evolving'].iteritems():
            print ("    {:<40} {:<10}".format(key,value[0]))
            if value[0] == "SUCCESS": numberBitMatches+=1
            numberBitTests+=1

        self.summary['dome' + resolution + os.sep + 'evolving'] = [numberPlots, numberOutputFiles,
                                                                     numberConfigMatches, numberConfigTests,
                                                                     numberBitMatches, numberBitTests]

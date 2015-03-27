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
    #    @param test : the string indicator of the test to run
    #
    def run(self, test):
        # Common run     
        self.testsRun.append(test)

        # Map the case names to the case functions
        splitCase = test.split('/')
        dOrE = splitCase[-1]
        resolution = splitCase[0][4:]
        callDict = {'diagnostic' : self.runDiagnostic,
                    'evolving' : self.runEvolving}

        # Make sure LIVV can find the data
        testDir = livv.inputDir + os.sep + "dome" + resolution + os.sep + dOrE + os.sep + livv.dataDir 
        benchDir = livv.benchmarkDir + os.sep + "dome" + resolution + os.sep + dOrE + os.sep + livv.dataDir
        if not (os.path.exists(testDir) and os.path.exists(benchDir)):
            print("    Could not find data for dome" + resolution + " " + dOrE + " tests!  Tried to find data in:")
            print("      " + testDir)
            print("      " + benchDir)
            print("    Continuing with next test....")
            self.bitForBitDetails['dome' + resolution + os.sep + dOrE] = {'Data not found': ['SKIPPED', '0.0']}
            return 1 # zero returns a problem        

        # Call the correct function
        if callDict.has_key(dOrE):
            callDict[dOrE](testDir, benchDir, resolution)
        else: 
            print("  Could not find test code for dome test: " + test)


    ## Perform V&V on the diagnostic dome case
    #
    #  Runs the dome diagnostic V&V for a given resolution.  First parses through all 
    #  of the standard output files for the given test case, then generates plots via
    #  the plotDiagnostic function.  Finishes up by doing bit for bit comparisons with
    #  the benchmark files.
    #
    #  input:
    #    @param testDir: The path to the test data
    #    @param benchDir: The path to the benchmark data
    #    @param resolution: The resolution of the test cases to look in. 
    #                       (eg resolution == 30 -> reg_test/dome30/diagnostic)
    # 
    def runDiagnostic(self, testDir, benchDir, resolution):
        print("  Dome Diagnostic test in progress....")

        testName = 'dome' + resolution + os.sep + 'diagnostic'
        
        # Process the configure files
        configPath = os.sep + ".." + os.sep + "configure_files"
        domeParser = Parser()
        self.modelConfigs[testName], self.benchConfigs[testName] = \
            domeParser.parseConfigurations(testDir + configPath, benchDir + configPath)

        # Search for the standard output files
        try:
            files = os.listdir(testDir)
        except:
            print("    Could not find model and benchmark directories for" + testName)
            files = []
        test = re.compile(".*[0-9]proc")
        files = filter(test.search, files)

        # Scrape the details from each of the files and store some data for later
        diagnosticDetails, diagnosticFiles = [], []
        for file in files:
            diagnosticDetails.append(domeParser.parseOutput(testDir + os.sep +  file))
            diagnosticFiles.append(file)
        self.fileTestDetails[testName] = zip(diagnosticFiles, diagnosticDetails)

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = domeParser.getParserSummary()

        # Create the plots and record the number of plots
        numberPlots = 0 #self.plotDiagnostic(resolution)

        # Run bit for bit tests
        numberBitTests, numberBitMatches = 0, 0
        self.bitForBitDetails[testName] = self.bit4bit(testName, testDir, benchDir)
        for key, value in self.bitForBitDetails[testName].iteritems():
            print ("    {:<30} {:<10}".format(key,value[0]))
            if value[0] == "SUCCESS": numberBitMatches+=1
            numberBitTests+=1

        self.summary['dome' + resolution + os.sep + 'diagnostic'] = [numberPlots, numberOutputFiles,
                                                                     numberConfigMatches, numberConfigTests,
                                                                     numberBitMatches, numberBitTests]


    ## Plot some details from the diagnostic dome case
    # 
    #  Plots a comparison of the norm of the velocity for several cases of the evolving
    #  dome test case.
    #
    #  input:
    #    @param resolution: The resolution of the test cases to look in.
    #                       (eg resolution == 30 -> reg_test/dome30/diagnostic)
    #
    #  output:
    #    @return the number of plots generated
    #
    def plotDiagnostic(self, resolution):
        # Set up where we are going to look for things
        ncl_path = livv.cwd + os.sep + "plots"
        img_path = livv.imgDir + os.sep + "dome"
        plotFile = ncl_path + os.sep + 'dome30' + os.sep + 'dome30dvel.ncl'
        benchDir = livv.benchmarkDir + os.sep + 'dome' + resolution + os.sep + 'diagnostic' + os.sep + livv.dataDir
        modelDir = livv.inputDir + os.sep + 'dome' + resolution + os.sep + 'diagnostic' + os.sep + livv.dataDir

        # The arguments to pass in to the ncl script
        description = "Velocity Comparison Plots"
        bench1 = 'STOCK1 = addfile(\"'+ benchDir + os.sep + 'dome.1.nc\", \"r\")'
        bench4 = 'STOCK4 = addfile(\"'+ benchDir + os.sep + 'dome.4.nc\", \"r\")'
        test1  = 'VAR1 = addfile(\"' + modelDir + os.sep + 'dome.1.nc\", \"r\")'
        test4  = 'VAR4 = addfile(\"' + modelDir + os.sep + 'dome.4.nc\", \"r\")'
        name = 'dome30dvel.png'
        path = 'PNG = "' + img_path + os.sep + name + '"'

        # The plot command to run
        plotCommand = "ncl '" + bench1 + "' '" + bench4 + "'  '" + test1 + "' '" + test4 + \
                    "' '" + path + "' " + plotFile 

        # Be cautious about running subprocesses
        call = subprocess.Popen(plotCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdOut, stdErr = call.stdout.read(), call.stderr.read()

        if os.path.exists(img_path + os.sep + name):
            print("    Plot details saved to " + img_path + " as " + name)
            self.plotDetails['dome' + resolution + os.sep + 'diagnostic'] = [[name, description]]
            return 1
        else:
            print("****************************************************************************")
            print("    Error saving " + name + " to " + img_path)
            print("    Details of the error follow: ")
            print("")
            print(stdOut)
            print(stdErr)
            print("****************************************************************************")
            return 0


    ## Perform V&V on the evolving dome case
    #
    #  Runs the dome evolving V&V for a given resolution.  First parses through all 
    #  of the standard output files for the given test case, then generates plots via
    #  the plotEvolving function.  Finishes up by doing bit for bit comparisons with
    #  the benchmark files.
    #
    #  input:
    #    @param testDir: The path to the test data
    #    @param benchDir: The path to the benchmark data
    #    @param resolution: The resolution of the test cases to look in. 
    #                       (eg resolution == 30 -> reg_test/dome30/evolving)
    # 
    def runEvolving(self, testDir, benchDir, resolution):
        print("  Dome Evolving test in progress....")  

        testName = 'dome' + resolution + os.sep + 'evolving'  

        # Search for the std output files
        try:
            files = os.listdir(testDir)
        except:
            print("    Could not find model and benchmark directories for dome" + resolution + "/evolving")
            files = []
        test = re.compile(".*((small)|(large))_proc")
        files = filter(test.search, files)

        # Process the configure files
        configPath = os.sep + ".." + os.sep + "configure_files"
        domeParser = Parser()
        self.modelConfigs[testName], self.benchConfigs[testName] = \
                domeParser.parseConfigurations(testDir + configPath, benchDir + configPath)

        # Scrape the details from each of the files and store some data for later
        evolvingDetails, evolvingFiles = [], []
        for file in files:
            evolvingDetails.append(domeParser.parseOutput(testDir + os.sep +  file))
            evolvingFiles.append(file)
        self.fileTestDetails[testName] = zip(evolvingFiles, evolvingDetails)

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = domeParser.getParserSummary()

        # Create the plots
        numberPlots = 0 #self.plotEvolving(resolution)

        # Run bit for bit test
        numberBitMatches, numberBitTests = 0, 0
        self.bitForBitDetails[testName] = self.bit4bit(os.sep + testName, testDir, benchDir)
        for key, value in self.bitForBitDetails[testName].iteritems():
            print ("    {:<30} {:<10}".format(key,value[0]))
            if value[0] == "SUCCESS": numberBitMatches+=1
            numberBitTests+=1

        self.summary[testName] = [numberPlots, numberOutputFiles,
                                                                     numberConfigMatches, numberConfigTests,
                                                                     numberBitMatches, numberBitTests]


    ## Plot some details from the evolving dome case
    # 
    #  Plots a comparison of the norm of the velocity for several cases of the evolving
    #  dome test case.
    #
    #  input:
    #    @param resolution: The resolution of the test cases to look in.
    #                       (eg resolution == 30 -> reg_test/dome30/evolving)
    #
    #  output:
    #    @return the number of plots generated
    #
    def plotEvolving(self, resolution):
        # Set up where we are going to look for things
        ncl_path = livv.cwd + os.sep + "plots"
        img_path = livv.imgDir + os.sep + "dome"
        plotFile = ''+ ncl_path + os.sep + 'dome30' + os.sep + 'dome30evel.ncl'
        benchDir = livv.benchmarkDir + os.sep + 'dome' + resolution + os.sep + 'evolving' + os.sep + livv.dataDir
        modelDir = livv.inputDir + os.sep + 'dome' + resolution + os.sep + 'evolving' + os.sep + livv.dataDir

        # The arguments to pass in to the ncl script
        description = "Velocity Comparison Plot"
        bench1 = 'STOCK9 = addfile(\"'+ benchDir + os.sep + 'dome.small.nc\", \"r\")'
        bench4 = 'STOCK15 = addfile(\"'+ benchDir + os.sep + 'dome.large.nc\", \"r\")'
        test1  = 'VAR9 = addfile(\"' + modelDir + os.sep + 'dome.small.nc\", \"r\")'
        test4  = 'VAR15 = addfile(\"' + modelDir + os.sep + 'dome.large.nc\", \"r\")'
        name = 'dome' + resolution + 'evel.png'
        path = 'PNG = "' + img_path + os.sep + name + '"'

        # The plot command to run
        plotCommand = "ncl '" + bench1 + "' '" + bench4 + "'  '" + test1 + "' '" + test4 + \
                    "' '" + path + "' " + plotFile

        # Be cautious about running subprocesses
        call = subprocess.Popen(plotCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdOut, stdErr = call.stdout.read(), call.stderr.read()

        if os.path.exists(img_path + os.sep + name):
            print("    Plot details saved to " + img_path + " as " + name)
            self.plotDetails['dome' + resolution + os.sep + 'evolving'] = [[name, description]]
            return 1
        else:
            print("****************************************************************************")
            print("    Error saving " + name + " to " + img_path)
            print("    Details of the error follow: ")
            print("")
            print(stdOut)
            print(stdErr)
            print("****************************************************************************")
            return 0

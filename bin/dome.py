'''
Master module for dome test cases

Created on Dec 8, 2014

@author: arbennett
'''

import re
import os
import subprocess

import livv
from bin.test import AbstractTest
from bin.parser import Parser

## Main class for handling dome test cases.
#
#  The dome test cases inherit functionality from AbstractTest for checking 
#  bit-for-bittedness as well as for parsing standard output from a model run.
#  This class handles evolving and diagnostic variations of the dome case.
#
class Dome(AbstractTest):

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
        domeDir = livv.inputDir + os.sep + "dome" + resolution + os.sep + type + os.sep + livv.dataDir 
        domeBenchDir = livv.benchmarkDir + os.sep + "dome" + resolution + os.sep + type + os.sep + livv.dataDir
        if not (os.path.exists(domeDir) and os.path.exists(domeBenchDir)):
            print("    Could not find data for dome" + resolution + " " + type + " tests!  Tried to find data in:")
            print("      " + domeDir)
            print("      " + domeBenchDir)
            print("    Continuing with next test....")
            self.bitForBitDetails['dome' + resolution + os.sep + type] = {'Data not found': ['SKIPPED', '0.0']}
            return 1 # zero returns a problem        

        # Call the correct function
        if callDict.has_key(type):
            callDict[type](resolution)
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
    def runDiagnostic(self, resolution):
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
        self.bitForBitDetails['dome' + resolution + os.sep + 'diagnostic'] = self.bit4bit(os.sep + 'dome' + resolution + os.sep + 'diagnostic')
        for key, value in self.bitForBitDetails['dome' + resolution + os.sep + 'diagnostic'].iteritems():
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
    #    @param resolution: The resolution of the test cases to look in. 
    #                       (eg resolution == 30 -> reg_test/dome30/evolving)
    # 
    def runEvolving(self, resolution):
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
        self.bitForBitDetails['dome' + resolution + os.sep +'evolving'] = self.bit4bit(os.sep + 'dome' + resolution + os.sep + 'evolving')
        for key, value in self.bitForBitDetails['dome' + resolution + os.sep + 'evolving'].iteritems():
            print ("    {:<30} {:<10}".format(key,value[0]))
            if value[0] == "SUCCESS": numberBitMatches+=1
            numberBitTests+=1

        self.summary['dome' + resolution + os.sep + 'evolving'] = [numberPlots, numberOutputFiles,
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

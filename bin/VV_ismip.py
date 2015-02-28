'''
Master module for Ismip tests.  

Created on Dec 8, 2014

@author: arbennett
'''

import re
import os
import sys
import subprocess

import livv
from bin.VV_test import AbstractTest
from bin.VV_parser import Parser
import jinja2

## Main class for handling Ismip test cases.
#
#  The Ismip test cases inherit functionality from AbstractTest for checking 
#  bit-for-bittedness as well as for parsing standard output from a model run.
#  This class handles the Ismip-hom a and c tests for resolutions of 20km and 80km.
#
class Ismip(AbstractTest):

    ## Constructor
    #
    def __init__(self):
        super(self.__class__, self).__init__()

        self.name = "ismip"
        self.description = "The Ice Sheet Model Intercomparison Project for Higher-Order Models (ISMIP-HOM) " + \
                           "prescribes a set of experiments meant to test the implementation of higher-order" + \
                           " physics.  For more information, see <a href=http://homepages.ulb.ac.be/~fpattyn/ismip/>" +\
                           "http://homepages.ulb.ac.be/~fpattyn/ismip/</a> \n" + \
                           " Simulates steady ice flow over a surface with periodic boundary conditions"

    ## Return the name of the test
    #
    #  output:
    #    @returns name : ismip
    #
    def getName(self):
        return self.name


    ## Runs the ismip specific test case.
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

        # Make sure LIVV can find the data
        ismipDir = livv.inputDir + os.sep + testCase + os.sep + livv.dataDir 
        ismipBenchDir = livv.benchmarkDir + os.sep + testCase + os.sep + livv.dataDir
        if not (os.path.exists(ismipDir) and os.path.exists(ismipBenchDir)):
            print("    Could not find data for " + ismipDir + " tests!  Tried to find data in:")
            print("      " + ismipDir)
            print("      " + ismipBenchDir)
            print("    Continuing with next test....")
            self.bitForBitDetails[testCase] = {'Data not found': ['SKIPPED', '0.0']}
            return 1 # zero returns a problem

        # Pull some data about the test case
        splitCase = testCase.split('/')
        aOrC = splitCase[0][-1]
        resolution = splitCase[-1]

        # Pass it onto the specific run
        self.runIsmip(aOrC,resolution)


    ## Perform V&V on an ismip-hom test case
    #
    #  Runs the ismip V&V for a given case and resolution.  First parses through all
    #  of the standard output files for the given test case, then generates plots via
    #  the plot function.  Finishes up by doing bit for bit comparisons with
    #  the benchmark files.
    #
    #  input:
    #    @param aOrC: Whether we are running ismip-hom-a or ismip-hom-c
    #    @param resolution: The resolution of the test cases to look in.
    #                       (eg resolution == 30 -> reg_test/dome30/diagnostic)
    # 
    def runIsmip(self, aOrC, resolution):
        print("  Ismip-hom-" + aOrC + os.sep + resolution + " test in progress....")

        testName = 'ismip-hom-' + aOrC + os.sep + resolution
        ismipDir = livv.inputDir + os.sep + testName + os.sep + livv.dataDir
        ismipBenchDir = livv.benchmarkDir + os.sep + testName + os.sep + livv.dataDir

        # Process the configure files
        configPath = os.sep + ".." + os.sep + "configure_files"
        ismipParser = Parser()
        self.modelConfigs[testName], self.benchConfigs[testName] = \
            ismipParser.parseConfigurations(ismipDir + configPath, ismipBenchDir + configPath)

        # Search for the std output files
        files = os.listdir(ismipDir)
        test = re.compile(".*out.*[0-9]")
        files = filter(test.search, files)

        # Scrape the details from each of the files and store some data for later
        ismipDetails, ismipFiles = [], []
        for file in files:
            ismipDetails.append(ismipParser.parseOutput(ismipDir + '/' + file))
            ismipFiles.append(file)
        self.fileTestDetails[testName] = zip(ismipFiles, ismipDetails)

        # Record the data from the parser
        numberOutputFiles, numberConfigMatches, numberConfigTests = ismipParser.getParserSummary()

        # Create the plots & record the number generated
        numberPlots = self.plot(aOrC,resolution[:2])

        # Run bit for bit test
        numberBitTests, numberBitMatches = 0, 0
        self.bitForBitDetails[testName] = self.bit4bit(os.sep + testName)
        for key, value in self.bitForBitDetails[testName].iteritems():
            print ("    {:<30} {:<10}".format(key,value[0]))
            if value[0] == "SUCCESS": numberBitMatches+=1
            numberBitTests+=1

        self.summary[testName] = [numberPlots, numberOutputFiles,
                                  numberConfigMatches, numberConfigTests,
                                  numberBitMatches, numberBitTests]

    ## Creates a plot based on the given input.
    #  
    #  input:
    #    @param aOrC : A string containing either "a" or "c" depending on the test case.
    #    @param size : The spatial resolution of the test in km.
    #
    def plot(self, aOrC, size):
        ncl_path = livv.cwd + os.sep + "plots" 
        img_path = livv.imgDir + os.sep + "ismip"
        plotFile = ''+ ncl_path + '/ismip-'+aOrC+'/ismip'+aOrC+size+'ug.ncl'
        benchDir = livv.benchmarkDir + '/ismip-hom-'+aOrC+'/'+size+'km/' + os.sep + livv.dataDir
        modelDir =  livv.inputDir + '/ismip-hom-'+aOrC+'/'+size+'km/' + os.sep + livv.dataDir

        description = "U Velocity Comparison Plot"
        bench1 = 'STOCK1 = addfile(\"'+ benchDir + os.sep + 'ishom.'+aOrC+'.'+size+'km.glissade.1.out.nc\", \"r\")'
        bench4 = 'STOCK4 = addfile(\"'+ benchDir + os.sep + 'ishom.'+aOrC+'.'+size+'km.glissade.4.out.nc\", \"r\")'
        test1 = 'VAR1 = addfile(\"'+ modelDir + os.sep + 'ishom.'+aOrC+'.'+size+'km.glissade.1.out.nc\", \"r\")'
        test4 = 'VAR4 = addfile(\"'+ modelDir + os.sep + 'ishom.'+aOrC+'.'+size+'km.glissade.1.out.nc\", \"r\")'
        name = 'ismip'+aOrC+size+'ug.png'
        path = 'PNG = "' + img_path + '/' + name + '"'
        plotCommand = "ncl '" + bench1 + "'  '" + bench4 + "'  '" + test1 + "'  '" + test4 \
                        +"'  '" + path + "' " + plotFile

        # Be cautious about running subprocesses
        call = subprocess.Popen(plotCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdOut, stdErr = call.stdout.read(), call.stderr.read()

        if os.path.exists(img_path + os.sep + name):
            print("    Plot details saved to " + img_path + " as " + name)
            self.plotDetails['ismip-hom-'+aOrC+'/'+size+'km'] = [[name, description]]
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


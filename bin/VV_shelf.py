'''
Master module for shelf test cases

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
from numpy.f2py import diagnose

# # Main class for handling shelf test cases.
#
#  The shelf test cases inherit functionality from AbstractTest for checking 
#  bit-for-bittedness as well as for parsing standard output from a model run.
#  This class handles the confined and circular variations of the shelf cases.
#
class Shelf(AbstractTest):

    ## Constructor
    #
    def __init__(self):
        super(self.__class__, self).__init__()

        self.name = "shelf"
        self.description = "A blank description"

    # # Return the name of the test
    #
    #  output:
    #    @returns name : shelf
    #
    def getName(self):
        return self.name


    # # Runs the shelf specific test case.  
    #
    #  When running a test this call will record the specific test case 
    #  being run.  Each specific test case string is mapped to the 
    #  method that will be used to run the actual test case.
    #
    #  input:
    #    @param testCase : the string indicator of the test to run
    #
    def run(self, test):
        # Common run 
        self.testsRun.append(test)

        # Map the case names to the case functions
        callDict = {'confined-shelf' : self.runConfined,
                    'circular-shelf' : self.runCircular}

        # Make sure LIVV can find the data
        shelfDir = livv.inputDir + os.sep + test + os.sep + livv.dataDir 
        shelfBenchDir = livv.benchmarkDir + os.sep + test + os.sep + livv.dataDir 
        if not (os.path.exists(shelfDir) and os.path.exists(shelfBenchDir)):
            print("    Could not find data for " + type + " tests!  Tried to find data in:")
            print("      " + shelfDir)
            print("      " + shelfBenchDir)
            print("    Continuing with next test....")
            self.bitForBitDetails[test] = {'Data not found': ['SKIPPED', '0.0']}
            return 1 # zero returns a problem

        # Call the correct function
        if callDict.has_key(test):
            callDict[test]()
        else:
            print("  Could not find test code for shelf test: " + test)


    # # Perform V&V on the confined shelf case
    # 
    def runConfined(self):
        print("  Confined Shelf test in progress....")

        confinedDir = livv.inputDir + '/confined-shelf' + os.sep + livv.dataDir
        confinedBenchDir = livv.benchmarkDir + '/confined-shelf' + os.sep + livv.dataDir

        # Parse the configure files
        configPath = os.sep + ".." + os.sep + "configure_files"
        shelfParser = Parser()
        self.modelConfigs['confined-shelf'], self.benchConfigs['confined-shelf'] = \
            shelfParser.parseConfigurations(confinedDir + configPath, confinedBenchDir + configPath)

        # Search for the std output files
        files = os.listdir(livv.inputDir + '/confined-shelf' + os.sep + livv.dataDir)
        test = re.compile("confined-shelf.*out.*")
        files = filter(test.search, files)

        # Scrape the details from each of the files and store some data for later
        shelfFiles, shelfDetails = [], []
        for file in files:
            shelfDetails.append(self.parse(livv.inputDir + '/confined-shelf' + os.sep + livv.dataDir + "/" + file))
            shelfFiles.append(file)
        self.fileTestDetails["confined-shelf"] = zip(shelfFiles, shelfDetails)

        # Create the plots
        self.plotConfined()

        # Run bit for bit test
        self.bitForBitDetails['confined-shelf'] = self.bit4bit('/confined-shelf')
        for key, value in self.bitForBitDetails['confined-shelf'].iteritems():
            print ("    {:<30} {:<10}".format(key, value[0]))


    # # Plot some details for the confined shelf case
    # 
    def plotConfined(self):
        # Setup where we are going to look for things
        ncl_path = livv.cwd + os.sep + "plots" 
        img_path = livv.imgDir + os.sep + "shelf"
        modelDir = livv.inputDir + os.sep + "confined-shelf" + os.sep + livv.dataDir
        benchDir = livv.benchmarkDir + os.sep + "confined-shelf" + os.sep + livv.dataDir
        glamFiles = ['confined-shelf.gnu.PIC.large.nc', 'confined-shelf.gnu.JFNK.large.nc']
        glissadeFiles = ['confined-shelf.gnu.glissade.nc']
        glamFlag, glissadeFlag = True, True

        # Check if all of the files for plotting Glam output is in place
        for each in glamFiles:
            if not (os.path.exists(modelDir + os.sep + each) and os.path.exists(benchDir + os.sep + each)):
                glamFlag = False

        # Check if all of the files for plotting Glissade output is in place
        for each in glissadeFiles:
            if not (os.path.exists(modelDir + os.sep + each) and os.path.exists(benchDir + os.sep + each)):
                glissadeFlag = False

        # Plot Glam
        if glamFlag:
            plotFile = ncl_path + '/shelf/confshelfvel.ncl'
            benchPIC = 'STOCKPIC = addfile(\"' + benchDir + os.sep + glamFiles[0] + '\", \"r\")'
            benchJFNK = 'STOCKJFNK = addfile(\"'+ benchDir + os.sep + glamFiles[1] + '\", \"r\")'
            modelPIC = 'VARPIC = addfile(\"' + modelDir + os.sep + glamFiles[0] + '\", \"r\")'
            modelJFNK = 'VARJFNK = addfile(\"' + modelDir + os.sep + glamFiles[1] + '\", \"r\")'
            name = 'confshelfvel.png' 
            path = 'PNG = "' + img_path + '/' + name + '"'
            plotCommand = "ncl '" + benchPIC + "'  '" + benchJFNK + "'  '" + modelPIC + "' '" + modelJFNK \
                    + "' '" + path + "' " + plotFile

            # Be cautious about running subprocesses
            call = subprocess.Popen(plotCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdOut, stdErr = call.stdout.read(), call.stderr.read()

            if os.path.exists(img_path + os.sep + name):
                print("    Plot details saved to " + img_path + " as " + name)
            else:
                print("****************************************************************************")
                print("*** Error saving " + name + " to " + img_path)
                print("*** Details of the error follow: ")
                print("")
                print(stdOut)
                print(stdErr)
                print("****************************************************************************")

        # Plot Glissade
        if glissadeFlag:
            plotFile = ncl_path + '/shelf/confshelfvelg.ncl'
            benchData = 'STOCKGLS = addfile(\"' + benchDir + os.sep + glissadeFiles[0] + '\", \"r\")'
            modelData = 'VARGLS = addfile(\"'  + modelDir + os.sep + glissadeFiles[0] + '\", \"r\")'
            name = 'confshelfvelg.png' 
            path = 'PNG = "' + img_path + '/' + name + '"'
            plotCommand = "ncl '" + benchData + "'  '" + modelData + "' '" + path + "' " + plotFile

            # Be cautious about running subprocesses
            call = subprocess.Popen(plotCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdOut, stdErr = call.stdout.read(), call.stderr.read()

            if os.path.exists(img_path + os.sep + name):
                print("    Plot details saved to " + img_path + " as " + name)
            else:
                print("****************************************************************************")
                print("*** Error saving " + name + " to " + img_path)
                print("*** Details of the error follow: ")
                print("")
                print(stdOut)
                print(stdErr)
                print("****************************************************************************")

        # Done with plotting for confined shelf
        return


    # # Perform V&V on the circular shelf case
    #
    def runCircular(self):
        print("  Circular Shelf test in progress....")  
        circularDir = livv.inputDir + '/circular-shelf' + os.sep + livv.dataDir
        circularBenchDir = livv.benchmarkDir + '/circular-shelf' + os.sep + livv.dataDir

        # Parse the configure files
        configPath = os.sep + ".." + os.sep + "configure_files"
        shelfParser = Parser()
        self.modelConfigs['circular-shelf'], self.benchConfigs['circular-shelf'] = \
            shelfParser.parseConfigurations(circularDir + configPath, circularBenchDir + configPath)

        # Search for the std output files
        files = os.listdir(livv.inputDir + '/circular-shelf' + os.sep + livv.dataDir)
        test = re.compile("circular-shelf.*out.*")
        files = filter(test.search, files)

        # Scrape the details from each of the files and store some data for later
        shelfDetails, shelfFiles = [], []
        for file in files:
            shelfDetails.append(self.parse(livv.inputDir + '/circular-shelf' + os.sep + livv.dataDir + "/" + file))
            shelfFiles.append(file)
        self.fileTestDetails["circular-shelf"] = zip(shelfFiles, shelfDetails)

        # Create the plots
        self.plotCircular()

        # Run bit for bit test
        self.bitForBitDetails['circular-shelf'] = self.bit4bit('/circular-shelf')
        for key, value in self.bitForBitDetails['circular-shelf'].iteritems():
            print ("    {:<30} {:<10}".format(key, value[0]))


    # # Plot some details from the confined shelf case
    # 
    def plotCircular(self):
        # Setup where we are going to look for things
        ncl_path = livv.cwd + os.sep + "plots" 
        img_path = livv.imgDir + os.sep + "shelf"
        modelDir = livv.inputDir + os.sep + "circular-shelf" + os.sep + livv.dataDir
        benchDir = livv.benchmarkDir + os.sep + "circular-shelf" + os.sep + livv.dataDir
        glamFiles = ['circular-shelf.gnu.PIC.large.nc', 'circular-shelf.gnu.JFNK.large.nc']
        glissadeFiles = ['circular-shelf.gnu.glissade.nc']
        glamFlag, glissadeFlag = True, True

        # Check if all of the files for plotting Glam output is in place
        for each in glamFiles:
            if not (os.path.exists(modelDir + os.sep + each) and os.path.exists(benchDir + os.sep + each)):
                glamFlag = False

        # Check if all of the files for plotting Glissade output is in place
        for each in glissadeFiles:
            if not (os.path.exists(modelDir + os.sep + each) and os.path.exists(benchDir + os.sep + each)):
                glissadeFlag = False

        # Plot Glam
        if glamFlag:
            plotFile = ncl_path + '/shelf/circshelfvel.ncl'
            benchPIC    = 'STOCKPIC = addfile(\"'+ benchDir +  '/circular-shelf.gnu.PIC.large.nc\", \"r\")'
            benchJFNK   = 'STOCKJFNK = addfile(\"'+ benchDir + '/circular-shelf.gnu.JFNK.large.nc\", \"r\")'
            modelPIC      = 'VARPIC = addfile(\"' + modelDir + '/circular-shelf.gnu.PIC.large.nc\", \"r\")'
            modelJFNK     = 'VARJFNK = addfile(\"' + modelDir + '/circular-shelf.gnu.JFNK.large.nc\", \"r\")'
            name  = 'circshelfvel.png' 
            png         = 'PNG = "' + img_path + '/' + name + '"'
            plotCommand = "ncl '" + benchPIC + "'  '" + benchJFNK + "'  '" + modelPIC + "' '" + modelJFNK \
                    + "' '" + png + "' " + plotFile

            # Be cautious about running subprocesses
            call = subprocess.Popen(plotCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdOut, stdErr = call.stdout.read(), call.stderr.read()

            if os.path.exists(img_path + os.sep + name):
                print("    Plot details saved to " + img_path + " as " + name)
            else:
                print("****************************************************************************")
                print("*** Error saving " + name + " to " + img_path)
                print("*** Details of the error follow: ")
                print("")
                print(stdOut)
                print(stdErr)
                print("****************************************************************************")

        if glissadeFlag:
            plotFile = ''+ ncl_path + '/shelf/circshelfvelg.ncl'
            benchGLS    = 'STOCKGLS = addfile(\"'+ benchDir + '/circular-shelf.gnu.glissade.nc\", \"r\")'
            modelGLS = 'VARGLS = addfile(\"' + modelDir + '/circular-shelf.gnu.glissade.nc\", \"r\")'
            name = 'circshelfvelg.png'
            png = 'PNG = "' + img_path + '/' + name + '"'
            plotCommand = "ncl '" + benchGLS + "'  '" + modelGLS \
                    + "' '" + png + "' " + plotFile

            # Be cautious about running subprocesses
            call = subprocess.Popen(plotCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdOut, stdErr = call.stdout.read(), call.stderr.read()

            if os.path.exists(img_path + os.sep + name):
                print("    Plot details saved to " + img_path + " as " + name)
            else:
                print("****************************************************************************")
                print("*** Error saving " + name + " to " + img_path)
                print("*** Details of the error follow: ")
                print("")
                print(stdOut)
                print(stdErr)
                print("****************************************************************************")

        # Done plotting circular-shelf
        return

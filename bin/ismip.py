'''
Master module for Ismip tests.  

Created on Dec 8, 2014

@author: arbennett
'''

import re
import os
import subprocess


cases = {'none'  : [],
         'small' : ['ismip-hom-a/80km', 'ismip-hom-c/80km'],
         'large' : ['ismip-hom-a/20km', 'ismip-hom-c/20km'],
         'all'   : ['ismip-hom-a/20km', 'ismip-hom-c/20km', 'ismip-hom-a/80km', 'ismip-hom-c/80km']}

def choices():
    return list( cases.keys() )

def choose(key):
    return cases[key]


import livv
from bin.test import AbstractTest
from bin.parser import Parser

## Main class for handling Ismip test cases.
#
#  The Ismip test cases inherit functionality from AbstractTest for checking 
#  bit-for-bittedness as well as for parsing standard output from a model run.
#  This class handles the Ismip-hom a and c tests for resolutions of 20km and 80km.
#
class Test(AbstractTest):

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
        test = re.compile(".*out.*[0-9]")
        try:
            files = os.listdir(ismipDir)
        except:
            print("    Could not find model and benchmark directories for ismip-hom-" + aOrC + os.sep + resolution)
            files = []
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
            print ("    {:<40} {:<10}".format(key,value[0]))
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
        benchDir = livv.benchmarkDir + '/ismip-hom-'+aOrC+'/'+size+'km/' + os.sep + livv.dataDir
        modelDir =  livv.inputDir + '/ismip-hom-'+aOrC+'/'+size+'km/' + os.sep + livv.dataDir
        glamFiles = ["ishom."+aOrC+"."+size+"km.PIC.out.nc", "ishom."+aOrC+"."+size+"km.JFNK.out.nc"]
        #filter(re.compile("ishom." + aOrC + '.' + size + "km.((JFNK)|(PIC)).out.nc").search, os.listdir(modelDir))
        glissadeFiles = ["ishom."+aOrC+"."+size+"km.glissade.1.out.nc", "ishom."+aOrC+"."+size+"km.glissade.4.out.nc"]
        #filter(re.compile("ishom." + aOrC + '.' + size + "km.glissade.\d.out.nc").search, os.listdir(modelDir))
        glamFlag, glissadeFlag = True, True
        imgArr = []

        # Check if all of the files for plotting Glam output is in place
        if len(glamFiles) != 0:
            for each in glamFiles:
                if not (os.path.exists(modelDir + os.sep + each) and os.path.exists(benchDir + os.sep + each)):
                    glamFlag = False
        else:
            glamFlag = False

        # Check if all of the files for plotting Glissade output is in place
        if len(glissadeFiles) != 0:
            for each in glissadeFiles:
                if not (os.path.exists(modelDir + os.sep + each) and os.path.exists(benchDir + os.sep + each)):
                    glissadeFlag = False
        else: 
            glissadeFlag = False

        if glamFlag:
            description = "Glam U Velocity Comparison Plot"
            plotFile = ''+ ncl_path + '/ismip-'+aOrC+'/ismip'+aOrC+size+'u.ncl'
            bench1 = 'STOCKPIC = addfile(\"'+ benchDir + os.sep + glamFiles[0]+'\", \"r\")'
            bench4 = 'STOCKJFNK = addfile(\"'+ benchDir + os.sep + glamFiles[1]+'\", \"r\")'
            test1 = 'VARPIC = addfile(\"'+ modelDir + os.sep + glamFiles[0]+'\", \"r\")'
            test4 = 'VARJFNK = addfile(\"'+ modelDir + os.sep + glamFiles[1]+'\", \"r\")'
            name = 'ismip'+aOrC+size+'u.png'
            path = 'PNG = "' + img_path + '/' + name + '"'
            plotCommand = "ncl '" + bench1 + "'  '" + bench4 + "'  '" + test1 + "'  '" + test4 \
                            +"'  '" + path + "' " + plotFile

            # Be cautious about running subprocesses
            call = subprocess.Popen(plotCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdOut, stdErr = call.stdout.read(), call.stderr.read()

            if os.path.exists(img_path + os.sep + name):
                print("    Plot details saved to " + img_path + " as " + name)
                imgArr.append([name, description])
            else:
                print("****************************************************************************")
                print("    Error saving " + name + " to " + img_path)
                print("    Details of the error follow: ")
                print("")
                print(stdOut)
                print(stdErr)
                print("****************************************************************************")
                return 0

            description = "Glam V Velocity Comparison Plot"
            plotFile = ''+ ncl_path + '/ismip-'+aOrC+'/ismip'+aOrC+size+'v.ncl'
            bench1 = 'STOCKPIC = addfile(\"'+ benchDir + os.sep + glamFiles[0]+'\", \"r\")'
            bench4 = 'STOCKJFNK = addfile(\"'+ benchDir + os.sep + glamFiles[1]+'\", \"r\")'
            test1 = 'VARPIC = addfile(\"'+ modelDir + os.sep + glamFiles[0]+'\", \"r\")'
            test4 = 'VARJFNK = addfile(\"'+ modelDir + os.sep + glamFiles[1]+'\", \"r\")'
            name = 'ismip'+aOrC+size+'v.png'
            path = 'PNG = "' + img_path + '/' + name + '"'
            plotCommand = "ncl '" + bench1 + "'  '" + bench4 + "'  '" + test1 + "'  '" + test4 \
                            +"'  '" + path + "' " + plotFile

            # Be cautious about running subprocesses
            call = subprocess.Popen(plotCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdOut, stdErr = call.stdout.read(), call.stderr.read()

            if os.path.exists(img_path + os.sep + name):
                print("    Plot details saved to " + img_path + " as " + name)
                imgArr.append([name, description])
            else:
                print("****************************************************************************")
                print("    Error saving " + name + " to " + img_path)
                print("    Details of the error follow: ")
                print("")
                print(stdOut)
                print(stdErr)
                print("****************************************************************************")
                return 0

        if glissadeFlag:
            description = "Glissade U Velocity Comparison Plot"
            plotFile = ''+ ncl_path + '/ismip-'+aOrC+'/ismip'+aOrC+size+'ug.ncl'
            bench1 = 'STOCK1 = addfile(\"'+ benchDir + os.sep + glissadeFiles[0]+'\", \"r\")'
            bench4 = 'STOCK4 = addfile(\"'+ benchDir + os.sep + glissadeFiles[1]+'\", \"r\")'
            test1 = 'VAR1 = addfile(\"'+ modelDir + os.sep + glissadeFiles[0]+'\", \"r\")'
            test4 = 'VAR4 = addfile(\"'+ modelDir + os.sep + glissadeFiles[1]+'\", \"r\")'
            name = 'ismip'+aOrC+size+'ug.png'
            path = 'PNG = "' + img_path + '/' + name + '"'
            plotCommand = "ncl '" + bench1 + "'  '" + bench4 + "'  '" + test1 + "'  '" + test4 \
                            +"'  '" + path + "' " + plotFile

            # Be cautious about running subprocesses
            call = subprocess.Popen(plotCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdOut, stdErr = call.stdout.read(), call.stderr.read()

            if os.path.exists(img_path + os.sep + name):
                print("    Plot details saved to " + img_path + " as " + name)
                imgArr.append([name, description])
            else:
                print("****************************************************************************")
                print("    Error saving " + name + " to " + img_path)
                print("    Details of the error follow: ")
                print("")
                print(stdOut)
                print(stdErr)
                print("****************************************************************************")
                return 0

            description = "Glissade V Velocity Comparison Plot"
            plotFile = ''+ ncl_path + '/ismip-'+aOrC+'/ismip'+aOrC+size+'vg.ncl'
            bench1 = 'STOCK1 = addfile(\"'+ benchDir + os.sep + glissadeFiles[0]+'\", \"r\")'
            bench4 = 'STOCK4 = addfile(\"'+ benchDir + os.sep + glissadeFiles[1]+'\", \"r\")'
            test1 = 'VAR1 = addfile(\"'+ modelDir + os.sep + glissadeFiles[0]+'\", \"r\")'
            test4 = 'VAR4 = addfile(\"'+ modelDir + os.sep + glissadeFiles[1]+'\", \"r\")'
            name = 'ismip'+aOrC+size+'vg.png'
            path = 'PNG = "' + img_path + '/' + name + '"'
            plotCommand = "ncl '" + bench1 + "'  '" + bench4 + "'  '" + test1 + "'  '" + test4 \
                            +"'  '" + path + "' " + plotFile

            # Be cautious about running subprocesses
            call = subprocess.Popen(plotCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdOut, stdErr = call.stdout.read(), call.stderr.read()

            if os.path.exists(img_path + os.sep + name):
                print("    Plot details saved to " + img_path + " as " + name)
                imgArr.append([name, description])
            else:
                print("****************************************************************************")
                print("    Error saving " + name + " to " + img_path)
                print("    Details of the error follow: ")
                print("")
                print(stdOut)
                print(stdErr)
                print("****************************************************************************")
                return 0

        if len(imgArr) != 0:
            self.plotDetails['ismip-hom-'+aOrC+'/'+size+'km'] = imgArr
        # Done with plotting for ismip case
        return len(imgArr)

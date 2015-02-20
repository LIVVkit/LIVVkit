'''
Master module for Ismip tests.  

Created on Dec 8, 2014

@author: arbennett
'''

import re
import os
import sys
import glob
import subprocess

import livv
from livv import *
from bin.VV_test import *
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
        self.ismipTestsRun = []
        self.ismipBitForBitDetails = dict()
        self.ismipFileTestDetails = dict()
        
        self.name = "ismip"
        self.description = "Ice Sheet Model Intercomparison Project for Higher-Order Models (ISMIP-HOM)" + \
                           "prescribes a set of experiments meant to test the implementation of higher-order" + \
                           " physics.  For more information, see http://homepages.ulb.ac.be/~fpattyn/ismip/ \n" + \
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
        self.ismipTestsRun.append(testCase)
        
        # Make sure LIVV can find the data
        ismipDir = livv.inputDir + os.sep + testCase + os.sep + livv.dataDir 
        ismipBenchDir = livv.benchmarkDir + os.sep + testCase + os.sep + livv.dataDir
        if not (os.path.exists(ismipDir) and os.path.exists(ismipBenchDir)):
            print("    Could not find data for " + ismipDir + " tests!  Tried to find data in:")
            print("      " + ismipDir)
            print("      " + ismipBenchDir)
            print("    Continuing with next test....")
            self.ismipBitForBitDetails[testCase] = {'Data not found': ['SKIPPED', '0.0']}
            return 1 # zero returns a problem        
        
        # Pull some data about the test case
        splitCase = testCase.split('/')
        aOrC = splitCase[0][-1]
        resolution = splitCase[-1]
        
        # Pass it onto the specific run
        self.runIsmip(aOrC,resolution)
            
    
    ## Creates the output test page
    #
    #  The generate method will create an ismip.html page in the output directory.
    #  This page will contain a detailed list of the results from LIVV.  
    #
    def generate(self):
        # Set up jinja related variables
        templateLoader = jinja2.FileSystemLoader( searchpath=livv.templateDir )
        templateEnv = jinja2.Environment( loader=templateLoader )
        templateFile = "/test.html"
        template = templateEnv.get_template( templateFile )
        
        # Set up relative paths
        indexDir = ".."
        cssDir = indexDir + "/css"
        imgDir = indexDir + "/imgs/ismip"
        
        # Grab all of our images
        testImgDir = livv.imgDir + os.sep + "ismip"
        testImages = [os.path.basename(img) for img in glob.glob(testImgDir + os.sep + "*.png")]
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + "/*.jpg")] )
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + "/*.svg")] )

        # Set up the template variables  
        templateVars = {"timestamp" : livv.timestamp,
                        "user" : livv.user,
                        "comment" : livv.comment,
                        "testName" : self.getName(),
                        "indexDir" : livv.indexDir,
                        "cssDir" : livv.cssDir,
                        "testDescription" : self.description,
                        "testsRun" : self.ismipTestsRun,
                        "testHeader" : livv.parserVars,
                        "bitForBitDetails" : self.ismipBitForBitDetails,
                        "testDetails" : self.ismipFileTestDetails,
                        "imgDir" : imgDir,
                        "testImages" : testImages}
        outputText = template.render( templateVars )
        page = open(testDir + '/ismip.html', "w")
        page.write(outputText)
        page.close()        
    
    
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
                
        # Search for the std output files
        files = os.listdir(livv.inputDir + '/ismip-hom-' + aOrC + os.sep + resolution + os.sep + livv.dataDir)
        test = re.compile(".*out.*[0-9]")
        files = filter(test.search, files)
        
        # Scrape the details from each of the files and store some data for later
        ismipDetails, ismipFiles = [], []
        for file in files:
            ismipDetails.append(self.parse(livv.inputDir + '/ismip-hom-' + aOrC + os.sep + resolution + os.sep + livv.dataDir + '/' + file))
            ismipFiles.append(file)
        self.ismipFileTestDetails['ismip-hom-' + aOrC + os.sep + resolution] = zip(ismipFiles, ismipDetails)
        
        # Create the plots
        self.plot(aOrC,resolution[:2])

        # Run bit for bit test
        self.ismipBitForBitDetails['ismip-hom-' + aOrC + os.sep + resolution] = self.bit4bit('/ismip-hom-' + aOrC + os.sep + resolution)
        for key, value in self.ismipBitForBitDetails['ismip-hom-' + aOrC + os.sep + resolution].iteritems():
            print ("    {:<30} {:<10}".format(key,value[0]))
            

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
        else:
            print("****************************************************************************")
            print("    Error saving " + name + " to " + img_path)
            print("    Details of the error follow: ")
            print("")
            print(stdOut)
            print(stdErr)
            print("****************************************************************************")
        
        
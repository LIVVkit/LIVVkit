'''
Master module for dome test cases

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
from livv_bin.VV_test import *
import jinja2
from numpy.f2py import diagnose

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
        # Mapping of result codes to results
        result = {-1 : 'N/A', 0 : 'SUCCESS', 1 : 'FAILURE'}
        
        # Keep track of what dome test have been run
        self.domeTestsRun = []
        self.domeBitForBitDetails = dict()
        self.domeTestFiles = []
        self.domeTestDetails = []
        self.domeFileTestDetails = []
        
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
        self.domeTestsRun.append(testCase)
        
        # Map the case names to the case functions
        splitCase = testCase.split('/')
        type = splitCase[-1]
        resolution = splitCase[0][4:]
        callDict = {'diagnostic' : self.runDiagnostic,
                    'evolving' : self.runEvolving}
        
        # Make sure LIVV can find the data
        domeDir = livv.inputDir + os.sep + "dome" + resolution + os.sep + type + os.sep + livv.dataDir 
        domeBenchDir = livv.benchmarkDir + os.sep + "dome" + resolution + os.sep + type + os.sep + livv.dataDir 
        if not (os.path.exists(domeDir) or os.path.exists(domeBenchDir)):
            print("    Could not find data for dome" + resolution + " " + type + " tests!  Tried to find data in:")
            print("      " + domeDir)
            print("      " + domeBenchDir)
            print("    Continuing with next test....")
            self.domeBitForBitDetails['dome' + resolution + os.sep + type] = {'Data not found': ['SKIPPED', '0.0']}
            return 1 # zero returns a problem        
        
        # Call the correct function
        if callDict.has_key(type):
            callDict[type](resolution)
        else: 
            print("  Could not find test code for dome test: " + testCase)
         
        # More common postprocessing
        return
        
    
    ## Creates the output test page
    #
    #  The generate method will create a dome.html page in the output directory.
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
        templateLoader = jinja2.FileSystemLoader( searchpath=livv.templateDir )
        templateEnv = jinja2.Environment( loader=templateLoader )
        templateFile = "/test.html"
        template = templateEnv.get_template( templateFile )
        
        indexDir = ".."
        cssDir = indexDir + "/css"
        imgDir = indexDir + "/imgs/dome"
        
        testImgDir = livv.imgDir + os.sep + "dome"
        testImages = [os.path.basename(img) for img in glob.glob(testImgDir + os.sep + "*.png")]
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + os.sep + "*.jpg")] )
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + os.sep + "*.svg")] )

        self.domeFileTestDetails = zip(self.domeTestFiles,self.domeTestDetails)

        # Set up the template variables  
        templateVars = {"timestamp" : livv.timestamp,
                        "user" : livv.user,
                        "comment" : livv.comment,
                        "testName" : self.getName(),
                        "indexDir" : indexDir,
                        "cssDir" : cssDir,
                        "testDescription" : self.description,
                        "testsRun" : self.domeTestsRun,
                        "bitForBitDetails" : self.domeBitForBitDetails,
                        "testHeader" : livv.parserVars,
                        "testDetails" : self.domeFileTestDetails,
                        "imgDir" : imgDir,
                        "testImages" : testImages}
        outputText = template.render( templateVars )
        page = open(testDir + os.sep + 'dome.html', "w")
        page.write(outputText)
        page.close()        
    
    
    ## Perform V&V on the diagnostic dome case
    #
    #  Runs the dome diagnostic V&V for a given resolution.  First parses through all 
    #  of the standard output files for the given test case, then generates plots via
    #  the plotDiagnostic function.  Finishes up by doing bit for bit comparisons with
    #  the benchmark files.
    #
    #  input:
    #    @param resoultion: The resolution of the test cases to look in. 
    #                       (eg resolution == 30 -> reg_test/dome30/diagnostic)
    # 
    def runDiagnostic(self, resolution):        
        print("  Dome Diagnostic test in progress....")  

        # Search for the standard output files
        diagnosticDir = livv.inputDir + os.sep + "dome" + resolution + os.sep + "diagnostic" + os.sep + livv.dataDir 
        files = os.listdir(diagnosticDir)
        test = re.compile(".*[0-9]proc")
        files = filter(test.search, files)
        
        # Scrape the details from each of the files and store some data for later
        for file in files:
            self.domeTestDetails.append(self.parse(diagnosticDir + os.sep +  file))
            self.domeTestFiles.append(file)
        
        # Create the plots
        self.plotDiagnostic(resolution)

        # Run bit for bit tests
        self.domeBitForBitDetails['dome' + resolution + os.sep + 'diagnostic'] = self.bit4bit(os.sep + 'dome' + resolution + os.sep + 'diagnostic')
        for key, value in self.domeBitForBitDetails['dome' + resolution + os.sep + 'diagnostic'].iteritems():
            print ("    {:<30} {:<10}".format(key,value[0]))

        return 0 # zero returns success
    
    
    ## Plot some details from the diagnostic dome case
    # 
    #  Plots a comparison of the norm of the velocity for several cases of the evolving
    #  dome test case.
    #
    #  input:
    #    @param resoultion: The resolution of the test cases to look in. 
    #                       (eg resolution == 30 -> reg_test/dome30/diagnostic) 
    #
    def plotDiagnostic(self, resolution):
        # Set up where we are going to look for things
        ncl_path = livv.cwd + os.sep + "plots" 
        img_path = livv.imgDir + os.sep + "dome"
        domedvel_plotfile = ''+ ncl_path + os.sep + 'dome30' + os.sep + 'dome30dvel.ncl'
        
        # The arguments to pass in to the ncl script
        bench1 = 'STOCK1 = addfile(\"'+ livv.benchmarkDir + os.sep + 'dome' + resolution + os.sep + 'diagnostic' + livv.dataDir + os.sep + 'dome.1.nc\", \"r\")'
        bench4 = 'STOCK4 = addfile(\"'+ livv.benchmarkDir + os.sep + 'dome' + resolution + os.sep + 'diagnostic' + livv.dataDir + os.sep + 'dome.4.nc\", \"r\")'
        test1  = 'VAR1 = addfile(\"' + livv.inputDir + os.sep + 'dome' + resolution + os.sep + 'diagnostic' + livv.dataDir + os.sep + 'dome.1.nc\", \"r\")'
        test4  = 'VAR4 = addfile(\"' + livv.inputDir + os.sep + 'dome' + resolution + os.sep + 'diagnostic' + livv.dataDir + os.sep + 'dome.4.nc\", \"r\")'
        name = 'dome30dvel.png'
        path = 'PNG = "' + img_path + os.sep + name + '"'
        
        # The plot command to run
        plot_dome30dvel = "ncl '" + bench1 + "' '" + bench4 + "'  '" + test1 + "' '" + test4 + \
                    "' '" + path + "' " + domedvel_plotfile + " >> plot_details.out"
        
        # Give the user some feedback
        print("    Saving plot details to " + img_path + " as " + name)
            
        # Be cautious about running subprocesses
        try:
            subprocess.check_call(plot_dome30dvel, shell=True)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)
        
        return
    
    ## Perform V&V on the evolving dome case
    #
    #  Runs the dome evolving V&V for a given resolution.  First parses through all 
    #  of the standard output files for the given test case, then generates plots via
    #  the plotEvolving function.  Finishes up by doing bit for bit comparisons with
    #  the benchmark files.
    #
    #  input:
    #    @param resoultion: The resolution of the test cases to look in. 
    #                       (eg resolution == 30 -> reg_test/dome30/evolving)
    # 
    def runEvolving(self, resolution):
        print("  Dome Evolving test in progress....")  \
                        
        # Search for the std output files
        evolvingDir = livv.inputDir + os.sep + "dome" + resolution + os.sep + "evolving" + os.sep + livv.dataDir 
        files = os.listdir(evolvingDir)
        test = re.compile(".*[0-9]proc")
        files = filter(test.search, files)
        
        # Scrape the details from each of the files and store some data for later
        for file in files:
            self.domeTestDetails.append(self.parse(evolvingDir + os.sep + file))
            self.domeTestFiles.append(file)
        
        # Create the plots
        self.plotEvolving(resolution)

        # Run bit for bit test
        self.domeBitForBitDetails['dome' + resolution + os.sep +'evolving'] = self.bit4bit(os.sep + 'dome' + resolution + os.sep + 'evolving')
        for key, value in self.domeBitForBitDetails['dome' + resolution + os.sep + 'evolving'].iteritems():
            print ("    {:<30} {:<10}".format(key,value[0]))

        return 0 # zero returns success
    
    
    ## Plot some details from the evolving dome case
    # 
    #  Plots a comparison of the norm of the velocity for several cases of the evolving
    #  dome test case.
    #
    #  input:
    #    @param resoultion: The resolution of the test cases to look in. 
    #                       (eg resolution == 30 -> reg_test/dome30/evolving)
    #
    def plotEvolving(self, resolution):
        # Set up where we are going to look for things
        ncl_path = livv.cwd + os.sep + "plots" 
        img_path = livv.imgDir + os.sep + "dome"
        domeevel_plotfile = ''+ ncl_path + os.sep + 'dome30' + os.sep + 'dome30evel.ncl'
        
        # The arguments to pass in to the ncl script
        bench1 = 'STOCK9 = addfile(\"'+ livv.benchmarkDir + os.sep + 'dome' + resolution + os.sep + 'evolving' + livv.dataDir + os.sep + 'dome.small.nc\", \"r\")'
        bench4 = 'STOCK15 = addfile(\"'+ livv.benchmarkDir + os.sep + 'dome' + resolution + os.sep + 'evolving' + livv.dataDir + os.sep + 'dome.large.nc\", \"r\")'
        test1  = 'VAR9 = addfile(\"' + livv.inputDir + os.sep + 'dome' + resolution + os.sep + 'evolving' + livv.dataDir + os.sep + 'dome.small.nc\", \"r\")'
        test4  = 'VAR15 = addfile(\"' + livv.inputDir + os.sep + 'dome' + resolution + os.sep + 'evolving' + livv.dataDir + os.sep + 'dome.large.nc\", \"r\")'
        name = 'dome' + resolution + 'evel.png'
        path = 'PNG = "' + img_path + os.sep + name + '"'
        
        # The plot command to run
        plot_dome30evel = "ncl '" + bench1 + "' '" + bench4 + "'  '" + test1 + "' '" + test4 + \
                    "' '" + path + "' " + domeevel_plotfile + " >> plot_details.out"
        
        # Give the user some feedback
        print("    Saving plot details to " + img_path + " as " + name)
        
        # Be cautious about running subprocesses
        try:
            subprocess.check_call(plot_dome30evel, shell=True)
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)
        
        return
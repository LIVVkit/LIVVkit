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
    #  This page will contain a detailed list of the results from LIVV.  
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
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + "/*.jpg")] )
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + "/*.svg")] )

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
        page = open(testDir + '/dome.html', "w")
        page.write(outputText)
        page.close()        
    
    ## Perform V&V on the diagnostic dome case
    # 
    def runDiagnostic(self, resolution):
        print("  Dome Diagnostic test in progress....")  
        
        # Search for the std output files
        files = os.listdir(livv.inputDir + '/dome' + resolution + '/diagnostic' + livv.dataDir)
        test = re.compile(".*[0-9]proc")
        files = filter(test.search, files)
        
        # Scrape the details from each of the files and store some data for later
        for file in files:
            self.domeTestDetails.append(self.parse(livv.inputDir + '/dome' + resolution + '/diagnostic' + livv.dataDir + "/" +  file))
            self.domeTestFiles.append(file)
        
        # Create the plots
        self.plotDiagnostic(resolution)

        # Run bit for bit test
        self.domeBitForBitDetails['dome' + resolution + '/diagnostic'] = self.bit4bit('/dome' + resolution + '/diagnostic')
        for key, value in self.domeBitForBitDetails['dome' + resolution + '/diagnostic'].iteritems():
            print ("    {:<30} {:<10}".format(key,value[0]))

        return 0 # zero returns success
    
    
    ## Plot some details from the diagnostic dome case
    # 
    def plotDiagnostic(self, resolution):
        # Set up where we are going to look for things
        ncl_path = livv.cwd + os.sep + "plots" 
        img_path = livv.imgDir + os.sep + "dome"
        domedvel_plotfile = ''+ ncl_path + '/dome30/dome30dvel.ncl'
        
        # The arguments to pass in to the ncl script
        bench1 = 'STOCK1 = addfile(\"'+ livv.benchmarkDir + '/dome' + resolution + '/diagnostic' + livv.dataDir + '/dome.1.nc\", \"r\")'
        bench4 = 'STOCK4 = addfile(\"'+ livv.benchmarkDir + '/dome' + resolution + '/diagnostic' + livv.dataDir + '/dome.4.nc\", \"r\")'
        test1  = 'VAR1 = addfile(\"' + livv.inputDir + '/dome' + resolution + '/diagnostic' + livv.dataDir + '/dome.1.nc\", \"r\")'
        test4  = 'VAR4 = addfile(\"' + livv.inputDir + '/dome' + resolution + '/diagnostic' + livv.dataDir + '/dome.4.nc\", \"r\")'
        name = 'dome30dvel.png'
        path = 'PNG = "' + img_path + '/' + name + '"'
        
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
    def runEvolving(self, resolution):
        print("  Dome Evolving test in progress....")  
        
        # Search for the std output files
        files = os.listdir(livv.inputDir + '/dome' + resolution + '/evolving' + livv.dataDir)
        test = re.compile(".*[0-9]proc")
        files = filter(test.search, files)
        
        # Scrape the details from each of the files and store some data for later
        for file in files:
            self.domeTestDetails.append(self.parse(livv.inputDir + '/dome' + resolution + '/evolving/' + livv.dataDir + '/' + file))
            self.domeTestFiles.append(file)
        
        # Create the plots
        self.plotEvolving(resolution)

        # Run bit for bit test
        self.domeBitForBitDetails['dome' + resolution + '/evolving'] = self.bit4bit('/dome' + resolution + '/evolving')
        for key, value in self.domeBitForBitDetails['dome' + resolution + '/evolving'].iteritems():
            print ("    {:<30} {:<10}".format(key,value[0]))

        return 0 # zero returns success
    
    
    ## Plot some details from the evolving dome case
    # 
    def plotEvolving(self, resolution):
        # Set up where we are going to look for things
        ncl_path = livv.cwd + os.sep + "plots" 
        img_path = livv.imgDir + os.sep + "dome"
        domeevel_plotfile = ''+ ncl_path + '/dome30/dome30evel.ncl'
        
        # The arguments to pass in to the ncl script
        bench1 = 'STOCK9 = addfile(\"'+ livv.benchmarkDir + '/dome' + resolution + '/evolving' + livv.dataDir + '/dome.small.nc\", \"r\")'
        bench4 = 'STOCK15 = addfile(\"'+ livv.benchmarkDir + '/dome' + resolution + '/evolving' + livv.dataDir + '/dome.large.nc\", \"r\")'
        test1  = 'VAR9 = addfile(\"' + livv.inputDir + '/dome' + resolution + '/evolving' + livv.dataDir + '/dome.small.nc\", \"r\")'
        test4  = 'VAR15 = addfile(\"' + livv.inputDir + '/dome' + resolution + '/evolving' + livv.dataDir + '/dome.large.nc\", \"r\")'
        name = 'dome' + resolution + 'evel.png'
        path = 'PNG = "' + img_path + '/' + name + '"'
        
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
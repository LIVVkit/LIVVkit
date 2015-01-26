'''
Master script for dome test cases

Created on Dec 8, 2014

@author: bzq
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

class Dome(AbstractTest):

    #
    # Constructor
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
        self.name = "Dome"
        self.description = "3-D paraboloid dome of ice with a circular, 60 km" + \
                      " diameter base sitting on a flat bed. The horizontal" + \
                      " spatial resolution studies are 2 km, 1 km, 0.5 km" + \
                      " and 0.25 km, and there are 10 vertical levels. For this" + \
                      " set of experiments a quasi no-slip basal condition in" + \
                      " imposed by setting. A zero-flux boundary condition is" + \
                      " applied to the dome margins. "
    
    #
    # Returns the name of the test
    #
    def getName(self):
        return self.name
    
    #
    # Runs the dome specific test case.  Calls some shared resources and
    # some diagnostic/evolving case specific methods.
    #
    # Input:
    #   testCase: the name of the dome test to run
    #
    def run(self, test):
        # Common run     
        self.domeTestsRun.append(test)
        
        # Map the case names to the case functions
        callDict = {'dome30/diagnostic' : self.runDiagnostic,
                    'dome30/evolving' : self.runEvolving}
        
        # Call the correct function
        if callDict.has_key(test):
            callDict[test]()
        else: 
            print("  Could not find test code for dome test: " + test)
         
        # More common postprocessing
        return
        
    
    #
    #  Description
    #
    #
    def generate(self):
        templateLoader = jinja2.FileSystemLoader( searchpath=livv.templateDir )
        templateEnv = jinja2.Environment( loader=templateLoader )
        templateFile = "/test.html"
        template = templateEnv.get_template( templateFile )
        
        testImgDir = imgDir + os.sep + "dome"
        testImages = glob.glob(testImgDir + os.sep + "*.png")
        testImages.append( glob.glob(testImgDir + "/*.jpg") )
        testImages.append( glob.glob(testImgDir + "/*.svg") )

        self.domeFileTestDetails = zip(self.domeTestFiles,self.domeTestDetails)

        # Set up the template variables  
        templateVars = {"timestamp" : livv.timestamp,
                        "user" : livv.user,
                        "testName" : "Dome",
                        "indexDir" : livv.indexDir,
                        "cssDir" : "css",
                        "testDescription" : self.description,
                        "testsRun" : self.domeTestsRun,
                        "bitForBitDetails" : self.domeBitForBitDetails,
                        "testDetails" : self.domeFileTestDetails,
                        "imgDir" : testImgDir,
                        "testImages" : testImages}
        outputText = template.render( templateVars )
        page = open(testDir + '/dome.html', "w")
        page.write(outputText)
        page.close()        
    
    #
    # Runs the diagnostic dome specific test case code.  
    #
    #
    #    
    def runDiagnostic(self):
        print("  Dome Diagnostic test in progress....")  
        
        # Search for the std output files
        files = os.listdir(livv.inputDir + '/dome30/diagnostic' + livv.dataDir)
        test = re.compile(".*[0-9]proc")
        files = filter(test.search, files)
        
        # Scrape the details from each of the files and store some data for later
        for file in files:
            self.domeTestDetails.append(self.parse(livv.inputDir + '/dome30/diagnostic' + livv.dataDir + "/" +  file))
            self.domeTestFiles.append(file)
        
        # Create the plots
        self.plotDiagnostic()

        # Run bit for bit test
        self.domeBitForBitDetails['dome30/diagnostic'] = self.bit4bit('/dome30/diagnostic')
        for key, value in self.domeBitForBitDetails['dome30/diagnostic'].iteritems():
            print ("    {:<30} {:<10}".format(key,value))

        return 0 # zero returns success
    
    
    #
    # Generates plots for the diagnostic dome test case.  
    #
    #
    #  
    def plotDiagnostic(self):
        # Set up where we are going to look for things
        ncl_path = livv.cwd + os.sep + "plots" 
        img_path = livv.imgDir + os.sep + "dome"
        dome30dvel_plotfile = ''+ ncl_path + '/dome30/dome30dvel.ncl'
        
        # The arguments to pass in to the ncl script
        bench1 = 'STOCK1 = addfile(\"'+ livv.benchmarkDir + '/dome30/diagnostic' + livv.dataDir + '/dome.1.nc\", \"r\")'
        bench4 = 'STOCK4 = addfile(\"'+ livv.benchmarkDir + '/dome30/diagnostic' + livv.dataDir + '/dome.4.nc\", \"r\")'
        test1  = 'VAR1 = addfile(\"' + livv.inputDir + '/dome30/diagnostic' + livv.dataDir + '/dome.1.nc\", \"r\")'
        test4  = 'VAR4 = addfile(\"' + livv.inputDir + '/dome30/diagnostic' + livv.dataDir + '/dome.4.nc\", \"r\")'
        name = 'dome30dvel.png'
        path = 'PNG = "' + img_path + '/' + name + '"'
        
        # The plot command to run
        plot_dome30dvel = "ncl '" + bench1 + "' '" + bench4 + "'  '" + test1 + "' '" + test4 + \
                    "' '" + path + "' " + dome30dvel_plotfile + " >> plot_details.out"
        
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
    
    #
    # Runs the evolving dome specific test case code.
    #
    #
    #
    def runEvolving(self):
        print("  Dome Evolving test in progress....")  
        
        # Search for the std output files
        files = os.listdir(livv.inputDir + '/dome30/evolving' + livv.dataDir)
        test = re.compile(".*[0-9]proc")
        files = filter(test.search, files)
        
        # Scrape the details from each of the files and store some data for later
        for file in files:
            self.domeTestDetails.append(self.parse(livv.inputDir + '/dome30/evolving/' + livv.dataDir + '/' + file))
            self.domeTestFiles.append(file)
        
        # Create the plots
        self.plotEvolving()

        # Run bit for bit test
        self.domeBitForBitDetails['dome30/evolving'] = self.bit4bit('/dome30/evolving')
        for key, value in self.domeBitForBitDetails['dome30/evolving'].iteritems():
            print ("    {:<30} {:<10}".format(key,value))

        return 0 # zero returns success
    
    
    #
    # Generates plots for the evolving dome test case.  
    #
    #
    #  
    def plotEvolving(self):
        # Set up where we are going to look for things
        ncl_path = livv.cwd + os.sep + "plots" 
        img_path = livv.imgDir + os.sep + "dome"
        dome30evel_plotfile = ''+ ncl_path + '/dome30/dome30evel.ncl'
        
        # The arguments to pass in to the ncl script
        bench1 = 'STOCK9 = addfile(\"'+ livv.benchmarkDir + '/dome30/evolving' + livv.dataDir + '/dome.small.nc\", \"r\")'
        bench4 = 'STOCK15 = addfile(\"'+ livv.benchmarkDir + '/dome30/evolving' + livv.dataDir + '/dome.large.nc\", \"r\")'
        test1  = 'VAR9 = addfile(\"' + livv.inputDir + '/dome30/evolving' + livv.dataDir + '/dome.small.nc\", \"r\")'
        test4  = 'VAR15 = addfile(\"' + livv.inputDir + '/dome30/evolving' + livv.dataDir + '/dome.large.nc\", \"r\")'
        name = 'dome30evel.png'
        path = 'PNG = "' + img_path + '/' + name + '"'
        
        # The plot command to run
        plot_dome30evel = "ncl '" + bench1 + "' '" + bench4 + "'  '" + test1 + "' '" + test4 + \
                    "' '" + path + "' " + dome30evel_plotfile + " >> plot_details.out"
        
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
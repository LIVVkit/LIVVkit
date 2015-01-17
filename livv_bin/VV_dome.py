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

    # Keep track of what dome test have been run
    domeTestsRun = []
    domeTestDetails = []
    
    # Describe what the dome tests are all about
    name = "Dome"
    description = "3-D paraboloid dome of ice with a circular, 60 km" + \
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
        #self.domeTestsRun.append(test)
        
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

        # Set up the template variables  
        templateVars = {"timestamp" : livv.timestamp,
                        "user" : livv.user,
                        "testName" : "Dome",
                        "indexDir" : livv.indexDir,
                        "cssDir" : livv.cssDir,
                        "testDescription" : self.description,
                        "testDetails" : zip(self.domeTestsRun, self.domeTestDetails),
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
        
        # Check for a test failure
        # Grep the std out of both the test and bench for things like:
        #    procs used
        #    nonlinear iterations
        #    linear iterations
        #    timesteps which failed to converge
        
        # Search for the std output files
        files = os.listdir(livv.inputDir + livv.dataDir + '/dome30/diagnostic')
        test = re.compile(".*[0-9]proc")
        files = filter(test.search, files)
        
        for file in files:
            self.domeTestsRun.append(file)
            self.domeTestDetails.append(self.parse(livv.inputDir + livv.dataDir + '/dome30/diagnostic/' + file))
        
        # Create the plots
        self.plotDiagnostic()
        
        # Run bit for bit test
        super(Dome, self).bit4bit('/dome30/diagnostic')
    
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
        bench1 = 'STOCK1 = addfile(\"'+ livv.benchmarkDir + '/dome30/diagnostic/dome.1.nc\", \"r\")'
        bench4 = 'STOCK4 = addfile(\"'+ livv.benchmarkDir + '/dome30/diagnostic//dome.4.nc\", \"r\")'
        test1  = 'VAR1 = addfile(\"' + livv.benchmarkDir + '/dome30/diagnostic/dome.1.nc\", \"r\")'
        test4  = 'VAR4 = addfile(\"' + livv.benchmarkDir + '/dome30/diagnostic/dome.4.nc\", \"r\")'
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
        print("  Dome Diagnostic test in progress....")
        
        # Create the plots
        self.plotEvolving()
        
        return
    
    
    #
    # Generates plots for the evolving dome test case.  
    #
    #
    #  
    def plotEvolving(self):
        ncl_path = livv.cwd + os.sep + "plots" 
        dome30dvel_plotfile = ''+ ncl_path + '/dome30/dome30evel.ncl'
        stock1      = 'STOCK1 = addfile(\"'+ livv.benchmarkDir + '/dome30/evolving/dome.1.nc\", \"r\")'
        stock4      = 'STOCK4 = addfile(\"'+ livv.benchmarkDir + '/dome30/evolving//dome.4.nc\", \"r\")'
        VAR1        = 'VAR1 = addfile(\"' + livv.benchmarkDir + '/dome30/evolving/dome.1.nc\", \"r\")'
        VAR4        = 'VAR4 = addfile(\"' + livv.benchmarkDir + '/dome30/evolving/dome.4.nc\", \"r\")'
        pngnamevel  = 'dome30evel.png'
        png         = 'PNG = "' + ncl_path + '/' + pngnamevel + '"'
        plot_dome30dvel = "ncl '" + stock1 + "'  '" + stock4 + "'  '" + VAR1 + "' '" + VAR4 + \
                    "' '" + png + "' " + dome30dvel_plotfile + " >> plot_details.out"
        
        print("    Saving plot details to " + ncl_path + " as " + pngnamevel)
    
        '''
        try:
            subprocess.check_call(plot_dome30dvel, shell=True)
            #print "creating diagnostic dome 30 velocity plots"
        except subprocess.CalledProcessError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.returncode)
        except OSError as e:
            print(str(e)+ ", File: "+ str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]) \
                    + ", Line number: "+ str(sys.exc_info()[2].tb_lineno))
            exit(e.errno)
        '''
        
        return
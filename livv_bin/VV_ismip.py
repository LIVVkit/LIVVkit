'''
Master script for dome test cases

Created on Dec 8, 2014

@author: bzq
'''

import livv
from livv import *
import livv_bin.VV_checks as check
import livv_bin.VV_utilities as util
import livv_bin.VV_outprocess as process
from livv_bin.VV_test import *

class Ismip(AbstractTest):
    
    #
    # Constructor
    #
    def __init__(self):
        self.ismipTestsRun = []
        self.ismipBitForBitDetails = dict()
        self.ismipTestDetails = []
        
        self.name = "ismip"
        self.description = "Simulates steady ice flow over a surface with periodic boundary conditions"
    
    #
    # Return the name of the test
    #
    def getName(self):
        return self.name
    
    
    #
    # Runs the dome specific test case.  Calls some shared resources and
    # some diagnostic/evolving case specific methods.
    #
    #
    #
    def run(self, testCase):
        # Common run 
        self.ismipTestsRun.append(testCase)
        
        # Map the case names to the case functions
        callDict = {'ismip-hom-a/20km' : self.runLargeA,
                    'ismip-hom-c/20km' : self.runLargeC,
                    'ismip-hom-a/80km' : self.runSmallA,
                    'ismip-hom-c/80km' : self.runSmallC }
        
        # Call the correct function
        callDict[testCase]()
         
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
        
        testImgDir = imgDir + os.sep + "ismip"
        testImages = glob.glob(testImgDir + os.sep + "*.png")
        testImages.append( glob.glob(testImgDir + "/*.jpg") )
        testImages.append( glob.glob(testImgDir + "/*.svg") )

        # Set up the template variables  
        templateVars = {"timestamp" : livv.timestamp,
                        "user" : livv.user,
                        "testName" : self.getName(),
                        "indexDir" : livv.indexDir,
                        "cssDir" : livv.cssDir,
                        "testDescription" : self.description,
                        "testsRun" : self.ismipTestsRun,
                        "bitForBitDetails" : self.ismipBitForBitDetails,
                        "imgDir" : testImgDir,
                        "testImages" : testImages}
        outputText = template.render( templateVars )
        page = open(testDir + '/ismip.html', "w")
        page.write(outputText)
        page.close()        
    
    
    #
    # Runs the diagnostic dome specific test case code.  
    #
    #
    #    
    def runLargeA(self):
        print("  Large ismip-hom-a test in progress....")
        return
    
    #
    # Runs the evolving dome specific test case code.
    #
    #
    #
    def runLargeC(self):
        print("  Large ismip-hom-c test in progress....")
        return
    
    #
    # Runs the evolving dome specific test case code.
    #
    #
    #
    def runSmallA(self):
        print("  Small ismip-hom-a test in progress....")
        return
    
    #
    # Runs the evolving dome specific test case code.
    #
    #
    #
    def runSmallC(self):
        print("  Small ismip-hom-c test in progress....")
        return

'''
Master script for gis test cases

Created on Dec 8, 2014

@author: bzq
'''

import livv
from livv import *
from livv_bin.VV_test import *
import jinja2

class Gis(AbstractTest):
    
    #
    # Constructor
    #
    def __init__(self):
        # Mapping of result codes to results
        result = {-1 : 'N/A', 0 : 'SUCCESS', 1 : 'FAILURE'}
        
        # Keep track of what gis test have been run
        self.gisTestsRun = []
        self.gisBitForBitDetails = dict()
        self.gisTestFiles = []
        self.gisTestDetails = []
        self.gisFileTestDetails = []
    
        self.name = "gis"
        self.description = "Attributes: This test case represents the Greenland ice" + \
                  " sheet (GIS) at different spatial resolutions (10km and 5km)." + \
                  " A quasi-no slip boundary condition is applied at the bed. As" + \
                  " with the dome test cases, a zero-flux boundary condition is" + \
                  " applied to the lateral margins. In all test cases, the ice" + \
                  " is taken as isothermal with a constant and uniform rate factor of."
    
    #
    # Return the name of the test
    #
    def getName(self):
        return self.name
    
    #
    # Runs the gis specific test case.  Calls some shared resources and
    # some resolution dependent case specific methods.
    #
    #
    #
    def run(self, testCase):
        # Common run 
        name = testCase
        
        # Map the case names to the case functions
        callDict = {'RUN_GIS_4KM' : self.runSmall,
                    'RUN_GIS_2KM' : self.runMedium,
                    'RUN_GIS_1KM' : self.runLarge }
        
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
        
        indexDir = ".."
        cssDir = indexDir + "/css"
        imgDir = indexDir + "/imgs/gis"
        
        testImgDir = livv.imgDir + os.sep + "gis"
        testImages = [os.path.basename(img) for img in glob.glob(testImgDir + os.sep + "*.png")]
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + "/*.jpg")] )
        testImages.append([os.path.basename(img) for img in glob.glob(testImgDir + "/*.svg")] )

        self.gisFileTestDetails = zip(self.gisTestFiles,self.gisTestDetails)

        # Set up the template variables  
        templateVars = {"timestamp" : livv.timestamp,
                        "user" : livv.user,
                        "testName" : self.getName(),
                        "indexDir" : indexDir,
                        "cssDir" : cssDir,
                        "testDescription" : self.description,
                        "testsRun" : self.gisTestsRun,
                        "bitForBitDetails" : self.gisBitForBitDetails,
                        "testDetails" : self.gisFileTestDetails,
                        "imgDir" : imgDir,
                        "testImages" : testImages}
        outputText = template.render( templateVars )
        page = open(testDir + '/gis.html', "w")
        page.write(outputText)
        page.close()  
    
    
    #
    # Runs the large gis specific test case code.  
    #
    #
    #    
    def runLarge():
        print("  Large gis test in progress....")
        return
    
    #
    # Runs the medium gis specific test case code.
    #
    #
    #
    def runMedium():
        print("  Medium gis test in progress....")
        return
    
    #
    # Runs the small gis specific test case code.
    #
    #
    #
    def runSmall():
        print("  Small gis test in progress....")
        return
    

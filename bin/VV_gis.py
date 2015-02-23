'''
Master module for Greenland Ice Sheet test cases

Created on Dec 8, 2014

@author: arbennett
'''

import livv
from bin.VV_test import AbstractTest
import jinja2

# # Main class for handling Greenland Ice Sheet test cases.
#
#  The GIS test cases inherit functionality from AbstractTest for checking 
#  bit-for-bittedness as well as for parsing standard output from a model run.
#  This class handles resolutions of 4km, 2km, and 1km.
#
class Gis(AbstractTest):
    
    # # Constructor
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
    
        # Some information about the GIS tests
        self.name = "gis"
        self.description = "Attributes: This test case represents the Greenland ice" + \
                  " sheet (GIS) at different spatial resolutions (10km and 5km)." + \
                  " A quasi-no slip boundary condition is applied at the bed. As" + \
                  " with the dome test cases, a zero-flux boundary condition is" + \
                  " applied to the lateral margins. In all test cases, the ice" + \
                  " is taken as isothermal with a constant and uniform rate factor of."
    
    
    # # Return the name of the test
    #
    #  output:
    #    @returns name : Greenland Ice Sheet
    #
    def getName(self):
        return self.name
    
    
    # # Runs the gis specific test case.  
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
        name = testCase
        
        # Map the case names to the case functions
        callDict = {'RUN_GIS_4KM' : self.runSmall,
                    'RUN_GIS_2KM' : self.runMedium,
                    'RUN_GIS_1KM' : self.runLarge}

        # Call the correct function
        callDict[testCase]()

        # More common postprocessing
        return
    
    
    # # Perform V&V on the Greenland Ice Sheet with 1km resolution.  
    #    
    def runLarge():
        print("  Large gis test in progress....")
        return
    
    # # Perform V&V on the Greenland Ice Sheet with 2km resolution.  
    #    
    def runMedium():
        print("  Medium gis test in progress....")
        return
    
    # # Perform V&V on the Greenland Ice Sheet with 4km resolution.  
    #    
    def runSmall():
        print("  Small gis test in progress....")
        return
    

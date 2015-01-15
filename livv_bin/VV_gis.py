'''
Master script for gis test cases

Created on Dec 8, 2014

@author: bzq
'''

import livv
from livv import *
import livv_bin.VV_checks as check
import livv_bin.VV_utilities as util
import livv_bin.VV_outprocess as process
from livv_bin.VV_test import *

class Gis(AbstractTest):
    
    description = "Attributes: This test case represents the Greenland ice" + \
                  " sheet (GIS) at different spatial resolutions (10km and 5km)." + \
                  " A quasi-no slip boundary condition is applied at the bed. As" + \
                  " with the dome test cases, a zero-flux boundary condition is" + \
                  " applied to the lateral margins. In all test cases, the ice" + \
                  " is taken as isothermal with a constant and uniform rate factor of."
    
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
        callDict = {'RUN_GIS_4KM' : runSmall,
                    'RUN_GIS_2KM' : runMedium,
                    'RUN_GIS_1KM' : runLarge }
        
        # Call the correct function
        callDict[testCase]()
         
        # More common postprocessing
        return
    
    
    #
    #  Description
    #
    #
    def generate(self):
        print "This is a placeholder method"
    
    
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
    

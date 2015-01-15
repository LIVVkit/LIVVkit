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
    
    description = "Simulates steady ice flow over a surface with periodic boundary conditions"
    
    #
    # Runs the dome specific test case.  Calls some shared resources and
    # some diagnostic/evolving case specific methods.
    #
    #
    #
    def run(self, testCase):
        # Common run 
        name = testCase
        
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
        print "This is a placeholder method"
    
    
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

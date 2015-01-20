'''
Master script for shelf test cases

Created on Dec 8, 2014

@author: bzq
'''

import livv
from livv import *
from livv_bin.VV_test import *
import jinja2

class Shelf(AbstractTest):
    
    
    name = "shelf"
    description = "a description"
    
    #
    # Return the name of the test
    #
    def getName(self):
        return self.name
    
    #
    # Runs the shelf specific test case.  Calls some shared resources and
    # some circular/confined case specific methods.
    #
    #
    #
    def run(self, testCase):
        # Common run 
        name = testCase
        
        # Map the case names to the case functions
        callDict = {'confined-shelf' : runConfined,
                    'circular-shelf' : runCircular}
        
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
    def runConfined():
        print("  Confined shelf test in progress....")
        return
    
    #
    # Runs the evolving dome specific test case code.
    #
    #
    #
    def runCircular():
        print("  Circular shelf test in progress....")
        return
'''
Master module for dome test cases

Created on Dec 8, 2014

@author: bzq
'''

import re
import os
import sys
import glob
import subprocess
import itertools

import livv
from livv import *
from livv_bin.VV_test import *
import jinja2

## Main class for handling performance test cases.
#
#  The performance test cases inherit functionality from AbstractTest for checking 
#  bit-for-bittedness as well as for parsing standard output from a model run.
#
class Performance(AbstractTest):

    ## Constructor
    #
    def __init__(self):
        # Mapping of result codes to results
        result = {-1 : 'N/A', 0 : 'SUCCESS', 1 : 'FAILURE'}
        
        # Keep track of what dome test have been run
        self.perfTestsRun = []
        self.perfBitForBitDetails = dict()
        self.perfTestFiles = []
        self.perfTestDetails = []
        self.perfFileTestDetails = []
        
        # Describe what the dome tests are all about
        self.name = "performance"
        self.description = "Tests the performance of various test cases." 
    
    
    ## Returns the name of the test
    #
    #  output:
    #    @returns name : Dome
    #
    def getName(self):
        return self.name
    
    
    ## Runs the performance specific test case.  
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
        self.perfTestsRun.append(testCase)
        
        # Map the case names to the case functions
        splitCase = ["".join(x) for _, x in itertools.groupby(testCase, key=str.isdigit)]
        type = splitCase[0]
        resolution = "".join(splitCase[1:])
        callDict = {'dome' : self.runDomePerformance,
                    'gis_' : self.runGisPerformance}
        
        # Call the correct function
        if callDict.has_key(type):
            print("  Running " + type + resolution + " performance test....")
            callDict[type]()
        else: 
            print("  Could not find test code for performance test: " + testCase)
         
        # More common postprocessing
        return
        
        
    #    
    #  DUMMY METHODS FOLLOW
    #
    def runDomePerformance(self):
        print("    This is a placeholder....")
    
    def runGisPerformance(self):
        print("    This is a placeholder....")
    
    def generate(self):
        print("    This is a placeholder....")
    

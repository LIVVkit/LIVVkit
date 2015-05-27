'''
Provides a way to check internal consistency of LIVV's capabilities.
Runs the basic verification tests for a small set of known data that
can be compared with known outputs.

Created on Dec 8, 2014

@author: arbennett
'''

import os
import sys

import verification.dome.Test as Test
import util.variables

'''
Uses a small set of included dome data to ensure that everything in 
LIVV works as planned.
'''
def check():   
    print("Beginning internal consistency checks....")
    print("  Verifying integrity of verification tests....")
    
    # Redirect standard output so that we don't have to see the output of these tests
    sys.stdout = open(os.devnull, "w")
    errorList = []
    dome = Test()
    dome.benchDir = util.variables.cwd + "util" + os.sep + "data" + os.sep + "bench"
    
    # Compare against data that should all match
    dome.modelDir = util.variables.cwd + "util" + os.sep + "data" + os.sep + "same"
    dome.run()
    if not dome.bitForbitDetails["filename.nc"][0] == 'SUCCESS':
        errorList.append("NCDiff recorded differences on results of same test.")

    # Compare against data that has a small difference
    dome.modelDir = util.variables.cwd + "util" + os.sep + "data" + os.sep + "small"
    dome.run()
    if not dome.bitForbitDetails["filename.nc"][0] == 'FAILURE':
        errorList.append("NCDiff failed to record differences on small difference test") 

    # Compare against data that has a large difference
    dome.modelDir = util.variables.cwd + "util" + os.sep + "data" + os.sep + "large"
    dome.run() 
    if not dome.bitForbitDetails["filename.nc"][0] == 'FAILURE':
        errorList.append("NCDiff failed to record differences on small difference test") 

    # Restore standard output so that we can report and continue if possible 
    sys.stdout = sys.__stdout__
    
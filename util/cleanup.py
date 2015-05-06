'''
Clean up all temporary files that were created and may be left behind.

Created on May 6, 2015

@author arbennett
'''
import os
import glob

import util.variables

def clean():
    for dir in os.listdir(util.variables.inputDir):
        [os.remove(file) for file in glob.glob(util.variables.inputDir + os.sep + dir + os.sep + "temp.*")]
        [os.remove(file) for file in glob.glob(util.variables.inputDir + os.sep + dir + os.sep + "*.tmp")]
    for dir in os.listdir(util.variables.benchmarkDir):
        [os.remove(file) for file in glob.glob(util.variables.inputDir + os.sep + dir + os.sep + "temp.*")]
        [os.remove(file) for file in glob.glob(util.variables.inputDir + os.sep + dir + os.sep + "*.tmp")]

'''
Clean up all temporary files that were created and may be left behind.

Created on May 6, 2015

@author arbennett
'''
import os
import glob
import util.variables

''' Removes files that are generated during the LIVV run '''
def clean():
    for subDir in os.listdir(util.variables.inputDir):
        [os.remove(tempFile) for tempFile in glob.glob(util.variables.inputDir + os.sep + subDir + os.sep + "temp.*")]
        [os.remove(tempFile) for tempFile in glob.glob(util.variables.inputDir + os.sep + subDir + os.sep + "*.tmp")]
    for subDir in os.listdir(util.variables.benchmarkDir):
        [os.remove(tempFile) for tempFile in glob.glob(util.variables.inputDir + os.sep + subDir + os.sep + "temp.*")]
        [os.remove(tempFile) for tempFile in glob.glob(util.variables.inputDir + os.sep + subDir + os.sep + "*.tmp")]

'''
Main script to run LIVV.  This script records some user data, sets up the test 
suite, runs the tests, and generates a website based on the results of the tests.

Created on Dec 3, 2014

@author: bzq
'''

###############################################################################
#                                  Imports                                    #
###############################################################################
import os
import time
import getpass

from optparse import OptionParser

import livv_bin.VV_test as vv
import livv_website.VV_website as web

###############################################################################
#                                  Options                                    #
###############################################################################
usage_string = "%prog [options]"
parser = OptionParser(usage=usage_string)
parser.add_option('-d', '--dome', 
                  action='store', 
                  type='choice', 
                  dest='dome', 
                  metavar='PATH', 
                  choices=['none', 'diagnostic', 'evolving', 'all'], 
                  default='diagnostic', 
                  help='specifies the dome tests to run')

parser.add_option('-g', '--gis', 
                  action='store', 
                  type='choice',
                  dest='gis', 
                  metavar='PATH', 
                  choices=['none', 'small', 'medium', 'large'], 
                  default='none', 
                  help='specifies the gis tests to run')

parser.add_option('-m', '--ismip', 
                  action='store', 
                  type='choice', 
                  dest='ismip', 
                  metavar='PATH', 
                  choices=['none', 'small', 'large', 'all'], 
                  default='small', 
                  help='specifies the ismip tests to run')

parser.add_option('-v', '--validation', 
                  action='store', 
                  type='choice', 
                  dest='validation', 
                  metavar='PATH', 
                  choices=['none', 'small', 'large'], 
                  default='none', 
                  help='specifies the validation tests to run')

parser.add_option('-c', '--comment', 
                  action='store', 
                  type='string',
                  dest='comment',
                  default='Test run of code', 
                  help='Log a comment about this run')

parser.add_option('-o', '--outputDir',
                  action='store',
                  type='string',
                  dest='outputDir',
                  default=os.path.dirname(__file__) + "/www",
                  help='Location to output the LIVV webpages.')

parser.add_option('-i', '--inputDir',
                  action='store',
                  type='string',
                  dest='inputDir',
                  default=os.path.dirname(__file__) + "/reg_test",
                  help='Location of the input for running tests.')

parser.add_option('-b', '--benchmarkDir',
                  action='store',
                  type='string',
                  dest='benchmarkDir',
                  default=os.path.dirname(__file__) + "/reg_test/bench",
                  help='Location of the input for running tests.')

# More options should go in to deal with things like the RUN_ANT flag and
#    RUN_VALIDATION set of flags.

(options, args) = parser.parse_args()
###############################################################################
#                             Dependency Checking                             #
###############################################################################
# does this need to be done?

###############################################################################
#                                  Variables                                  #
###############################################################################
inputDir = options.inputDir
benchmarkDir = options.benchmarkDir
outputDir = options.outputDir
imgDir = outputDir + "/imgs"

# Check to make sure the directory structure is okay
if not os.path.exists(inputDir):
    print("Error: Could not find " + inputDir + " for input")
    exit(1)
if not os.path.exists(benchmarkDir):
    print("Error: Could not find " + inputDir + " for input")
    exit(1)
    
###############################################################################
#                              Record Test Cases                              #
###############################################################################
# glam tests
# glissade tests
# large tests
# validation

# TODO: Add/edit test cases to reflect LIVV's reality, also the things above
# TODO: Which of these are resolution vs size ??
# dome tests
domeCases = {'none'   : [],
             'diagnostic' : ['dome30/diagnostic'],
             'evolving'  : ['dome30/evolving'],
             'all'    : ['dome30/diagnostic', 'dome30/evolving'],}
runDomeCase = domeCases[options.dome]

# ismip tests
ismipCases = {'none'  : [],
              'small' : ['ismip-hom-a/80km', 'ismip-hom-c/80km'],
              'large' : ['ismip-hom-a/20km', 'ismip-hom-c/20km'],
              'all'   : ['ismip-hom-a/20km', 'ismip-hom-c/20km', 'ismip-hom-a/80km', 'ismip-hom-c/80km']}
runIsmipCase = ismipCases[options.ismip]

# gis tests
gisCases = {'none'   : [],
            'small'  : ['RUN_GIS_4KM'],
            'medium' : ['RUN_GIS_2KM'],
            'large'  : ['RUN_GIS_1KM']}
runGisCase = gisCases[options.gis]

# validation tests
validationCases = {'none' : [],
                   'small' : ['RUN_VALIDATION'],
                   'large' : ['RUN_VALIDATION', 'RUN_VAL_COUPLED', 'RUN_VAL_DATA', 'RUN_VAL_YEARS', 'RUN_VAL_RANGE']}
runValidationCase = validationCases[options.validation]

# TODO: Eventually would like to record successes and failures in the testSummary
testSummary = [runDomeCase, runIsmipCase, runGisCase, runValidationCase]

###############################################################################
#                               Run Test Cases                                #
###############################################################################
# Flattens testSummary to a single list
tests = [test for sublist in testSummary for test in sublist]
print("Running " + str(tests) + " in " + inputDir)
vv.run(tests, inputDir, benchmarkDir)

###############################################################################
#                              Generate Website                               #
###############################################################################
print("\nGenerating web pages in " + outputDir)
web.generate(outputDir, tests)
print("\nOpen " + outputDir + "/index.html to see test results")
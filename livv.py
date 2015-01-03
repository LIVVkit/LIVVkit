'''
Main script to run LIVV.  This script records some user data, sets up the test 
suite, runs the tests, and generates a website based on the results of the tests.

Created on Dec 3, 2014

@author: bzq
'''

###############################################################################
#                             Dependency Checking                             #
###############################################################################
# 
# TODO:  if needed the script can auto download jinja2 and/or other dependencies
# TODO:  learn about dependency management in python
#

###############################################################################
#                                  Imports                                    #
###############################################################################
import os
import time
import getpass
import platform
import socket

from optparse import OptionParser

# Don't try to import these if we are not calling livv.py directly
if __name__ == '__main__':
    import livv_bin.VV_machines as machines
    import livv_website.VV_website as web
    import livv_bin.VV_test as vv


###############################################################################
#                                  Options                                    #
###############################################################################
usage_string = "%prog [options]"
parser = OptionParser(usage=usage_string)
parser.add_option('--dome', 
                  action='store', 
                  type='choice', 
                  dest='dome', 
                  choices=['none', 'diagnostic', 'evolving', 'all'], 
                  default='diagnostic', 
                  help='specifies the dome tests to run')

parser.add_option('--gis', 
                  action='store', 
                  type='choice',
                  dest='gis', 
                  choices=['none', 'small', 'medium', 'large'], 
                  default='none', 
                  help='specifies the gis tests to run')

parser.add_option('--ismip', 
                  action='store', 
                  type='choice', 
                  dest='ismip', 
                  choices=['none', 'small', 'large', 'all'], 
                  default='small', 
                  help='specifies the ismip tests to run')

parser.add_option('--validation', 
                  action='store', 
                  type='choice', 
                  dest='validation', 
                  choices=['none', 'small', 'large'], 
                  default='none', 
                  help='specifies the validation tests to run')

parser.add_option('--shelf', 
                  action='store', 
                  type='choice', 
                  dest='shelf', 
                  choices=['none', 'confined', 'circular', 'large'], 
                  default='none', 
                  help='specifies the shelf tests to run')

parser.add_option('--comment', 
                  action='store', 
                  type='string',
                  dest='comment',
                  default='Test run of code', 
                  help='Log a comment about this run')

parser.add_option('-o', '--outputDir',
                  action='store',
                  type='string',
                  dest='outputDir',
                  default=os.path.dirname(os.path.abspath(__file__)) + "/www",
                  help='Location to output the LIVV webpages.')

parser.add_option('-i', '--inputDir',
                  action='store',
                  type='string',
                  dest='inputDir',
                  default=os.path.dirname(os.path.abspath(__file__)) + "/reg_test",
                  help='Location of the input for running tests.')

parser.add_option('-b', '--benchmarkDir',
                  action='store',
                  type='string',
                  dest='benchmarkDir',
                  default=os.path.dirname(os.path.abspath(__file__)) + "/reg_test/bench",
                  help='Location of the input for running tests.')

parser.add_option('-m', '--machine',
                  action='store',
                  type='string',
                  dest='machineName',
                  default='',
                  help='Load a preconfigured set of options for a specific machine.')

parser.add_option('-s', '--save',
                  action="store_true", 
                  dest='save',
                  help='Store the configuration being run with the given machine name.')

# More options should go in to deal with things like the RUN_ANT flag and
#    RUN_VALIDATION set of flags.

(options, args) = parser.parse_args()

###############################################################################
#                                  Variables                                  #
###############################################################################
inputDir = options.inputDir             # The location where the test data is 
benchmarkDir = options.benchmarkDir     # The location of the benchmark data
outputDir = options.outputDir           # Where to output the website
imgDir = outputDir + "/imgs"            # Where to store output images


###############################################################################
#                               Main Execution                                #
###############################################################################
if __name__ == '__main__':
    
    # Check if we are saving/loading the configuration and set up the machine name
    if options.machineName == '' and options.save:
        # Save the configuration with the default host name
        machineName = socket.gethostname()
        machines.save(machineName)
    elif options.save:
        # Save the configuration with the specified host name
        machineName = options.machineName
        machines.save(machineName)
    elif options.machineName == '':
        # Don't save the configuration and use the default host name
        machineName = socket.gethostname() 
    else:
        # Try to load the machine name specified
        machineName = options.machineName
        machines.load(machineName)
    
    # Print out some information
    print("---------------------------------------------")
    print("  Land Ice Verification & Validation (LIVV)")
    print("---------------------------------------------")
    print("\n Current run: " + time.strftime("%m-%d-%Y %H:%M:%S"))
    print(" User: " + getpass.getuser())
    print(" Host: " + machineName)
    print(" OS Type: " + platform.system() + " " + platform.release())
    print(" " + options.comment)
    print("")
    
    # Check to make sure the directory structure is okay
    if not os.path.exists(inputDir):
        print("Error: Could not find " + inputDir + " for input")
        exit(1)
    if not os.path.exists(benchmarkDir):
        print("Error: Could not find " + benchmarkDir + " for input")
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
    
    # shelf tests
    shelfCases = {'none' : [],
                  'confined' : ['confined-shelf'],
                  'circular' : ['circular-shelf'],
                  'all' : ['confined-shelf', 'circular-shelf']}
    runShelfCase = shelfCases[options.shelf]
    
    # TODO: Eventually would like to record successes and failures in the testSummary
    testCases = [runDomeCase, runIsmipCase, runGisCase, runValidationCase, runShelfCase]
    testSummary = (("dome","ismip","gis","validation","shelf"),(runDomeCase, runIsmipCase, runGisCase, runValidationCase, runShelfCase))
    
    ###############################################################################
    #                               Run Test Cases                                #
    ###############################################################################
    # Flattens testSummary to a single list
    tests = [test for sublist in testCases for test in sublist]
    print("Running tests: "),
    for test in tests: print("  " + test + " "),
    print("\n")
    vv.run(tests)
    
    ###############################################################################
    #                              Generate Website                               #
    ###############################################################################
    print("\nGenerating web pages in " + outputDir)
    web.generate(testSummary)
    print("\nOpen " + outputDir + "/index.html to see test results")

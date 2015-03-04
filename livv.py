'''
Main script to run LIVV.  This script records some user data, sets up the test 
suite, runs the tests, and generates a website based on the results of the tests.

This script is broken into several main sections.  The first section defines the imports.
For each new module added to LIVV they must be added to this section for the script to 
access them.  Modules that are added internally to LIVV should be added within the __main__
section of the imports to prevent data from being incorrectly shared & from breaking LIVV 
as a whole.  System imports can go outside of __main__, though the libraryList in 
VV_dependencies should be updated if any functionality from outside the standard library is 
added. 

To add or modify the test groupings there are several places that will need to be modified.
First, if adding tests new options will need to be put in place to handle them.  If overall 
test cases are modified the existing options for that test will need to be updated.  The 
last place that will need to be modified is in the RECORD TEST CASES section where the 
tests being run in a particular execution are resolved, and those test cases mapped to the 
delegate test classes (found in livv_bin).

Execution of LIVV proceeds in the RUN TEST CASES section where the totality of the test 
cases are recorded and run grouped by their respective delegate classes.  Each test case
is run using the run method in the class.  This method will run common functionality then
pass off to specialized methods for each test case.  Finally all of the information is 
filled into an html template that contains all of the run information for a grouping of 
tests.

Created on Dec 3, 2014

@author: arbennett
'''


###############################################################################
#                                  Imports                                    #
###############################################################################


    
# Standard python imports can be loaded any time
import os
import time
import getpass
import platform
import socket

from optparse import OptionParser
from collections import OrderedDict

###############################################################################
#                                  Options                                    #
###############################################################################
print "before options"
usage_string = "%prog [options]"
parser = OptionParser(usage=usage_string)
parser.add_option('--dome', 
                  action='store', 
                  type='choice', 
                  dest='dome', 
                  choices=['none', 'diagnostic', 'evolving', 'all'], 
                  default='all', 
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
                  default='all', 
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
                  choices=['none', 'confined', 'circular', 'all'], 
                  default='all', 
                  help='specifies the shelf tests to run')

parser.add_option('--performance', 
                  action='store', 
                  type='choice', 
                  dest='perf', 
                  choices=['none', 'small', 'medium', 'large'], 
                  default='none', 
                  help='specifies the performance tests to run')

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

parser.add_option('-p', '--performanceDir',
                  action='store',
                  type='string',
                  dest='performanceDir',
                  default=os.path.dirname(os.path.abspath(__file__)) + "/perf_test",
                  help='Location of the input for running performance tests.')


parser.add_option('-b', '--benchmarkDir',
                  action='store',
                  type='string',
                  dest='benchmarkDir',
                  default="NOT A REAL FOLDER",
                  help='Location of the input for running tests.')

parser.add_option('-d', '--dataDir',
                  action='store',
                  type='string',
                  dest='dataDir',
                  default='data_titan',
                  help='Subdirectory where data is stored')

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

# Get the options and the arguments
(options, args) = parser.parse_args()
print "After options"
###############################################################################
#                              Global Variables                               #
###############################################################################

# I/O Related variables
cwd = os.path.dirname(os.path.abspath(__file__))
configDir = cwd + os.sep + "configurations"
inputDir = options.inputDir
performanceDir = options.performanceDir
dataDir = options.dataDir
outputDir = options.outputDir
imgDir = outputDir + "/imgs"
comment = options.comment
timestamp = time.strftime("%m-%d-%Y %H:%M:%S")
user = getpass.getuser()

# If the user specifies a benchmark dir honor it, otherwise default to inside of inputDir
if options.benchmarkDir == "NOT A REAL FOLDER":
    benchmarkDir = inputDir + os.sep + "bench"
else:
    benchmarkDir = options.benchmarkDir

# Modules that need to be loaded on big machines
modules = [
           "python/2.7.5", 
           "ncl/6.1.0", 
           "nco/4.3.9", 
           "python_matplotlib/1.3.1", 
           "hdf5/1.8.11", 
           "netcdf/4.1.3", 
           "python_numpy/1.8.0", 
           "python_netcdf4/1.0.6"
          ]

# A list of the information that should be looked for in the stdout of model output
parserVars = [
              'Dycore Type', 
              'Number of processors',
              'Number of timesteps',
              'Avg convergence rate'
              ]
# Build an empty ordered dictionary so that the output prints in a nice order
parserDict = OrderedDict()
for var in parserVars: parserDict[var] = None
parserVars = parserDict

# Test related variables
dome = options.dome
ismip = options.ismip
gis = options.gis
shelf = options.shelf
validation = options.validation
perf = options.perf

# Website related variables
websiteDir = os.path.dirname(__file__) + "/web"
templateDir = websiteDir + "/templates"
indexDir = outputDir
cssDir = indexDir + os.sep + "css"
testDir = indexDir + os.sep + "tests"
imgDir = indexDir + os.sep + "imgs"

###############################################################################
#                               Main Execution                                #
###############################################################################
if __name__ == '__main__':
    print("------------------------------------------------------------------------------")
    print("  Land Ice Verification & Validation (LIVV)")
    print("------------------------------------------------------------------------------")

    # Run the dependency checker
    import bin.VV_dependencies as dependencies
    dependencies.check()

    import bin.VV_machines as machines
    from bin.VV_test import AbstractTest
    from bin.VV_test import TestSummary
    from bin.VV_dome import Dome
    from bin.VV_ismip import Ismip
    from bin.VV_gis import Gis
    from bin.VV_shelf import Shelf
    from bin.VV_performance import Performance   
     
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
        vars = machines.load(machineName)
        globals().update(vars)

    # Check if the user has a default config saved and use that if it does
    if os.path.exists(configDir + os.sep + machineName + "_" + getpass.getuser() + "_default"):
        machineName = machineName + "_" + getpass.getuser() + "_default"
        vars = machines.load(machineName)
        globals().update(vars)

    # Print out some information
    print("\n  Current run: " + time.strftime("%m-%d-%Y %H:%M:%S"))
    print("  User: " + getpass.getuser())
    print("  Config: " + machineName)
    print("  OS Type: " + platform.system() + " " + platform.release())
    print("  " + comment)
    print("")

    # Check to make sure the directory structure is okay
    if not os.path.exists(inputDir):
        print("------------------------------------------------------------------------------")
        print("ERROR: Could not find " + inputDir + " for input")
        print("       Use the -i, -b, and -d flags to specify the locations of the model and comparison data.")
        print("       See README.md for more details.")
        print("------------------------------------------------------------------------------")
        exit(1)
    if not os.path.exists(benchmarkDir):
        print("------------------------------------------------------------------------------")    
        print("ERROR: Could not find " + benchmarkDir + " for input")
        print("       Use the -i, -b, and -d flags to specify the locations of the model and comparison data.")
        print("       See README.md for more details.")
        print("------------------------------------------------------------------------------")
        exit(1)

    ###############################################################################
    #                              Record Test Cases                              #
    ###############################################################################
    # A dictionary describing which module will be called for each test
    # Each of these modules can be found in livv_bin
    testDict = { "dome" : Dome,
                 "ismip" : Ismip,
                 "gis" : Gis,
                 "shelf" : Shelf,
                 "perf" : Performance
               }

    # dome tests
    domeCases = {'none'   : [],
                 'diagnostic' : ['dome30/diagnostic'],
                 'evolving'  : ['dome30/evolving'],
                 'all'    : ['dome30/diagnostic', 'dome30/evolving'],}
    runDomeCase = domeCases[dome]

    # ismip tests
    ismipCases = {'none'  : [],
                  'small' : ['ismip-hom-a/80km', 'ismip-hom-c/80km'],
                  'large' : ['ismip-hom-a/20km', 'ismip-hom-c/20km'],
                  'all'   : ['ismip-hom-a/20km', 'ismip-hom-c/20km', 'ismip-hom-a/80km', 'ismip-hom-c/80km']}
    runIsmipCase = ismipCases[ismip]

    # gis tests
    gisCases = {'none'   : [],
                'small'  : ['gis_4km'],
                'medium' : ['gis_2km'],
                'large'  : ['gis_1km']}
    runGisCase = gisCases[gis]

    # validation tests
    validationCases = {'none' : [],
                       'small' : ['RUN_VALIDATION'],
                       'large' : ['RUN_VALIDATION', 'RUN_VAL_COUPLED', 'RUN_VAL_DATA', 'RUN_VAL_YEARS', 'RUN_VAL_RANGE']}
    runValidationCase = validationCases[validation]

    # shelf tests
    shelfCases = {'none' : [],
                  'confined' : ['confined-shelf'],
                  'circular' : ['circular-shelf'],
                  'all' : ['confined-shelf', 'circular-shelf']}
    runShelfCase = shelfCases[shelf]

    # performance tests
    perfCases = {'none' : [],
                 'small' : ['dome60', 'gis_4km'],
                 'medium' : ['dome120', 'gis_2km'],
                 'large' : ['dome240', 'gix_4km']}
    runPerfCase = perfCases[perf]

    # Describes how to group each test case in with more general groupings
    tests = ["dome", "ismip", "gis", "shelf", "perf"]
    testMapping = {"dome" : runDomeCase,
                   "ismip" : runIsmipCase,
                   "gis" : runGisCase,
                   "shelf" : runShelfCase,
                   "perf" : runPerfCase}

    # Group the tests into their respective cases
    testsRun = []
    for test in tests:
        if len(testMapping[test]):
            testsRun.append(test)

    ###############################################################################
    #                               Run Test Cases                                #
    ###############################################################################
    # Flattens to a list of all test cases being run
    testCases = [test for sublist in [runDomeCase, runIsmipCase, runGisCase, runValidationCase, runShelfCase, runPerfCase] for test in sublist]
    print("Running tests: \n"),
    for test in testCases: print("  " + test + "\n"),
    print("------------------------------------------------------------------------------")
    print("")

    # Run the tests
    testResults, bit4bitResults, testSummary = [], [], []
    print("Beginning test suite....")

    summary = TestSummary()
    summary.webSetup(testsRun)
    for test in testsRun:
        # Create a new instance of the specific test class (see testDict for the mapping)
        newTest = testDict[test]()
        # Run the specific and bit for bit tests for each case of the test
        for case in testMapping[test]:
            newTest.run(case)
        testSummary.append(newTest.getSummary())
        print("")

        # Generate the test-specific webpage 
        newTest.generate()

    # Create the site index
    print("Generating web pages in " + outputDir) 
    summary.generate(testsRun, testMapping, testSummary)

    ###############################################################################
    #                        Finished.  Tell user about it.                       #
    ###############################################################################
    print("------------------------------------------------------------------------------")
    print("Finished running LIVV.  Results:  ")
    print("  Open " + outputDir + "/index.html to see test results")
    print("------------------------------------------------------------------------------")


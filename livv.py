'''
Main script to run LIVV.  This script records some user data, sets up the test 
suite, runs the tests, and generates a website based on the results of the tests.

Created on Dec 3, 2014

@author: bzq
'''


###############################################################################
#                                  Imports                                    #
###############################################################################

# Don't try to import these if we are not calling livv.py directly
if __name__ == '__main__':    
    print("------------------------------------------------------------------------------")
    print("  Land Ice Verification & Validation (LIVV)")
    print("------------------------------------------------------------------------------")
    
    # Run the dependency checker
    import livv_bin.VV_dependencies as dependencies
    dependencies.check()
    
    import livv_bin.VV_machines as machines
    import livv_website.VV_website as web
    from livv_bin.VV_test import AbstractTest
    from livv_bin.VV_test import GenericTest
    from livv_bin.VV_dome import Dome
    from livv_bin.VV_ismip import Ismip
    from livv_bin.VV_gis import Gis
    from livv_bin.VV_shelf import Shelf
    

    
    # A dictionary describing which module will be called for each test
    # Each of these modules can be found in livv_bin
    testDict = { "dome" : Dome,
                 "ismip" : Ismip,
                 "gis" : Gis,
                 "shelf" : Shelf
               }
import os
import time
import getpass
import platform
import socket

from optparse import OptionParser

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

# More options should go in to deal with things like the RUN_ANT flag and
#    RUN_VALIDATION set of flags.

(options, args) = parser.parse_args()

###############################################################################
#                              Global Variables                               #
###############################################################################

# I/O Related variables
cwd = os.path.dirname(os.path.abspath(__file__))  
inputDir = options.inputDir                       
benchmarkDir = options.benchmarkDir
dataDir = '/' + options.dataDir
outputDir = options.outputDir                    
imgDir = outputDir + "/imgs"                     
comment = options.comment                         
timestamp = time.strftime("%m-%d-%Y %H:%M:%S")
user = getpass.getuser()

# Test related variables
dome = options.dome
ismip = options.ismip
gis = options.gis
shelf = options.shelf
validation = options.validation

# Website related variables
websiteDir = os.path.dirname(__file__) + "/livv_website"
templateDir = websiteDir + "/templates"
indexDir = outputDir
cssDir = indexDir + os.sep + "css"
testDir = indexDir + os.sep + "tests"
imgDir = indexDir + os.sep + "imgs"

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
        print("Error: Could not find " + inputDir + " for input")
        exit(1)
    if not os.path.exists(benchmarkDir):
        print("Error: Could not find " + benchmarkDir + " for input")
        exit(1)
        
    ###############################################################################
    #                              Record Test Cases                              #
    ###############################################################################

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
                'small'  : ['RUN_GIS_4KM'],
                'medium' : ['RUN_GIS_2KM'],
                'large'  : ['RUN_GIS_1KM']}
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
       
    # Describes how to group each test case in with more general groupings
    tests = ["dome", "ismip", "gis", "shelf"]
    testMapping = {"dome" : runDomeCase,
                   "ismip" : runIsmipCase,
                   "gis" : runGisCase,
                   "shelf" : runShelfCase}

    # Group the tests into their respective cases
    testsRun = []
    for test in tests:
        if len(testMapping[test]):
            testsRun.append(test)
    
    ###############################################################################
    #                               Run Test Cases                                #
    ###############################################################################
    # Flattens to a list of all test cases being run
    testCases = [test for sublist in [runDomeCase, runIsmipCase, runGisCase, runValidationCase, runShelfCase] for test in sublist]
    print("Running tests: \n"),
    for test in testCases: print("  " + test + "\n"),
    print("------------------------------------------------------------------------------")
    print("")
    
    # Run the tests
    testResults = []
    bit4bitResults = []
    print("Beginning test suite....")
    newTest = GenericTest()
    newTest.webSetup(testsRun, testCases)
    for test in testsRun:
        # Create a new instance of the specific test class (see testDict for the mapping)
        newTest = testDict[test]()
        # Run the specific and bit for bit tests for each case of the test
        for case in testMapping[test]:
            newTest.run(case)
        print("")

        # Generate the test-specific webpage 
        newTest.generate()
        
    # On the last test generate the common web resources
    print("Generating web pages in " + outputDir)
    
    ###############################################################################
    #                              Generate Website                               #
    ###############################################################################
    print("------------------------------------------------------------------------------")
    print("Finished running LIVV.  Results:  ")
    print("  Open " + outputDir + "/index.html to see test results")
    print("------------------------------------------------------------------------------")


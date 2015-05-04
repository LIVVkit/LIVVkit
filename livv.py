'''
Main script to run LIVV.  This script records some user data, sets up the test 
suite, runs the verification, and generates a website based on the results of the verification.

This script is broken into several main sections.  The first section defines the imports.
For each new module added to LIVV they must be added to this section for the script to 
access them.  Modules that are added internally to LIVV should be added within the __main__
section of the imports to prevent data from being incorrectly shared & from breaking LIVV 
as a whole.  System imports can go outside of __main__, though the libraryList in 
dependencies should be updated if any functionality from outside the standard library is 
added. 

To add or modify the test groupings there are several places that will need to be modified.
First, if adding verification new options will need to be put in place to handle them.  If overall 
test cases are modified the existing options for that test will need to be updated.  The 
last place that will need to be modified is in the RECORD TEST CASES section where the 
verification being run in a particular execution are resolved, and those test cases mapped to the 
delegate test classes (found in livv_bin).

Some information stored in the GLOBAL VARIABLES section may be of interest.  If modifications to
LIVV require that new modules be loaded on LCF machines they can be defined in the modules variable.
These modules are automatically checked by the dependency checker before running the test cases.
The definitions for the variables pulled from standard output files is also recorded here.  If the
parser needs to look for new information the variables of interest should be added to this list.

Execution of LIVV proceeds in the RUN TEST CASES section where the totality of the test 
cases are recorded and run grouped by their respective delegate classes.  Each test case
is run using the run method in the class.  This method will run common functionality then
pass off to specialized methods for each test case.  Finally all of the information is 
filled into an html template that contains all of the run information for a grouping of 
verification.

Created on Dec 3, 2014

@authors: arbennett, jhkennedy
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
import itertools

from optparse import OptionParser
from collections import OrderedDict

###############################################################################
#                                  Options                                    #
###############################################################################

#NOTE: be careful here! We just want to get our optional argument choices. 
# Everything else should be imported in __main__!
from verification.dome import choices as domeVerificationChoices
from verification.ismip import choices as ismipVerificationChoices
from verification.shelf import choices as shelfVerificationChoices
from performance.dome import choices as domePerformanceChoices
from performance.gis import choices as gisPerformanceChoices

usage_string = "%prog [options]"
parser = OptionParser(usage=usage_string)
parser.add_option('--dome', action='store', 
                  type='choice', dest='dome', 
                  choices=domeVerificationChoices(), default='all', 
                  help='specifies the dome verification to run')


parser.add_option('--ismip', action='store', 
                  type='choice', dest='ismip', 
                  choices=ismipVerificationChoices(), default='none', 
                  help='specifies the ismip verification to run')

parser.add_option('--shelf', action='store', 
                  type='choice', dest='shelf', 
                  choices=shelfVerificationChoices(), default='all', 
                  help='specifies the shelf verification to run')

parser.add_option('--performanceDome', action='store', 
                  type='choice', dest='perfDome', 
                  choices=domePerformanceChoices(), default='none', 
                  help='specifies the dome performance verification to run')

parser.add_option('--performanceGreenland', action='store', 
                  type='choice', dest='perfGis', 
                  choices=gisPerformanceChoices(), default='none', 
                  help='specifies the greenland performance verification to run')

parser.add_option('--comment', action='store', 
                  type='string', dest='comment',
                  default='Test run of code', 
                  help='Log a comment about this run')

parser.add_option('-o', '--outputDir', action='store',
                  type='string', dest='outputDir',
                  default=os.path.dirname(os.path.abspath(__file__)) + os.sep + "www",
                  help='Location to output the LIVV webpages.')

parser.add_option('-i', '--inputDir', action='store',
                  type='string', dest='inputDir',
                  default=os.path.dirname(os.path.abspath(__file__)) + os.sep + "reg_test",
                  help='Location of the input for running verification.')

parser.add_option('-p', '--performanceDir', action='store',
                  type='string', dest='performanceDir',
                  default=os.path.dirname(os.path.abspath(__file__)) + os.sep + "reg_test",
                  help='Location of the input for running performance verification.')

parser.add_option('-b', '--benchmarkDir', action='store',
                  type='string', dest='benchmarkDir',
                  default=os.path.dirname(os.path.abspath(__file__)) + os.sep + "reg_bench",
                  help='Location of the input for running verification.')

parser.add_option('-d', '--dataDir', action='store',
                  type='string', dest='dataDir', default='data_titan',
                  help='Subdirectory where data is stored')

parser.add_option('-m', '--machine', action='store',
                  type='string', dest='machineName', default='',
                  help='Load a preconfigured set of options for a specific machine.')

parser.add_option('-s', '--save', action="store_true", dest='save',
                  help='Store the configuration being run with the given machine name.')

# Get the options and the arguments
(options, args) = parser.parse_args()

###############################################################################
#                              Global Variables                               #
###############################################################################

# I/O Related variables
cwd            = os.path.dirname(os.path.abspath(__file__))
configDir      = cwd + os.sep + "configurations"
inputDir       = options.inputDir
benchmarkDir   = options.benchmarkDir
performanceDir = options.performanceDir
dataDir        = options.dataDir
outputDir      = options.outputDir
imgDir         = outputDir + "/imgs"
comment        = options.comment
timestamp      = time.strftime("%m-%d-%Y %H:%M:%S")
user           = getpass.getuser()
websiteDir     = cwd + "/web"
templateDir    = websiteDir + "/templates"
indexDir       = outputDir  

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

# Variables to measure when parsing through timing summaries
timingVars = [
              'Simple Glide',
              'Velocity Driver',
              'Initial Diagonal Solve',
              'IO Writeback'
             ]

# Dycores to try to parse output for
dycores = ['glissade'] #["glide", "glissade", "glam", "albany", "bisicles"]

###############################################################################
#                               Main Execution                                #
###############################################################################
if __name__ == '__main__':
    print("------------------------------------------------------------------------------")
    print("  Land Ice Verification & Validation (LIVV)")
    print("------------------------------------------------------------------------------")

    # Run the dependency checker
    import util.dependencies as dependencies
    dependencies.check()

    # Pull in the LIVV specific modules
    import util.configurationHandler
    import util.websetup
    import verification.dome, verification.ismip, verification.shelf
    import performance.dome, performance.gis

    # Check if we are saving/loading the configuration and set up the machine name
    if options.machineName == '' and options.save:
        # Save the configuration with the default host name
        machineName = socket.gethostname()
        util.configurationHandler.save(machineName)
    elif options.save:
        # Save the configuration with the specified host name
        machineName = options.machineName
        util.configurationHandler.save(machineName)
    elif options.machineName == '':
        # Don't save the configuration and use the default host name
        machineName = socket.gethostname() 
    else:
        # Try to load the machine name specified
        machineName = options.machineName
        vars = util.configurationHandler.load(machineName)
        globals().update(vars)

    # Check if the user has a default config saved and use that if it does
    if os.path.exists(configDir + os.sep + machineName + "_" + user + "_default"):
        machineName = machineName + "_" + user + "_default"
        vars = util.configurationHandler.load(machineName)
        globals().update(vars)

    # Print out some information
    print("\n  Current run: " + time.strftime("%m-%d-%Y %H:%M:%S"))
    print("  User: " + user)
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

    # Describes the test module and the cases to run for said module
    #NOTE: Each of these modules can be found in bin
    verificationMapping = {
                    "dome" : ( verification.dome.Test, verification.dome.choose(options.dome) ),
                   "ismip" : ( verification.ismip.Test, verification.ismip.choose(options.ismip) ),
                   "shelf" : ( verification.shelf.Test, verification.shelf.choose(options.shelf) )
                   }

    perfMapping = {
                   "dome" : ( performance.dome.Test, performance.dome.choose(options.perfDome) ),
                   "gis" : ( performance.gis.Test, performance.gis.choose(options.perfGis))
                   }

    validationMapping = {
                         "validation" : (0,0)
                         }

    testMapping = {
                   "Verification" : verificationMapping,
                   "Performance" : perfMapping,
                   "Validation" : validationMapping
                   }

    # Get the keys for all non-empty test cases
    testsRun = list( itertools.compress( verificationMapping.keys(), [val[1] for val in verificationMapping.values()]) )
    perfTestsRun = list( itertools.compress( perfMapping.keys(), [val[1] for val in perfMapping.values()]) )
    validationTestsRun = list( itertools.compress( validationMapping.keys(), [val[1] for val in validationMapping.values()]))

    ###############################################################################
    #                               Run Test Cases                                #
    ###############################################################################
    print("Running V&V verification:")
    for case in itertools.chain.from_iterable( [verificationMapping[test][1] for test in testsRun] ): 
        print("  " + case)
    print("")
    print("Running performance verification:")
    for case in itertools.chain.from_iterable( [perfMapping[test][1] for test in perfTestsRun] ): 
        print("  " + case)
    print("")
    print("Running validation verification:")
    for case in itertools.chain.from_iterable( [validationMapping[test][1] for test in validationTestsRun] ): 
        print("  " + case)
    print("")

    # Set up the directory structure and summary dictionaries for output
    verificationSummary, performanceSummary, validationSummary = dict(), dict(), dict()
    util.websetup.setup(testsRun + perfTestsRun + validationTestsRun)

    # Run the verification tests
    if len(testsRun) > 0:
        print("--------------------------------------------------------------------------")
        print("  Beginning verification test suite....")
        print("--------------------------------------------------------------------------")
    for test in testsRun:
        # Create a new instance of the specific test class (see verificationMapping for the mapping)
        newTest = verificationMapping[test][0]()
        # Run the specific and bit for bit verification for each case of the test
        for case in verificationMapping[test][1]:
            newTest.run(case)
        verificationSummary[test] = newTest.summary
        print("")
        # Generate the test-specific webpage 
        newTest.generate()

    # Run the performance verification
    if len(perfTestsRun) > 0:
        print("--------------------------------------------------------------------------")
        print("  Beginning performance analysis....")
        print("--------------------------------------------------------------------------")
    for test in perfTestsRun:
        # Create a new instance of the specific test class (see verificationMapping for the mapping)
        newTest = perfMapping[test][0]()
        # Run the specific and bit for bit verification for each case of the test
        for case in perfMapping[test][1]:
            newTest.run(case)
        performanceSummary[test] = newTest.summary
        print("")
        # Generate the test-specific webpage 
        newTest.generate()

    # Run the validation verification
    if len(validationTestsRun) > 0:
        print("--------------------------------------------------------------------------")
        print("  Beginning validation test suite....")
        print("--------------------------------------------------------------------------")
    for test in validationTestsRun:
        # Create a new instance of the specific test class (see verificationMapping for the mapping)
        newTest = validationMapping[test][0]()
        # Run the specific and bit for bit verification for each case of the test
        for case in validationMapping[test][1]:
            newTest.run(case)
        validationSummary[test] = newTest.summary
        print("")
        # Generate the test-specific webpage 
        newTest.generate()

    # Create the site index
    print("Generating web pages in " + outputDir) 
    util.websetup.generate(verificationSummary, performanceSummary, validationSummary)

    ###############################################################################
    #                        Finished.  Tell user about it.                       #
    ###############################################################################
    print("------------------------------------------------------------------------------")
    print("Finished running LIVV.  Results:  ")
    print("  Open " + outputDir + "/index.html to see test results")
    print("------------------------------------------------------------------------------")

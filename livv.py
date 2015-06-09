#!/usr/bin/env python

'''
Main script to run LIVV.  This script records some user data, sets up the test 
suite, runs the verification, and generates a website based on the results of the verification.

This script is broken into several main sections.  The first section defines the imports.
For each new module added to LIVV they must be added to this section for the script to 
access them.  The libraryList in util.dependencies should be updated if any functionality 
from outside the standard library is added. 

To add or modify the test groupings there are several places that will need to be modified.
First, the base module (found in verification, validation, or performance) will need to have 
the new test added to the cases dictionary.  A new entry may need to be put into the test specific
module as well; performance tests require this, verfication tests do not.  Finally, a new entry for
the test will need to be added to the appropriate test mapping in the RECORD TEST CASES section.

Execution of LIVV proceeds in the RUN TEST CASES section where the totality of the test 
cases are recorded and run grouped by their respective delegate classes.  Each test case
is run using the run method in the class.  This method will run common functionality then
pass off to specialized methods for each test case.  Finally all of the information is 
filled into an html template that contains all of the run information for a grouping of 
verification.

Created on Dec 3, 2014

@authors: arbennett, jhkennedy
'''
print("------------------------------------------------------------------------------")
print("  Land Ice Verification & Validation (LIVV)")
print("------------------------------------------------------------------------------")


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

from verification.base import choices as verificationChoices
from performance.base import choices as performanceChoices
from validation.base import choices as validationChoices
###############################################################################
#                                  Options                                    #
###############################################################################
usage_string = "%prog [options]"
parser = OptionParser(usage=usage_string)
parser.add_option('--verification', action='store', 
                  type='choice', dest='verification', 
                  choices=verificationChoices(), default='all', 
                  help='specifies the verification tests to run')

parser.add_option('--performance', action='store', 
                  type='choice', dest='performance', 
                  choices=performanceChoices(), default='none', 
                  help='specifies the performance tests to run')

parser.add_option('--validation', action='store', 
                  type='choice', dest='validation', 
                  choices=validationChoices(), default='none', 
                  help='specifies the validation tests to run')

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
                  default=os.path.dirname(os.path.abspath(__file__)) + os.sep + "reg_test" + os.sep + "linux-gnu" + os.sep + "higher-order",
                  help='Location of the input for running verification.')

parser.add_option('-b', '--benchmarkDir', action='store',
                  type='string', dest='benchmarkDir',
                  default=os.path.dirname(os.path.abspath(__file__)) + os.sep + "reg_bench" + os.sep + "linux-gnu" + os.sep + "higher-order",
                  help='Location of the input for running verification.')

parser.add_option('--load', action='store',
                  type='string', dest='loadName', default='',
                  help='Load a preconfigured set of options for the given machine name.')

parser.add_option('--save', action="store", dest='saveName', default='',
                  help='Store the configuration being run with the given machine name.')

# Get the options and the arguments
(options, args) = parser.parse_args()

# Pull in the LIVV specific modules
import util.dependencies
util.dependencies.check()
import util.variables
import util.configurationHandler
import util.websetup
import util.selfVerification
import verification.dome, verification.ismip, verification.shelf, verification.stream
import performance.dome, performance.gis
import validation.gis
import util.cleanup

###############################################################################
#                              Global Variables                               #
###############################################################################
util.variables.cwd            = os.getcwd()
util.variables.configDir      = util.variables.cwd + os.sep + "configurations"
util.variables.inputDir       = options.inputDir
util.variables.benchmarkDir   = options.benchmarkDir
util.variables.outputDir      = options.outputDir
util.variables.imgDir         = util.variables.outputDir + "/imgs"
util.variables.comment        = options.comment
util.variables.timestamp      = time.strftime("%m-%d-%Y %H:%M:%S")
util.variables.user           = getpass.getuser()
util.variables.websiteDir     = util.variables.cwd + "/web"
util.variables.templateDir    = util.variables.websiteDir + "/templates"
util.variables.indexDir       = util.variables.outputDir
util.variables.verification   = options.verification
util.variables.performance    = options.performance
util.variables.validation     = options.validation

# A list of the information that should be looked for in the stdout of model output
util.variables.parserVars = [
              'Dycore Type', 
              'Number of processors',
              'Number of timesteps',
              'Avg convergence rate'
             ]

# Variables to measure when parsing through timing summaries
util.variables.timingVars = ['Time'
             # 'Simple Glide',
             # 'Velocity Driver',
             # 'Initial Diagonal Solve',
             # 'IO Writeback'
             ]

# Dycores to try to parse output for
util.variables.dycores = ['glissade'] #["glide", "glissade", "glam", "albany", "bisicles"]


###############################################################################
#                               Main Execution                                #
###############################################################################


# Check if we are saving/loading the configuration and set up the machine name
machineName = socket.gethostname()
if options.saveName != '':
    # Save the configuration with the default host name
    machineName = options.saveName
    util.configurationHandler.save(machineName)
elif options.loadName != '':
    # Try to load the machine name specified
    machineName = options.loadName
    vars = util.configurationHandler.load(machineName)
    util.variables.update(vars)

# Check if the user has a default config saved and use that if it does
if os.path.exists(util.variables.configDir + os.sep + machineName + "_" + util.variables.user + "_default"):
    machineName = machineName + "_" + util.variables.user + "_default"
    vars = util.configurationHandler.load(machineName)
    #util.variables.globals().update(vars)

# Print out some information
print(os.linesep + "  Current run: " + time.strftime("%m-%d-%Y %H:%M:%S"))
print("  User: " + util.variables.user)
print("  Config: " + machineName)
print("  OS Type: " + platform.system() + " " + platform.release())
print("  " + util.variables.comment + os.linesep)

# Check to make sure the directory structure is okay
for dir in [util.variables.inputDir, util.variables.benchmarkDir]:
    if not os.path.exists(dir):
        print("------------------------------------------------------------------------------")
        print("ERROR: Could not find " + dir + " for input")
        print("       Use the -i, -b, and -d flags to specify the locations of the model and comparison data.")
        print("       See README.md for more details.")
        print("------------------------------------------------------------------------------")
        exit(1)

###############################################################################
#                              Record Test Cases                              #
###############################################################################
verificationMapping = {
                       'dome' : verification.dome.Test,
                       'ismip' : verification.ismip.Test,
                       'shelf' : verification.shelf.Test,
                       'stream' : verification.stream.Test
                       }

performanceMapping = {
                      'dome' : performance.dome.Test,
                      'gis' : performance.gis.Test
                      }

validationMapping = {
                     'gis' : validation.gis.Test
                     }

verificationTests = verification.base.choose(util.variables.verification)
performanceTests = performance.base.choose(util.variables.performance)
validationTests = validation.base.choose(util.variables.validation)
testMapping = {
               "Verification" : verificationTests,
               "Performance" : performanceTests,
               "Validation" : validationTests
               }

###############################################################################
#                               Run Test Cases                                #
###############################################################################
# Do a quick check to make sure that analysis works the way we want it to
util.selfVerification.check()

# Give a list of the tests that will be run
if len(verificationTests) > 0:  
    print("Running verification tests:")
    for case in verificationTests: 
        print("  " + case)
if len(performanceTests) > 0:
    print(os.linesep + "Running performance tests:")
    for case in performanceTests:
        print("  " + case)
if len(validationTests) > 0:
    print(os.linesep + "Running validation tests:")
    for case in validationTests:
        print("  " + case)

# Set up the directory structure and summary dictionaries for output
verificationSummary, performanceSummary, validationSummary = dict(), dict(), dict()
util.websetup.setup(verificationTests + performanceTests + validationTests)

# Run the verification tests
if len(verificationTests) > 0:
    print("--------------------------------------------------------------------------")
    print("  Beginning verification test suite....")
    print("--------------------------------------------------------------------------")
for test in verificationTests:
    # Create a new instance of the specific test class (see verificationMapping for the mapping)
    newTest = verificationMapping[test]()
    newTest.run()
    verificationSummary[test] = newTest.summary
    newTest.generate()
    print("")

# Run the performance verification
if len(performanceTests) > 0:
    print("--------------------------------------------------------------------------")
    print("  Beginning performance analysis....")
    print("--------------------------------------------------------------------------")
for test in performanceTests:
    # Create a new instance of the specific test class (see verificationMapping for the mapping)
    newTest = performanceMapping[test]()
    newTest.run()
    performanceSummary[test] = newTest.summary
    newTest.generate()
    print("")

# Run the validation verification
if len(validationTests) > 0:
    print("--------------------------------------------------------------------------")
    print("  Beginning validation test suite....")
    print("--------------------------------------------------------------------------")
for test in validationTests:
    # Create a new instance of the specific test class (see verificationMapping for the mapping)
    newTest = validationMapping[test]()
    # Run the specific and bit for bit verification for each case of the test
    newTest.run()
    validationSummary[test] = newTest.summary
    # Generate the test-specific webpage 
    newTest.generate()
    print("")

# Create the site index
print("Generating web pages in " + util.variables.outputDir + "....")
util.websetup.generate(verificationSummary, performanceSummary, validationSummary)

print("Cleaning up....")
util.cleanup.clean()

###############################################################################
#                        Finished.  Tell user about it.                       #
###############################################################################
print("------------------------------------------------------------------------------")
print("Finished running LIVV.  Results:  ")
print("  Open " + util.variables.outputDir + "/index.html to see test results")
print("------------------------------------------------------------------------------")

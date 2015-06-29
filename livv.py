#!/usr/bin/env python

# Copyright (c) 2015, UT-BATTELLE, LLC
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Main script to run LIVV.  This script records some user data, sets up the test 
suite, runs the verification, and generates a website based on the results of the verification.

This script is broken into several main sections.  The first section defines the imports.
For each new module added to LIVV they must be added to this section for the script to 
access them.  The library_list in util.dependencies should be updated if any functionality 
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
"""
print("------------------------------------------------------------------------------")
print("  Land Ice Verification & Validation (LIVV)")
print("------------------------------------------------------------------------------")
print("  Load modules: python, ncl, nco, python_matplotlib, hdf5, netcdf, python_numpy, and python_netcdf4 for best results.")
###############################################################################
#                                  Imports                                    #
###############################################################################

# Standard python imports can be loaded any time
import os
import time
import getpass
import platform
import socket
import time
import multiprocessing

from optparse import OptionParser

###############################################################################
#                                  Options                                    #
###############################################################################
usage_string = "%prog [options]"
parser = OptionParser(usage=usage_string)
parser.add_option('--performance', action='store_true', 
                  dest='performance', help='specifies whether to run the performance tests')

parser.add_option('--comment', action='store', 
                  type='string', dest='comment',
                  default='Test run of code', 
                  help='Log a comment about this run')

parser.add_option('-o', '--out-dir', action='store',
                  type='string', dest='output_dir',
                  default=os.path.dirname(os.path.abspath(__file__)) + os.sep + "www",
                  help='Location to output the LIVV webpages.')

parser.add_option('-t', '--test-dir', action='store',
                  type='string', dest='input_dir',
                  default=os.path.dirname(os.path.abspath(__file__)) + os.sep + "reg_test" + os.sep + "linux-gnu",
                  help='Location of the input for running verification.')

parser.add_option('-b', '--bench-dir', action='store',
                  type='string', dest='benchmark_dir',
                  default=os.path.dirname(os.path.abspath(__file__)) + os.sep + "reg_bench" + os.sep + "linux-gnu",
                  help='Location of the input for running verification.')

parser.add_option('--load', action='store',
                  type='string', dest='load_name', default='',
                  help='Load a preconfigured set of options for the given machine name.')

parser.add_option('--save', action="store", dest='save_name', default='',
                  help='Store the configuration being run with the given machine name.')

# Get the options and the arguments
(options, args) = parser.parse_args()

# Pull in the LIVV specific modules
import util.dependencies
util.dependencies.check()
import util.variables
import util.configuration_handler
import util.websetup
import util.self_verification
import verification.dome, verification.ismip, verification.shelf, verification.stream
import performance.dome
import util.cleanup

###############################################################################
#                              Global Variables                               #
###############################################################################
util.variables.cwd             = os.getcwd()
util.variables.config_dir      = util.variables.cwd + os.sep + "configurations"
util.variables.input_dir       = options.input_dir + os.sep + 'higher-order'
util.variables.benchmark_dir   = options.benchmark_dir + os.sep + 'higher-order'
util.variables.output_dir      = options.output_dir
util.variables.img_dir         = util.variables.output_dir + "/imgs"
util.variables.comment         = options.comment
util.variables.timestamp       = time.strftime("%m-%d-%Y %H:%M:%S")
util.variables.user            = getpass.getuser()
util.variables.website_dir     = util.variables.cwd + "/web"
util.variables.template_dir    = util.variables.website_dir + "/templates"
util.variables.index_dir       = util.variables.output_dir
util.variables.verification    = "True"
util.variables.performance     = str(options.performance)
util.variables.validation      = "False"

# A list of the information that should be looked for in the stdout of model output
util.variables.parser_vars = [
              'Dycore Type', 
              'Number of processors',
              'Number of timesteps',
              'Avg convergence rate'
             ]

# Variables to measure when parsing through timing summaries
util.variables.timing_vars = ['Time'
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
machine_name = socket.gethostname()
if options.save_name != '':
    # Save the configuration with the default host name
    machine_name = options.save_name
    util.configuration_handler.save(machine_name)
elif options.load_name != '':
    # Try to load the machine name specified
    machine_name = options.load_name
    vars = util.configuration_handler.load(machine_name)
    util.variables.update(vars)

# Check if the user has a default config saved and use that if it does
if os.path.exists(util.variables.config_dir + os.sep + machine_name + "_" + util.variables.user + "_default"):
    machine_name = machine_name + "_" + util.variables.user + "_default"
    vars = util.configuration_handler.load(machine_name)
    #util.variables.globals().update(vars)

# Print out some information
print(os.linesep + "  Current run: " + time.strftime("%m-%d-%Y %H:%M:%S"))
print("  User: " + util.variables.user)
print("  Config: " + machine_name)
print("  OS Type: " + platform.system() + " " + platform.release())
print("  " + util.variables.comment + os.linesep)

# Check to make sure the directory structure is okay
for dir in [util.variables.input_dir, util.variables.benchmark_dir]:
    if not os.path.exists(dir):
        print("------------------------------------------------------------------------------")
        print("ERROR: Could not find " + dir + " for input")
        print("       Use the -t and -b flags to specify the locations of the test and benchmark data.")
        print("       See README.md for more details.")
        print("------------------------------------------------------------------------------")
        exit(1)

###############################################################################
#                              Record Test Cases                              #
###############################################################################
verification_tests = [verification.dome, verification.ismip, verification.shelf, verification.stream] 
performance_tests = [performance.dome]
validation_tests = []
test_mapping = {
               "Verification" : verification_tests,
               "Performance" : performance_tests,
               "Validation" : validation_tests}

###############################################################################
#                               Run Test Cases                                #
###############################################################################
# Set up the directory structure for output
util.websetup.setup(verification_tests + performance_tests + validation_tests)

# Do a quick check to make sure that analysis works the way we want it to
util.self_verification.check()

# Give a list of the tests that will be run
print("Running verification tests:")
for case in verification_tests: 
    print("  " + case.get_name())
if util.variables.performance == "True":
    print(os.linesep + "Running performance tests:")
    for case in performance_tests:
        print("  " + case.get_name())
if util.variables.validation == "True":
    print(os.linesep + "Running validation tests:")
    for case in validation_tests:
        print("  " + case.get_name())

# Run the verification tests
manager = multiprocessing.Manager()
output = multiprocessing.Queue()
verification_summary = manager.dict()
performance_summary = manager.dict()
validation_summary = manager.dict()
verification_processes = [multiprocessing.Process(target=ver_type.Test().run, args=(verification_summary, output)) for ver_type in verification_tests]
if util.variables.verification == "True":
    print("--------------------------------------------------------------------------")
    print("  Beginning verification test suite....")
    print("--------------------------------------------------------------------------")
    # Spawn a new process for each test
    for p in verification_processes:
        p.start()
        p.join()
    
    # Wait for all of the tests to finish
    while len(multiprocessing.active_children()) > 3:
        time.sleep(0.25)

    # Show the results
    while output.qsize() > 0:
        print output.get()

# Run the performance verification
if util.variables.performance == "True":
    print("--------------------------------------------------------------------------")
    print("  Beginning performance analysis....")
    print("--------------------------------------------------------------------------")
    for test in performance_tests:
        # Create a new instance of the specific test class (see verification_mapping for the mapping)
        new_test = test.Test()
        new_test.run()
        performance_summary[test.get_name().lower()] = new_test.summary
        new_test.generate()
        print("")

# Run the validation verification
if util.variables.validation == "True":
    print("--------------------------------------------------------------------------")
    print("  Beginning validation test suite....")
    print("--------------------------------------------------------------------------")
    for test in validation_tests:
        # Create a new instance of the specific test class (see verification_mapping for the mapping)
        new_test = validation_mapping[test]()
        # Run the specific and bit for bit verification for each case of the test
        new_test.run()
        validation_summary[test.get_name().lower()] = new_test.summary
        # Generate the test-specific webpage 
        new_test.generate()
        print("")

# Create the site index
verification_summary = dict(verification_summary)
performance_summary = dict(performance_summary)
validation_summary = dict(validation_summary)
print("Generating web pages in " + util.variables.output_dir + "....")
util.websetup.generate(verification_summary, performance_summary, validation_summary)

print("Cleaning up....")
util.cleanup.clean()

###############################################################################
#                        Finished.  Tell user about it.                       #
###############################################################################
print("------------------------------------------------------------------------------")
print("Finished running LIVV.  Results:  ")
print("  Open " + util.variables.output_dir + "/index.html to see test results")
print("------------------------------------------------------------------------------")


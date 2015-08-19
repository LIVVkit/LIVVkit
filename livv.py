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
print("                          __   _____   ___   ____    _ __     ") 
print("                         / /  /  _/ | / / | / / /__ (_) /_    ") 
print("                        / /___/ / | |/ /| |/ /  '_// / __/    ") 
print("                       /____/___/ |___/ |___/_/\_\/_/\__/     ")
print("")
print("                       Land Ice Verification & Validation     ")
print("------------------------------------------------------------------------------")
print("  Load modules: python, ncl, nco, python_matplotlib, hdf5, netcdf,")
print("                python_numpy, and python_netcdf4 for best results.\n")

import os
import sys
import time
import getpass
import platform
import socket
import multiprocessing

import argparse

###############################################################################
#                                  Options                                    #
###############################################################################

parser = argparse.ArgumentParser(description="Main script to run LIVV.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        fromfile_prefix_chars='@')

# location of this file
livv_loc = os.path.abspath(__file__)

parser.add_argument('-b', '--bench-dir', 
        default="reg_bench" + os.sep + "linux-gnu",
        help='Location of the input for running verification.')
parser.add_argument('-t', '--test-dir', 
        default="reg_test" + os.sep + "linux-gnu",
        help='Location of the input for running verification.')
parser.add_argument('-o', '--out-dir', 
        default="www",
        help='Location to output the LIVV webpages.')

parser.add_argument('-c', '--comment', 
        default='Test run of code.', 
        help="Describe this run. Comment will appear in the output website's footer.")

parser.add_argument('--performance', 
        action='store_true', 
        help='Run the performance tests analysis.')

parser.add_argument('--validation',
        action='store', nargs='*',
        help='Specify the location of the configuration files for validation tests.')

parser.add_argument('--load', 
        help='Load saved options.')
parser.add_argument('--save', 
        help='Save the current options. If no path specification is given, saved options will appear in the configurations directory.')

# Get the options and the arguments
options = parser.parse_args()
# load as saved options file -- command line arguments will override options in file
if options.load:
    newOpts = ['@'+options.load]
    newOpts.extend(sys.argv[1:])
    options = parser.parse_args(newOpts)

# Pull in the LIVV specific modules
import util.dependencies
util.dependencies.check()
import util.variables
import util.configuration_handler
import util.websetup
import verification.ver_utils.self_verification
import verification.scheduler
import performance.dome
import validation.scheduler

###############################################################################
#                              Global Variables                               #
###############################################################################
util.variables.cwd                = os.getcwd()
util.variables.config_dir         = util.variables.cwd + os.sep + "configurations"
util.variables.input_dir          = os.path.abspath(options.test_dir + os.sep + 'higher-order')
util.variables.benchmark_dir      = os.path.abspath(options.bench_dir + os.sep + 'higher-order')
util.variables.output_dir         = os.path.abspath(options.out_dir)
util.variables.img_dir            = util.variables.output_dir + "/imgs"
util.variables.comment            = options.comment
util.variables.timestamp          = time.strftime("%m-%d-%Y %H:%M:%S")
util.variables.user               = getpass.getuser()
util.variables.website_dir        = util.variables.cwd + "/web"
util.variables.template_dir       = util.variables.website_dir + "/templates"
util.variables.index_dir          = util.variables.output_dir
util.variables.verification       = "True" if options.validation is None else "False"
util.variables.performance        = str(options.performance)
util.variables.validation         = options.validation

# A list of the information that should be looked for in the stdout of model output
util.variables.parser_vars = [
              'Dycore Type', 
              'Number of processors',
              'Number of timesteps',
              'Avg iterations to converge'
             ]

# Dycores to try to parse output for
util.variables.dycores = ['glissade'] #["glide", "glissade", "glam", "albany", "bisicles"]

verification_summary = dict()
performance_summary = dict()
validation_summary = dict()

# Check if we are saving the configuration
if options.save:
    print("  Saving options as: " + options.save)
    util.configuration_handler.save(options)

# Print out some information
machine_name = socket.gethostname()
print(os.linesep + "  Current run: " + time.strftime("%m-%d-%Y %H:%M:%S"))
print("  User: " + util.variables.user)
print("  OS Type: " + platform.system() + " " + platform.release())
print("  Machine: " + machine_name)
print("  " + util.variables.comment + os.linesep)

###############################################################################
#                               Run Test Cases                                #
###############################################################################
# Run the verification tests
if util.variables.verification == "True":
    scheduler = verification.scheduler.VerificationScheduler()
    scheduler.setup()
    verification.ver_utils.self_verification.check()
    scheduler.schedule()
    scheduler.run()
    scheduler.cleanup()
    verification_summary = scheduler.summary.copy()
    del scheduler

# Run the performance verification
performance_summary = dict()
if util.variables.performance == "True":
    print("--------------------------------------------------------------------------")
    print("  Beginning performance analysis....")
    print("--------------------------------------------------------------------------")
    for test in performance_tests:
        new_test = test.Test()
        new_test.run()
        performance_summary[test.get_name().lower()] = new_test.summary
        new_test.generate()
        print("")

# Run the validation verification
validation_summary = dict()
if util.variables.validation is not None:
    scheduler = validation.scheduler.ValidationScheduler()
    scheduler.setup()
    scheduler.schedule()
    scheduler.run()
    scheduler.cleanup()
    validation_summary = scheduler.summary.copy()
    del scheduler

# Create the site index
verification_summary = dict(verification_summary)
performance_summary = dict(performance_summary)
validation_summary = dict(validation_summary)
print("Generating web pages in " + util.variables.output_dir + "....")
util.websetup.generate(verification_summary, performance_summary, validation_summary)

###############################################################################
#                        Finished.  Tell user about it.                       #
###############################################################################
print("------------------------------------------------------------------------------")
print("Finished running LIVV.  Results:  ")
print("  Open " + util.variables.output_dir + "/index.html to see test results")
print("------------------------------------------------------------------------------")


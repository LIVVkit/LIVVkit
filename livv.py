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
Executable script to start a verification and validation test suite.  This script
handles options and setting up data storage from the options.  Each of the 
sub-categories (verification, performance, validation, and numerics) are launched
using their respective schedulers found in their subdirectories.

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
import shutil
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

parser.add_argument('--numerics',
        action='store_true',
        help="Run numerics tests.")

parser.add_argument('--load', 
        help='Load saved options.')
parser.add_argument('--save', 
        help='Save the current options. If no path specification is given, saved options will appear in the configurations directory.')

parser.add_argument('--check',
        action='store_true',
        help='Run only the verification self test to check for internal consistency.')


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
import numerics.scheduler
import verification.ver_utils.self_verification
import verification.scheduler
import performance.scheduler
import validation.scheduler

###############################################################################
#                              Global Variables                               #
###############################################################################
util.variables.cwd                = os.getcwd()
util.variables.config_dir         = os.path.join(util.variables.cwd, "configurations")
util.variables.input_dir          = os.path.abspath(options.test_dir + os.sep + 'higher-order')
util.variables.benchmark_dir      = os.path.abspath(options.bench_dir + os.sep + 'higher-order')
util.variables.output_dir         = os.path.abspath(options.out_dir)
util.variables.img_dir            = util.variables.output_dir + "/imgs"
util.variables.comment            = options.comment
util.variables.timestamp          = time.strftime("%m-%d-%Y %H:%M:%S")
util.variables.user               = getpass.getuser()
util.variables.website_dir        = os.path.join(util.variables.cwd, "web")
util.variables.template_dir       = os.path.join(util.variables.website_dir, "templates")
util.variables.index_dir          = util.variables.output_dir
util.variables.numerics           = options.numerics
util.variables.verification       = True if options.validation is None else False
util.variables.performance        = options.performance
util.variables.validation         = options.validation

# A list of the information that should be looked for in the stdout of model output
util.variables.parser_vars = [
              'Dycore Type', 
              'Number of processors',
              'Number of timesteps',
              'Avg iterations to converge'
             ]

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
util.websetup.setup()
numerics_summary, verification_summary = dict(), dict()
validation_summary, performance_summary = dict(), dict()

# Run the verification self test to check internal consistency
if options.check:
    verification.ver_utils.self_verification.check()
    # Remove output as it's just bit4bit plots that get overwitten with each internal test 
    shutil.rmtree(util.variables.output_dir)
    print("------------------------------------------------------------------------------")
    print("Finished checking LIVV for internal consistency.")
    print("------------------------------------------------------------------------------")
    sys.exit()


# Run the numerics tests
if util.variables.numerics:
    scheduler = numerics.scheduler.NumericsScheduler()
    scheduler.setup()
    scheduler.schedule()
    scheduler.run()
    scheduler.cleanup()
    numerics_summary = scheduler.summary.copy()

# Run the verification tests
if util.variables.verification:
    scheduler = verification.scheduler.VerificationScheduler()
    scheduler.setup()
    verification.ver_utils.self_verification.check()
    scheduler.schedule()
    scheduler.run()
    scheduler.cleanup()
    verification_summary = scheduler.summary.copy()

# Run the performance verification
if util.variables.performance:
    scheduler = performance.scheduler.PerformanceScheduler()
    scheduler.setup()
    scheduler.schedule()
    scheduler.run()
    performance_summary = scheduler.summary.copy()

# Run the validation verification
if util.variables.validation is not None:
    scheduler = validation.scheduler.ValidationScheduler()
    scheduler.setup()
    scheduler.schedule()
    scheduler.run()
    scheduler.cleanup()
    validation_summary = scheduler.summary.copy()

# Create the site index
numerics_summary = dict(numerics_summary)
verification_summary = dict(verification_summary)
performance_summary = dict(performance_summary)
validation_summary = dict(validation_summary)
print("Generating web pages in " + util.variables.output_dir + "....")
util.websetup.generate(numerics_summary, verification_summary, performance_summary, validation_summary)

###############################################################################
#                        Finished.  Tell user about it.                       #
###############################################################################
print("------------------------------------------------------------------------------")
print("Finished running LIVV.  Results:  ")
print("  Open " + util.variables.output_dir + "/index.html to see test results")
print("------------------------------------------------------------------------------")


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

import os
import time
import socket
import getpass
import platform
import argparse

import util.variables

"""
Handles the parsing of options for LIVV's command line interface
@authors: arbennett, jhkennedy

Args:
    args: The list of arguments, typically sys.argv[1:]
"""
def parse(args):
    parser = argparse.ArgumentParser(description="Main script to run LIVV.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        fromfile_prefix_chars='@')

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
            help='Save the current options. If no path specification is given,' +\
                 ' saved options will appear in the configurations directory.')
    return parser.parse_args()


def init(options):
    """ Initialize some defaults """
    util.variables.cwd                = os.getcwd()
    util.variables.config_dir         = os.path.join(util.variables.cwd, "configurations")
    util.variables.input_dir          = os.path.abspath(options.test_dir + os.sep + 'higher-order')
    util.variables.benchmark_dir      = os.path.abspath(options.bench_dir + os.sep + 'higher-order')
    util.variables.output_dir         = os.path.abspath(options.out_dir)
    util.variables.img_dir            = util.variables.output_dir + "/imgs"
    util.variables.comment            = options.comment
    util.variables.timestamp          = time.strftime("%m-%d-%Y %H:%M:%S")
    util.variables.user               = getpass.getuser()
    util.variables.machine            = socket.gethostname()
    util.variables.os_type            = platform.system() + " " + platform.release()
    util.variables.website_dir        = os.path.join(util.variables.cwd, "web")
    util.variables.template_dir       = os.path.join(util.variables.website_dir, "templates")
    util.variables.index_dir          = util.variables.output_dir
    util.variables.numerics           = options.numerics
    util.variables.verification       = True if options.validation is None else False
    util.variables.performance        = options.performance
    util.variables.validation         = options.validation


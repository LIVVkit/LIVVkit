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
import importlib

import util.variables

def parse(args):
    """
    Handles the parsing of options for LIVV's command line interface
    
    Args:
        args: The list of arguments, typically sys.argv[1:]
    """
    parser = argparse.ArgumentParser(description="Main script to run LIVV.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        fromfile_prefix_chars='@')

    parser.add_argument('-o', '--out-dir', 
            default="vv_" + time.strftime("%m-%d-%Y"),
            help='Location to output the LIVV webpages.')
    
    parser.add_argument('--run-tests', action='store_true', 
            help="Run unit tests.")

    parser.add_argument('--verification',
            nargs='*',
            action='store',
            default=[],
            help='Specify the locations of the test bundle to verify.')

    parser.add_argument('--validation',
            action='store', 
            nargs='*',            
            default=[],
            help='Specify the location of the configuration files for validation tests.')
   
    return parser.parse_args()


def init(options):
    """ Initialize some defaults """
    util.variables.cwd            = os.getcwd()
    util.variables.config_dir     = os.path.join(util.variables.cwd, "configurations")
    util.variables.output_dir     = os.path.abspath(options.out_dir)
    util.variables.img_dir        = util.variables.output_dir + "/imgs"
    util.variables.run_tests      = options.run_tests
    util.variables.timestamp      = time.strftime("%m-%d-%Y %H:%M:%S")
    util.variables.user           = getpass.getuser()
    util.variables.machine        = socket.gethostname()
    util.variables.os_type        = platform.system() + " " + platform.release()
    util.variables.website_dir    = os.path.join(util.variables.cwd, "resources")
    util.variables.template_dir   = os.path.join(util.variables.website_dir, "templates")
    util.variables.index_dir      = util.variables.output_dir

    # TODO: This is a workaround to handle the case when no --verification or 
    #       --validation options are given.  Need to also fix the way that 
    #       the validation/performance handling is done in the if 
    #       options.validation != [] block.  Things currently seem to work but 
    #       this can definitely be made cleaner -- arbennett 2/21/16 
    util.variables.model_dir = ""
    util.variables.model_config = ""
    util.variables.bench_dir = ""
    util.variables.bench_config = ""
    util.variables.performance_model_config = ""
    util.variables.performance_model_module = ""
    util.variables.validation_model_config = ""
    util.variables.validation_model_module = ""

    available_bundles = os.listdir(os.path.join(util.variables.cwd, "bundles"))
    # rstrip accounts for trailing path separators
    util.variables.model_dir = options.verification[0].rstrip(os.sep)
    util.variables.bench_dir = options.verification[1].rstrip(os.sep)
    util.variables.model_bundle = util.variables.model_dir.split(os.sep)[-1]
    util.variables.bench_bundle = util.variables.bench_dir.split(os.sep)[-1]

    if util.variables.model_bundle in available_bundles:
        util.variables.numerics_model_config = os.sep.join(
             [util.variables.cwd, "bundles", util.variables.model_bundle, "numerics.json"])
        util.variables.numerics_model_module = importlib.import_module(
             ".".join(["bundles", util.variables.model_bundle, "numerics"]))
        
        util.variables.verification_model_config = os.sep.join(
             [util.variables.cwd, "bundles", util.variables.model_bundle, "verification.json"])
        util.variables.verification_model_module = importlib.import_module(
             ".".join(["bundles", util.variables.model_bundle, "verification"]))
    
    if options.validation != []:
        util.variables.performance_model_config = os.sep.join(
             [util.variables.cwd, "bundles", util.variables.model_bundle, "performance.json"])
        util.variables.performance_model_module = importlib.import_module(
             ".".join(["bundles", util.variables.model_bundle, "performance"]))
        
        util.variables.validation_model_config = os.sep.join(
             [util.variables.cwd, "bundles", util.variables.model_bundle, "validation.json"])
        util.variables.validation_model_module = importlib.import_module(
             ".".join(["bundles", util.variables.model_bundle, "validation"]))


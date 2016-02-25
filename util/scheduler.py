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
Provides functions for scheduling the runs of tests.

@author: arbennett
"""
import os
import json
import multiprocessing

import util.variables
import components.numerics 
import components.verification 
import components.performance 
import components.validation 
from util.datastructures import LIVVDict

def run(run_type, module, config_path):
    """
    Collects the analyses cases to be run and launches processes for each of 
    them.

    Args:
        run_type: A string representation of the run type (eg. verification)
        module: The module corresponding to the run.  Must have a run_suite function
        config_path: The path to the configuration file for the bundle
    """
    if not os.path.isfile(config_path):
        return
    with open(config_path, 'r') as f:
        config = json.load(f)
    tests = [t for t in config.keys() if isinstance(config[t], dict)]
    print(" ---------------------------------------------------------------")
    print("   Beginning " + run_type.lower() + " test suite ")
    print(" ---------------------------------------------------------------")
    launch_processes(tests, module, **config)
    print(" ---------------------------------------------------------------")
    print("   " + run_type.capitalize() + " test suite complete ")
    print(" ---------------------------------------------------------------")
    print("")


def launch_processes(tests, run_module, **config):
    """ Helper method to launch processes and synch output """
    manager = multiprocessing.Manager()
    process_handles = [multiprocessing.Process(target=run_module.run_suite, 
                       args=(c, config[c])) for c in tests]
    for p in process_handles:
        p.start()
    for p in process_handles:
        p.join()


def summarize():
    pass


def cleanup():
    pass


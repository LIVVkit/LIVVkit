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

def run(run_type, module, in_file):
    if not os.path.isfile(in_file):
        return
    with open(in_file, 'r') as f:
        config = json.load(f)
    tests = [t for t in config.keys() if isinstance(config[t], dict)]
    tests = [(t,c) for t in tests for c in config[t]["test_cases"]]
    print(" ---------------------------------------------------------------")
    print("   Beginning " + run_type.lower() + " test suite ")
    print(" ---------------------------------------------------------------")
    launch_processes(tests, module.run_suite, **config)
    print(" ---------------------------------------------------------------")
    print("   " + run_type.capitalize() + " test suite complete ")
    print(" ---------------------------------------------------------------")


def launch_processes(test, run_funct, **config):
    """ Helper method to launch processes and synch output """
    manager = multiprocessing.Manager()
    process_handles = [multiprocessing.Process(target=run_funct,args=(t, c, config[t])) 
                       for t,c in test]
    for p in process_handles:
        p.start()
    for p in process_handles:
        p.join()


def cleanup():
    pass


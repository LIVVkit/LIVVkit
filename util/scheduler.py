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

def run_numerics():
    if not os.path.isfile(util.variables.numerics):
        return
    with open(util.variables.numerics, 'r') as f:
        config = json.load(f)
    tests = [t for t in config.keys() if isinstance(config[t], dict)]
    tests = [(t,c) for t in tests for c in config[t]["test_cases"]]
   
    print("   Beginning numerics test suite ")
    print(" -------------------------------------------------------------------")
    launch_processes(tests, components.numerics.run_suite, **config)
    print(" -------------------------------------------------------------------")
    print("   Numerics test suite complete ")



def run_verification():
    if not os.path.isfile(util.variables.verification):
        return
    with open(util.variables.verification, 'r') as f:
        config = json.load(f)
    tests = [t for t in config.keys() if isinstance(config[t], dict)]
    tests = [(t,c) for t in tests for c in config[t]["test_cases"]]
    
    print("   Beginning verification test suite ")
    print(" -------------------------------------------------------------------")
    launch_processes(tests, components.verification.run_suite, **config)
    print(" -------------------------------------------------------------------")
    print("   Verification test suite complete ")


def run_performance():
    if not os.path.isfile(util.variables.performance):
        return
    with open(util.variables.performance, 'r') as f:
        config = json.load(f)
    tests = [t for t in config.keys() if isinstance(config[t], dict)]
    tests = [(t,c) for t in tests for c in config[t]["test_cases"]]
    
    print("   Beginning performance test suite ")
    print(" -------------------------------------------------------------------")
    launch_processes(tests, components.performance.run_suite, **config)
    print(" -------------------------------------------------------------------")
    print("   Performance test suite complete ")



def run_validation():
    if not os.path.isfile(util.variables.validation):
        return
    with open(util.variables.validation, 'r') as f:
        config = json.load(f)
    tests = [t for t in config.keys() if isinstance(config[t], dict)]
    tests = [(t,c) for t in tests for c in config[t]["test_cases"]]
    
    print("   Beginning validation test suite ")
    print(" -------------------------------------------------------------------")
    launch_processes(tests, components.validation.run_suite, **config)
    print(" -------------------------------------------------------------------")
    print("   Validation test suite complete ")



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




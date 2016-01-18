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
Performance Test Base Module.  

@author: arbennett
"""

import os
import util.variables
from util.datastructures import LIVVDict

def run_suite(test, case, config):
    """ Run the full suite of performance tests """
    summary = LIVVDict()
    summary[case] = LIVVDict()
    model_dir = os.path.join(util.variables.model_dir, config['data_dir'], case)
    bench_dir = os.path.join(util.variables.bench_dir, config['data_dir'], case)
    model_cases = []
    bench_cases = []

    for data_dir, cases in zip([model_dir, bench_dir], [model_cases, bench_cases]):
        for root, dirs, files in os.walk(data_dir):
            if not dirs:
                cases.append(root.strip(data_dir).split(os.sep))
   
    model_cases = sorted(model_cases)
    for mcase in model_cases:
        bench_path = (os.path.join(bench_dir, os.sep.join(mcase))
                        if mcase in bench_cases else None)
        model_path = os.path.join(model_dir, os.sep.join(mcase))
        summary[case].nested_assign(mcase, analyze_case(model_path, bench_path, config))
    
    print_summary(test,case,summary) #TODO
    write_summary(test,case,summary) #TODO


def analyze_case(model_dir, bench_dir, config):
    """ Run all of the performance checks on a particular case """
    summary = LIVVDict()
    model_timings = set([])
    bench_timings = set([])
    

def weak_scaling():
    """ Generate weak scaling stats """
    pass


def strong_scaling():
    """ Generate strong scaling stats """
    pass


def generate_timing_stats():
    """
    Parse all of the timing files, and generate some statistics
    about the run.

    Args:
        TODO

    Returns:
        A LIVVDict containing values that have the form [mean, min, max]
    """
    timing_summary = LIVVDict()
    # TODO
    return timing_summary


def parse_gptl_timing(file_path, var_list):
    """
    Read a GPTL timing file and extract some data.

    Args:
        file_path: the path to the GPTL timing file
        var_list: a list of strings to look for in the file

    Returns:
        A LIVVDict containing key-value pairs of the variables
        and the times associated with them
    """
    timing_summary = LIVVDict()
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            for var in var_list:
                for line in f:
                    if var in line:
                        timing_summary[var] = float(line.split()[4])/int(line.split()[2])
    return timing_summary


def parse_cism_timing(file_path):
    """
    Read a CISM timing file and extract the run time

    Args:
        file_path: the path to the CISM timing file
    
    Returns:
        A LIVVDict with one key under "Run Time".  This is
        done to maintain consistency with other methods
    """
    timing_summary = LIVVDict()
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                split = line.split()
                if not split == []:
                    timing_summary["Run Time"] = float(split[1])
                    break
    return timing_summary


def print_summary(test,case,summary):
    """ Show some statistics from the run """
    pass


def write_summary(test,case,summary):
    """ Take the summary and write out a JSON file """
    pass


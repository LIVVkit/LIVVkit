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
import glob
import json
import pprint
import numpy as np

from livvkit.util import functions
from livvkit.util import variables
from livvkit.util import colormaps
from livvkit.util.datastructures import LIVVDict
from livvkit.util.datastructures import ElementHelper

def run_suite(case, config, summary):
    """ Run the full suite of performance tests """
    config["name"] = case
    result = LIVVDict() 
    timing_data = LIVVDict()
    timing_plots = []
    model_dir = os.path.join(variables.model_dir, config['data_dir'], case)
    bench_dir = os.path.join(variables.bench_dir, config['data_dir'], case)
    model_cases = functions.collect_cases(model_dir)
    bench_cases = functions.collect_cases(bench_dir)
    
    for subcase in sorted(model_cases):
        bench_subcases = bench_cases[subcase] if subcase in bench_cases else []
        for mcase in model_cases[subcase]:
            config["case"] = "-".join([subcase, mcase])
            bpath = (os.path.join(bench_dir, subcase, mcase.replace("-", os.sep))
                            if mcase in bench_subcases else None)
            mpath = os.path.join(model_dir, subcase, mcase.replace("-", os.sep))
            timing_data[subcase][mcase] = analyze_case(mpath, bpath, config)
    
    timing_plots.append(weak_scaling(timing_data, config))
    timing_plots.append(strong_scaling(timing_data, config))

    summary = summarize_result(timing_data, summary)
    print_result(case, summary) #TODO
    functions.create_page_from_template("performance.html",
            os.path.join(variables.index_dir, "performance", case+".html"))
    functions.write_json(result, os.path.join(variables.output_dir, "performance"), case+".json")


def analyze_case(model_dir, bench_dir, config):
    """ Run all of the performance checks on a particular case """
    model_timings = set(glob.glob(os.path.join(model_dir, "*" + config["timing_ext"])))
    if bench_dir is not None:
        bench_timings = set(glob.glob(os.path.join(model_dir, "*" + config["timing_ext"])))
    else:
        bench_timings = set()
    if not len(model_timings):
        return dict(model=dict(), bench=dict()) 
    
    model_stats = generate_timing_stats(model_timings, config['timing_vars'])
    bench_stats = generate_timing_stats(bench_timings, config['timing_vars'])
     
    return dict(model=model_stats, bench=bench_stats) 


def weak_scaling(stats, config):
    """ Generate weak scaling stats """
    return ElementHelper.image_element("Weak Scaling", "", "") 


def strong_scaling(stats, config):
    """ Generate strong scaling stats """
    return ElementHelper.image_element("Strong Scaling", "", "")


def generate_timing_stats(file_list, var_list):
    """
    Parse all of the timing files, and generate some statistics
    about the run.

    Args:
        model_dir: Path to the model output
        bench_dir: Path to the benchmark data
        config: A dictionary containing option specifications

    Returns:
        A LIVVDict containing values that have the form: 
            [mean, min, max, mean, diff. from bench mean]
    """
    timing_result = LIVVDict()
    timing_summary = LIVVDict()
    for file in file_list:
        timing_result[file] = parse_gptl(file, var_list)
    for var in var_list:
        var_time = []
        for f, data in timing_result.items():
            if var in data: var_time.append(data[var])
        if len(var_time):
            var_mean = np.mean(var_time)
            var_max  = np.max(var_time)
            var_min  = np.min(var_time)
            timing_summary[var] = {'mean':var_mean, 'max':var_max, 'min':var_min}
    return timing_summary


def parse_gptl(file_path, var_list):
    """
    Read a GPTL timing file and extract some data.

    Args:
        file_path: the path to the GPTL timing file
        var_list: a list of strings to look for in the file

    Returns:
        A LIVVDict containing key-value pairs of the variables
        and the times associated with them
    """
    timing_result = LIVVDict()
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            for var in var_list:
                for line in f:
                    if var in line:
                        timing_result[var] = float(line.split()[4])/int(line.split()[2])
    return timing_result


def print_result(case,result):
    """ Show some statistics from the run """
    pass


def write_result(case,result):
    """ Take the result and write out a JSON file """
    outpath = os.path.join(variables.output_dir, "Performance", case)
    util.functions.mkdir_p(outpath)
    with open(os.path.join(outpath, case+".json"), 'w') as f:
        json.dump(result, f, indent=4)

def summarize_result(result, summary):
    """ Trim out some data to return for the index page """
    # Get the number of bit for bit failures
    # Get the number of config matches
    # Get the number of files parsed
    return summary

def populate_metadata():
    """ Provide some top level information for the summary """
    return {"Type"    : "Summary",
            "Title"   : "Performance",
            "Headers" : []}

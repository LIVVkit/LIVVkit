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
Verification Test Base Module

@author: arbennett
"""
import os
import re
import copy
import glob
import json
import numpy as np
import multiprocessing
from operator import add
from netCDF4 import Dataset
from matplotlib import pyplot
import util.netcdf
import util.variables
from util.datastructures import LIVVDict

def run_suite(case, config, summary):
    """ Run the full suite of verification tests """
    config["name"] = case
    result = LIVVDict()
    summary[case] = util.variables.manager.dict()
    result[case] = LIVVDict()
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
        case_result = analyze_case(model_path, bench_path, config)
        result[case].nested_assign(mcase, case_result)
        summary[case] = summarize_result(case_result, summary[case])
    print_result(case, result) # TODO
    write_result(case, result)

def analyze_case(model_dir, bench_dir, config, plot=True):
    """ Runs all of the verification checks on a particular case """
    bundle = util.variables.verification_model_module
    result = LIVVDict()
    model_configs = set([os.path.basename(f) for f in 
                      glob.glob(os.path.join(model_dir, "*" + config["config_ext"]))])
    model_logs    = set([os.path.basename(f) for f in 
                      glob.glob(os.path.join(model_dir, "*" + config["logfile_ext"]))])
    model_output  = set([os.path.basename(f) for f in 
                      glob.glob(os.path.join(model_dir, "*" + config["output_ext"]))])
    
    if bench_dir is not None:
        bench_configs = set([os.path.basename(f) for f in
                          glob.glob(os.path.join(bench_dir,"*"+config["config_ext"]))])
        bench_logs = set([os.path.basename(f) for f in
                       glob.glob(os.path.join(bench_dir,"*"+config["logfile_ext"]))])
        bench_output = set([os.path.basename(f) for f in 
                         glob.glob(os.path.join(bench_dir,"*"+config["output_ext"]))])
    else:
        bench_configs = bench_logs = bench_output = set()

    outfiles = model_output.intersection(bench_output)
    configs = model_configs.intersection(bench_configs)
    for of in outfiles:
        result["Output data"][of] = bit_for_bit(os.path.join(model_dir, of), 
                                                 os.path.join(bench_dir, of), 
                                                 config, 
                                                 plot)
    for cf in configs:
        result["Configurations"][cf] = diff_configurations(
                                            os.path.join(model_dir,cf),
                                            os.path.join(bench_dir,cf),
                                            bundle, bundle)
    for lf in model_logs:
        result["Output Log"][lf] = bundle.parse_log(os.path.join(model_dir,lf))
    return result


def bit_for_bit(model_path, bench_path, config, plot=True):
    """
    Checks whether the given files have bit for bit solution matches
    on the given variable list.

    Args:
        model_path: absolute path to the model dataset
        bench_path: absolute path to the benchmark dataset
        config: the configuration of the set of analyses
        plot: a boolean of whether or not to generate plots
    
    Returns:
        A LIVVDict formatted as {var : { err_type : amount }} 
    """
    stats = LIVVDict()
    if not (os.path.isfile(bench_path) and os.path.isfile(model_path)):
        return stats
    try:
        model_data = Dataset(model_path, 'r')
        bench_data = Dataset(bench_path, 'r')
    except:
        print("Error opening datasets!")
        return stats
    if not (util.netcdf.has_time(model_data) and util.netcdf.has_time(bench_data)):
        return stats

    for i, var in enumerate(config["bit_for_bit_vars"]):
        if (var in model_data.variables and var in bench_data.variables):
            m_vardata = model_data.variables[var][:]
            b_vardata = bench_data.variables[var][:]
            diff_data = m_vardata - b_vardata
            if diff_data.any():
                stats[var]["Max Error"] = np.amax(np.absolute(diff_data))
                stats[var]["RMS Error"] = np.sqrt(np.sum(np.square(diff_data).flatten())/
                                                  diff_data.size)
            else:
                stats[var]["Max Error"] = stats[var]["RMS Error"] = 0
            if plot and stats[var]["Max Error"] > 0:
                pf = plot_bit_for_bit(config["name"], var, m_vardata, b_vardata,  diff_data)
            else: pf = "N/A"
            stats[var]["Plot"] = pf
    
    model_data.close()
    bench_data.close()
    return stats 


def diff_configurations(model_config, bench_config, model_bundle, bench_bundle):
    """
    Description

    Args:
        model_config: a dictionary with the model configuration data
        bench_config: a dictionary with the benchmark configuration data

    Returns:
        a nested dictionary with the format 
            {section : {variable : (equal, model value, benchmark value) } }
    """
    diff_dict = LIVVDict()
    model_data = model_bundle.parse_config(model_config)
    bench_data = bench_bundle.parse_config(bench_config)
    model_sections= set(model_data.keys())
    bench_sections = set(bench_data.keys())
    all_sections = set(model_sections.union(bench_sections))
    for s in all_sections:
        model_vars = set(model_data[s].keys()) if s in model_sections else set()
        bench_vars = set(bench_data[s].keys()) if s in bench_sections else set()
        all_vars = set(model_vars.union(bench_vars))
        for v in all_vars:
            model_val = model_data[s][v] if s in model_sections and v in model_vars else 'NA'
            bench_val = bench_data[s][v] if s in bench_sections and v in bench_vars else 'NA'
            same = True if model_val == bench_val and model_val != 'NA' else False
            diff_dict[s][v] = (same, model_val, bench_val)
    return diff_dict


def plot_bit_for_bit(case, var_name, model_data, bench_data, diff_data):
    """ Create a bit for bit plot """
    plot_path = os.sep.join([util.variables.output_dir,"plots","bit_for_bit",case])
    util.datastructures.mkdir_p(plot_path)
    pyplot.figure(figsize=(12,3), dpi=80)
    pyplot.clf()
    # Calculate min and max to scale the colorbars
    max = np.amax([np.amax(model_data), np.amax(bench_data)])
    min = np.amin([np.amin(model_data), np.amin(bench_data)])
    
    # Plot the model output
    pyplot.subplot(3,1,1)
    pyplot.xlabel("Model Data")
    pyplot.ylabel(var_name)
    pyplot.imshow(model_data, vmin=min, vmax=max, interpolation='nearest')
    pyplot.colorbar()
    pyplot.tight_layout()

    # Plot the benchmark data
    pyplot.subplot(3,1,2)
    pyplot.xlabel("Benchmark Data")
    pyplot.imshow(bench_data, vmin=min, vmax=max, interpolation='nearest')
    pyplot.colorbar()
    pyplot.tight_layout()

    # Plot the difference
    pyplot.subplot(3,1,3)
    pyplot.xlabel("Difference")
    pyplot.imshow(diff_data, interpolation='nearest')
    pyplot.colorbar()
    pyplot.tight_layout()
    
    pyplot.savefig(os.sep.join([plot_path, case+".png"]))


def validation_configuration(config):
    """ Make sure that the configuration contains all the needed data """
    pass

def print_result(case, result):
    """ Show some statistics from the run """
    pass

def write_result(case, result):
    """ Take the result and write out a JSON file """
    outpath = os.path.join(util.variables.output_dir, "Verification", case)
    util.datastructures.mkdir_p(outpath)
    with open(os.path.join(outpath, case+".json"), 'w') as f:
            json.dump(result, f, indent=4)

def summarize_result(result, summary):
    """ Trim out some data to return for the index page """
    if not "Bit for Bit" in summary:
        summary["Bit for Bit"] = [0,0]
    if not "Configurations" in summary:
        summary["Configurations"] = [0,0]
    if not "Std. Out Files" in summary:
        summary["Std. Out Files"] = 0

    # Get the number of bit for bit failures
    total_count = failure_count = 0
    summary_data = summary["Bit for Bit"]
    for vals in result["Output data"].values():
        for data in vals.values():
            total_count += 1
            if data["Max Error"] != 0:
                failure_count += 1
    summary_data = np.add(summary_data, [failure_count, total_count]) 
    summary["Bit for Bit"] = summary_data

    # Get the number of config matches
    total_count = failure_count = 0
    summary_Data = summary["Configurations"]
    for vals in result["Configurations"].values():
        for each in vals.values():
            total_count += 1
            for any in each.values():
                if not any[0]:
                    failure_count += 1
                    break
    summary_data = np.add(summary_data, [failure_count, total_count]) 
    summary["Configurations"] = summary_data


    # Get the number of files parsed
    summary["Std. Out Files"] += len(result["Output Log"].keys())

    return summary

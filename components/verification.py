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
import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot

from util import netcdf
from util import functions
from util import variables
from util.datastructures import LIVVDict
from util.datastructures import ElementHelper

def run_suite(case, config, summary):
    """ Run the full suite of verification tests """
    config["name"] = case
    model_dir = os.path.join(variables.model_dir, config['data_dir'], case)
    bench_dir = os.path.join(variables.bench_dir, config['data_dir'], case)
    result = LIVVDict()
    case_summary = LIVVDict()
    model_cases = functions.collect_cases(model_dir)
    bench_cases = functions.collect_cases(bench_dir)

    for subcase in sorted(model_cases.keys()):
        bench_subcases = bench_cases[subcase] if subcase in bench_cases else [] 
        result[subcase] = []
        for mcase in model_cases[subcase]:
            #print(subcase + " - " + mcase)
            bpath = (os.path.join(bench_dir, subcase, mcase.replace("-", os.sep)) 
                      if mcase in bench_subcases else "")
            mpath = os.path.join(model_dir, subcase, mcase.replace("-", os.sep))
            case_result = analyze_case(mpath, bpath, config, case)
            result[subcase].append(ElementHelper.section(mcase, case_result))
            case_summary[subcase] = summarize_result(case_result, 
                    case_summary[subcase])
            
    summary[case] = case_summary
    print_summary(case, summary[case])
    functions.create_page_from_template("verification.html", 
            os.path.join(variables.index_dir, "verification", case + ".html"))
    functions.write_json(result, os.path.join(variables.output_dir, "verification"), case+".json")


def analyze_case(model_dir, bench_dir, config, case, plot=True):
    """ Runs all of the verification checks on a particular case """
    bundle = variables.verification_model_module
    model_out = functions.find_file(model_dir, "*"+config["output_ext"])
    bench_out = functions.find_file(bench_dir, "*"+config["output_ext"])
    model_config = functions.find_file(model_dir, "*"+config["config_ext"])
    bench_config = functions.find_file(bench_dir, "*"+config["config_ext"])
    model_log = functions.find_file(model_dir, "*"+config["logfile_ext"])
    bench_log = functions.find_file(bench_dir, "*"+config["logfile_ext"])
    el = [
            bit_for_bit(model_out, bench_out, config, plot),
            diff_configurations(model_config, bench_config, bundle, bundle),
            bundle.parse_log(model_log)
         ]
    return el


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
        A dictionary created by the ElementHelper object corresponding to
        the results of the bit for bit testing
    """
    # Error handling
    if not (os.path.isfile(bench_path) and os.path.isfile(model_path)):
        return ElementHelper.error("Bit for Bit", 
                "File named " + model_path.split(os.sep)[-1] + " has no suitable match!")
    try:
        model_data = Dataset(model_path, 'r')
        bench_data = Dataset(bench_path, 'r')
    except:
        return ElementHelper.error("Bit for Bit", 
                "File named " + model_path.split(os.sep)[-1] + " could not be read!")
    if not (netcdf.has_time(model_data) and netcdf.has_time(bench_data)):
        return ElementHelper.error("Bit for Bit", 
                "File named " + model_path.split(os.sep)[-1] + " could not be read!")

    # Begin bit for bit analysis
    headers = ["Max Error", "RMS Error", "Plot"]
    stats = LIVVDict()
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
            else: 
                pf = "N/A"
            stats[var]["Plot"] = pf
        else:
            stats[var] = {"Max Error": "No Match", "RMS Error": "N/A", "Plot": "N/A"}
    model_data.close()
    bench_data.close()
    return ElementHelper.bit_for_bit("Bit for Bit", headers, stats) 


def diff_configurations(model_config, bench_config, model_bundle, bench_bundle):
    """
    Description

    Args:
        model_config: a dictionary with the model configuration data
        bench_config: a dictionary with the benchmark configuration data

    Returns:
        A dictionary created by the ElementHelper object corresponding to
        the results of the bit for bit testing
    """
    diff_dict = LIVVDict()
    model_data = model_bundle.parse_config(model_config)
    bench_data = bench_bundle.parse_config(bench_config)
    if model_data == {} and bench_data == {}:
        return ElementHelper.error("Configuration Comparison", 
                "Could not open file: " + model_config.split(os.sep)[-1])
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
    return ElementHelper.diff("Configuration Comparison", diff_dict)


def plot_bit_for_bit(case, var_name, model_data, bench_data, diff_data):
    """ Create a bit for bit plot """
    plot_path = os.sep.join([variables.output_dir, "Verification", case])
    functions.mkdir_p(plot_path)
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


def print_summary(case, summary):
    """ Show some statistics from the run """
    for dof, data in summary.items():
        b4b = data["Bit for Bit"]
        conf = data["Configurations"]
        stdout = data["Std. Out Files"]
        print("    " + case + " " + str(dof))
        print("    --------------------")
        print("     Bit for bit matches   : " + str(b4b[0]) + " of " + str(b4b[1]))
        print("     Configuration matches : " + str(conf[0])+ " of " + str(conf[1]))
        print("     Std. Out files parsed : " + str(stdout))
        print("")


def summarize_result(result, summary):
    """ Trim out some data to return for the index page """
    if "Bit for Bit" not in summary:
        summary["Bit for Bit"] = [0,0]
    if "Configurations" not in summary:
        summary["Configurations"] = [0,0]
    if "Std. Out Files" not in summary:
        summary["Std. Out Files"] = 0

    # Get the number of bit for bit failures
    total_count = failure_count = 0
    summary_data = None
    for elem in result:
        if elem["Type"] == "Bit for Bit" and "Data" in elem:
            elem_data = elem["Data"]
            summary_data = summary["Bit for Bit"]
            total_count += 1
            for var in elem_data.keys():
                if elem_data[var]["Max Error"] != 0:
                    failure_count += 1
                    break
    if summary_data is not None:
        summary_data = np.add(summary_data, [total_count-failure_count, total_count]).tolist() 
        summary["Bit for Bit"] = summary_data

    # Get the number of config matches
    summary_data = None
    total_count = success_count = 0
    for elem in result:
        if elem["Title"] == "Configuration Comparison" and elem["Type"] == "Diff":
            elem_data = elem["Data"]
            summary_data = summary["Configurations"]
            total_count += 1
            for section_name, varlist in elem_data.items():
                for var, val in varlist.items():
                    if not val[0]:
                        success_count += 1
                        break
    if summary_data is not None:
        success_count = total_count - success_count
        summary_data = np.add(summary_data, [success_count, total_count]).tolist()
        summary["Configurations"] = summary_data

    # Get the number of files parsed
    for elem in result:
        if elem["Title"] == "Output Log" and elem["Type"] == "Table":
            summary["Std. Out Files"] += 1
            break
    return summary


def populate_metadata():
    """ Provide some top level information for the summary """
    metadata = {}
    metadata["Type"] = "Summary"
    metadata["Title"] = "Verification"
    metadata["Headers"] = ["Bit for Bit", "Configurations", "Std. Out Files"]
    return metadata


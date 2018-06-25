# coding=utf-8
# Copyright (c) 2015-2018, UT-BATTELLE, LLC
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
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import six

import os

import numpy as np
import matplotlib.pyplot as plt

from netCDF4 import Dataset

import livvkit
from livvkit.util import netcdf
from livvkit.util import functions
from livvkit.util import colormaps
from livvkit.util.LIVVDict import LIVVDict
from livvkit.util import elements


def run_suite(case, config, summary):
    """ Run the full suite of verification tests """
    config["name"] = case
    model_dir = os.path.join(livvkit.model_dir, config['data_dir'], case)
    bench_dir = os.path.join(livvkit.bench_dir, config['data_dir'], case)
    tabs = []
    case_summary = LIVVDict()
    model_cases = functions.collect_cases(model_dir)
    bench_cases = functions.collect_cases(bench_dir)

    for subcase in sorted(six.iterkeys(model_cases)):
        bench_subcases = bench_cases[subcase] if subcase in bench_cases else []
        case_sections = []
        for mcase in sorted(model_cases[subcase], key=functions.sort_processor_counts):
            bpath = (os.path.join(bench_dir, subcase, mcase.replace("-", os.path.sep))
                     if mcase in bench_subcases else "")
            mpath = os.path.join(model_dir, subcase, mcase.replace("-", os.path.sep))
            case_result = _analyze_case(mpath, bpath, config)
            case_sections.append(elements.section(mcase, case_result))
            case_summary[subcase] = _summarize_result(case_result,
                                                      case_summary[subcase])
        tabs.append(elements.tab(subcase, section_list=case_sections))

    result = elements.page(case, config["description"], tab_list=tabs)
    summary[case] = case_summary
    _print_summary(case, summary[case])
    functions.create_page_from_template("verification.html",
                                        os.path.join(livvkit.index_dir,
                                                     "verification",
                                                     case + ".html")
                                        )
    functions.write_json(result, os.path.join(livvkit.output_dir, "verification"), case+".json")


def _analyze_case(model_dir, bench_dir, config):
    """ Runs all of the verification checks on a particular case """
    bundle = livvkit.verification_model_module
    model_out = functions.find_file(model_dir, "*"+config["output_ext"])
    bench_out = functions.find_file(bench_dir, "*"+config["output_ext"])
    model_config = functions.find_file(model_dir, "*"+config["config_ext"])
    bench_config = functions.find_file(bench_dir, "*"+config["config_ext"])
    model_log = functions.find_file(model_dir, "*"+config["logfile_ext"])
    el = [
            bit_for_bit(model_out, bench_out, config),
            diff_configurations(model_config, bench_config, bundle, bundle),
            bundle.parse_log(model_log)
         ]
    return el


def _print_summary(case, summary):
    """ Show some statistics from the run """
    for dof, data in summary.items():
        b4b = data["Bit for Bit"]
        conf = data["Configurations"]
        stdout = data["Std. Out Files"]
        print("    " + case + " " + str(dof))
        print("    --------------------")
        print("     Bit for bit matches   : " + str(b4b[0]) + " of " + str(b4b[1]))
        print("     Configuration matches : " + str(conf[0]) + " of " + str(conf[1]))
        print("     Std. Out files parsed : " + str(stdout))
        print("")


def _summarize_result(result, summary):
    """ Trim out some data to return for the index page """
    if "Bit for Bit" not in summary:
        summary["Bit for Bit"] = [0, 0]
    if "Configurations" not in summary:
        summary["Configurations"] = [0, 0]
    if "Std. Out Files" not in summary:
        summary["Std. Out Files"] = 0

    # Get the number of bit for bit failures
    total_count = 0
    failure_count = 0
    summary_data = None
    for elem in result:
        if elem["Type"] == "Bit for Bit" and "Data" in elem:
            elem_data = elem["Data"]
            summary_data = summary["Bit for Bit"]
            total_count += 1
            for var in six.iterkeys(elem_data):
                if elem_data[var]["Max Error"] != 0:
                    failure_count += 1
                    break
    if summary_data is not None:
        summary_data = np.add(summary_data, [total_count-failure_count, total_count]).tolist()
        summary["Bit for Bit"] = summary_data

    # Get the number of config matches
    summary_data = None
    total_count = 0
    failure_count = 0
    for elem in result:
        if elem["Title"] == "Configuration Comparison" and elem["Type"] == "Diff":
            elem_data = elem["Data"]
            summary_data = summary["Configurations"]
            total_count += 1
            failed = False
            for section_name, varlist in elem_data.items():
                for var, val in varlist.items():
                    if not val[0]:
                        failed = True
            if failed:
                failure_count += 1
    if summary_data is not None:
        success_count = total_count - failure_count
        summary_data = np.add(summary_data, [success_count, total_count]).tolist()
        summary["Configurations"] = summary_data

    # Get the number of files parsed
    for elem in result:
        if elem["Title"] == "Output Log" and elem["Type"] == "Table":
            summary["Std. Out Files"] += 1
            break
    return summary


# noinspection PyUnusedLocal
def populate_metadata(case, config):
    """ Provide some top level information for the summary """
    return {"Type": "Summary",
            "Title": "Verification",
            "Headers": ["Bit for Bit", "Configurations", "Std. Out Files"]}


def bit_for_bit(model_path, bench_path, config):
    """
    Checks whether the given files have bit for bit solution matches
    on the given variable list.

    Args:
        model_path: absolute path to the model dataset
        bench_path: absolute path to the benchmark dataset
        config: the configuration of the set of analyses

    Returns:
        A dictionary created by the elements object corresponding to
        the results of the bit for bit testing
    """
    fname = model_path.split(os.path.sep)[-1]
    # Error handling
    if not (os.path.isfile(bench_path) and os.path.isfile(model_path)):
        return elements.error("Bit for Bit",
                              "File named " + fname + " has no suitable match!")
    try:
        model_data = Dataset(model_path)
        bench_data = Dataset(bench_path)
    except (FileNotFoundError, PermissionError):
        return elements.error("Bit for Bit",
                              "File named " + fname + " could not be read!")
    if not (netcdf.has_time(model_data) and netcdf.has_time(bench_data)):
        return elements.error("Bit for Bit",
                              "File named " + fname + " could not be read!")

    # Begin bit for bit analysis
    headers = ["Max Error", "Index of Max Error", "RMS Error", "Plot"]
    stats = LIVVDict()
    for i, var in enumerate(config["bit_for_bit_vars"]):
        if var in model_data.variables and var in bench_data.variables:
            m_vardata = model_data.variables[var][:]
            b_vardata = bench_data.variables[var][:]
            diff_data = m_vardata - b_vardata
            if diff_data.any():
                stats[var]["Max Error"] = np.amax(np.absolute(diff_data))
                stats[var]["Index of Max Error"] = str(
                        np.unravel_index(np.absolute(diff_data).argmax(), diff_data.shape))
                stats[var]["RMS Error"] = np.sqrt(np.sum(np.square(diff_data).flatten()) /
                                                  diff_data.size)
                pf = plot_bit_for_bit(fname, var, m_vardata, b_vardata, diff_data)
            else:
                stats[var]["Max Error"] = stats[var]["RMS Error"] = 0
                pf = stats[var]["Index of Max Error"] = "N/A"
            stats[var]["Plot"] = pf
        else:
            stats[var] = {"Max Error": "No Match", "RMS Error": "N/A", "Plot": "N/A"}
    model_data.close()
    bench_data.close()
    return elements.bit_for_bit("Bit for Bit", headers, stats)


def diff_configurations(model_config, bench_config, model_bundle, bench_bundle):
    """
    Description

    Args:
        model_config: a dictionary with the model configuration data
        bench_config: a dictionary with the benchmark configuration data
        model_bundle: a LIVVkit model bundle object
        bench_bundle: a LIVVkit model bundle object

    Returns:
        A dictionary created by the elements object corresponding to
        the results of the bit for bit testing
    """
    diff_dict = LIVVDict()
    model_data = model_bundle.parse_config(model_config)
    bench_data = bench_bundle.parse_config(bench_config)
    if model_data == {} and bench_data == {}:
        return elements.error("Configuration Comparison",
                              "Could not open file: " + model_config.split(os.path.sep)[-1])

    model_sections = set(six.iterkeys(model_data))
    bench_sections = set(six.iterkeys(bench_data))
    all_sections = set(model_sections.union(bench_sections))

    for s in all_sections:
        model_vars = set(six.iterkeys(model_data[s])) if s in model_sections else set()
        bench_vars = set(six.iterkeys(bench_data[s])) if s in bench_sections else set()
        all_vars = set(model_vars.union(bench_vars))
        for v in all_vars:
            model_val = model_data[s][v] if s in model_sections and v in model_vars else 'NA'
            bench_val = bench_data[s][v] if s in bench_sections and v in bench_vars else 'NA'
            same = True if model_val == bench_val and model_val != 'NA' else False
            diff_dict[s][v] = (same, model_val, bench_val)
    return elements.file_diff("Configuration Comparison", diff_dict)


def plot_bit_for_bit(case, var_name, model_data, bench_data, diff_data):
    """ Create a bit for bit plot """
    plot_title = ""
    plot_name = case + "_" + var_name + ".png"
    plot_path = os.path.join(os.path.join(livvkit.output_dir, "verification", "imgs"))
    functions.mkdir_p(plot_path)
    m_ndim = np.ndim(model_data)
    b_ndim = np.ndim(bench_data)
    if m_ndim != b_ndim:
        return "Dataset dimensions didn't match!"
    if m_ndim == 3:
        model_data = model_data[-1]
        bench_data = bench_data[-1]
        diff_data = diff_data[-1]
        plot_title = "Showing "+var_name+"[-1,:,:]"
    elif m_ndim == 4:
        model_data = model_data[-1][0]
        bench_data = bench_data[-1][0]
        diff_data = diff_data[-1][0]
        plot_title = "Showing "+var_name+"[-1,0,:,:]"
    plt.figure(figsize=(12, 3), dpi=80)
    plt.clf()

    # Calculate min and max to scale the colorbars
    _max = np.amax([np.amax(model_data), np.amax(bench_data)])
    _min = np.amin([np.amin(model_data), np.amin(bench_data)])

    # Plot the model output
    plt.subplot(1, 3, 1)
    plt.xlabel("Model Data")
    plt.ylabel(var_name)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(model_data, vmin=_min, vmax=_max, interpolation='nearest', cmap=colormaps.viridis)
    plt.colorbar()

    # Plot the benchmark data
    plt.subplot(1, 3, 2)
    plt.xlabel("Benchmark Data")
    plt.xticks([])
    plt.yticks([])
    plt.imshow(bench_data, vmin=_min, vmax=_max, interpolation='nearest', cmap=colormaps.viridis)
    plt.colorbar()

    # Plot the difference
    plt.subplot(1, 3, 3)
    plt.xlabel("Difference")
    plt.xticks([])
    plt.yticks([])
    plt.imshow(diff_data, interpolation='nearest', cmap=colormaps.viridis)
    plt.colorbar()

    plt.tight_layout(rect=(0, 0, 0.95, 0.9))
    plt.suptitle(plot_title)

    plot_file = os.path.sep.join([plot_path, plot_name])
    if livvkit.publish:
        plt.savefig(os.path.splitext(plot_file)[0]+'.eps', dpi=600)
    plt.savefig(plot_file)
    plt.close()
    return os.path.join(os.path.relpath(plot_path,
                                        os.path.join(livvkit.output_dir, "verification")),
                        plot_name)

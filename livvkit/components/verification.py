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

import os

import numpy as np
import matplotlib.pyplot as plt

from netCDF4 import Dataset

import livvkit
from livvkit import elements
from livvkit.util import functions
from livvkit.util import colormaps
from livvkit.util.LIVVDict import LIVVDict


def run_suite(case, config):
    """ Run the full suite of verification tests """
    config["name"] = case
    model_dir = os.path.join(livvkit.model_dir, config['data_dir'], case)
    bench_dir = os.path.join(livvkit.bench_dir, config['data_dir'], case)
    tabs = {}
    summary = LIVVDict()
    model_cases = functions.collect_cases(model_dir)
    bench_cases = functions.collect_cases(bench_dir)

    for subcase in sorted(model_cases):
        bench_subcases = bench_cases[subcase] if subcase in bench_cases else []
        case_sections = []
        try:
            _mcases = sorted(model_cases[subcase], key=functions.sort_processor_counts)
        except ValueError:
            _mcases = sorted(model_cases[subcase])

        for mcase in _mcases:
            if "setup_mesh" in mcase:
                continue
            bpath = (os.path.join(bench_dir, subcase, mcase.replace("-", os.path.sep))
                     if mcase in bench_subcases else "")
            mpath = os.path.join(model_dir, subcase, mcase.replace("-", os.path.sep))
            case_result = _analyze_case(mpath, bpath, config)
            case_sections.append(elements.Section(mcase, case_result))
            summary[subcase] = _summarize_result(case_result, summary[subcase])
        tabs[subcase] = case_sections

    result = elements.Page(case, config["description"], elements=[elements.Tabs(tabs)])

    _print_summary(case, summary)

    functions.create_page_from_template(
        "verification.html", os.path.join(livvkit.index_dir, "verification", case + ".html")
    )
    with open(os.path.join(livvkit.output_dir, "verification", case+".json"), 'w') as f:
        f.write(result._repr_json())

    return summary


def _analyze_case(test_dir, ref_dir, config):
    """ Runs all of the verification checks on a particular case """
    bundle = livvkit.verification_model_module
    test_out = functions.find_file(test_dir, "*"+config["output_ext"])
    ref_out = functions.find_file(ref_dir, "*"+config["output_ext"])
    test_config = functions.find_file(test_dir, "*"+config["config_ext"])
    ref_config = functions.find_file(ref_dir, "*"+config["config_ext"])
    model_log = functions.find_file(test_dir, "*"+config["logfile_ext"])
    ref_log = functions.find_file(ref_dir, "*"+config["logfile_ext"])
    try:
        el = [
                bit_for_bit(test_out, ref_out, config, bundle),
                elements.FileDiff("Configuration Comparison",
                                ref_config, test_config),
            bundle.parse_log(ref_log, title="Benchmark Output Log"),
            bundle.parse_log(model_log, title="Model Output Log"),
        ]
    except (FileNotFoundError, IndexError):
        el = []
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
        if isinstance(elem, elements.BitForBit):
            elem_data = elem.data
            summary_data = summary["Bit for Bit"]
            total_count += 1
            for ii, var in enumerate(elem_data['Variable']):
                if elem_data["Max Error"][ii] != 0:
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
        if isinstance(elem, elements.FileDiff) and elem.title == 'Configuration Comparison':
            summary_data = summary["Configurations"]
            total_count += 1
            if elem.diff_status:
                failure_count += 1
            else:
                continue
    if summary_data is not None:
        success_count = total_count - failure_count
        summary_data = np.add(summary_data, [success_count, total_count]).tolist()
        summary["Configurations"] = summary_data

    # Get the number of files parsed
    for elem in result:
        if isinstance(elem, elements.Table) and elem.title == 'Output Log':
            summary["Std. Out Files"] += 1
            break

    return summary


def populate_metadata(case, config):
    """ Provide some top level information for the summary """
    return {"Type": "Summary",
            "Title": "Verification",
            "Headers": ["Bit for Bit", "Configurations", "Std. Out Files"]}


def bit_for_bit(model_path, bench_path, config, bundle=None):
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
    title = "_".join(model_path.split(os.path.sep)[-5:])[:-3]
    # Error handling
    if not (os.path.isfile(bench_path) and os.path.isfile(model_path)):
        return elements.Error("Bit for Bit",
                              "File named " + fname + " has no suitable match!")
    try:
        model_data = Dataset(model_path)
        bench_data = Dataset(bench_path)
    except (FileNotFoundError, PermissionError):
        return elements.Error("Bit for Bit",
                              "File named " + fname + " could not be read!")
    _timevar = config.get("time_var", "time")
    if not (len(model_data.dimensions[_timevar]) > 0 and len(bench_data.dimensions[_timevar]) > 0):
        return elements.Error("Bit for Bit",
                              "File named " + fname + " could not be read!")

    # Begin bit for bit analysis
    plot_elements = []
    table_data = {'Variable': [], 'Max Error': [], 'Index of Max Error': [], 'RMS Error': []}
    for var in config["bit_for_bit_vars"]:
        if var in model_data.variables and var in bench_data.variables:
            table_data['Variable'].append(var)

            m_vardata = model_data.variables[var][:]
            b_vardata = bench_data.variables[var][:]
            diff_data = m_vardata - b_vardata

            if diff_data.any():
                if hasattr(bundle, "plot_bit_for_bit"):
                    # Try to use the bundle's plotting routine first, mainly for MALI
                    _plot = bundle.plot_bit_for_bit
                else:
                    # Default back to the local plotting routine
                    _plot = plot_bit_for_bit

                table_data["Max Error"].append(np.amax(np.absolute(diff_data)))
                table_data["Index of Max Error"].append(str(
                        np.unravel_index(np.absolute(diff_data).argmax(), diff_data.shape)))
                table_data["RMS Error"].append(np.sqrt(np.sum(np.square(diff_data).flatten()) /
                                               diff_data.size))
                plot_elements.append(_plot(title, var, model_data, bench_data, diff_data))
            else:
                table_data["Max Error"].append(0)
                table_data["Index of Max Error"].append("N/A")
                table_data["RMS Error"].append(0)
                plot_elements.append(elements.B4BImage('', '{} is bit-for-bit'.format(var),
                                                       page_path=os.path.join(livvkit.output_dir, "verification")))
        else:
            table_data["Max Error"].append("No Match")
            table_data["Index of Max Error"].append("N/A")
            table_data["RMS Error"].append("N/A")
            plot_elements.append(elements.NAImage('', '{} is not in both test and reference data'.format(var),
                                                  page_path=os.path.join(livvkit.output_dir, "verification")))
    model_data.close()
    bench_data.close()
    return elements.BitForBit("Bit for Bit", table_data, imgs=plot_elements)


def plot_bit_for_bit(case, var_name, model_data, bench_data, diff_data):
    """ Create a bit for bit plot """
    plot_title = ""
    plot_name = case + "_" + var_name + ".png"
    plot_path = os.path.join(os.path.join(livvkit.output_dir, "verification", "imgs"))
    functions.mkdir_p(plot_path)

    # The new MALI bundle needs the full dataset to plot, so that gets passed now
    # here we only need the variable data since no coords are plotted
    model_data = model_data.variables[var_name]
    bench_data = bench_data.variables[var_name]

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
    plt.savefig(plot_file)
    plt.close()

    # NOTE: If you don't include a title, you must include a group for the image
    #       to appear in a lightbox when clicked instead of as it's own page.
    plot_element = elements.Image(
            '', 'Bit for bit differences between test and reference for '
                '{} in {}'.format(var_name, case),
            plot_file, height=50, group='not-b4b'
    )
    return plot_element

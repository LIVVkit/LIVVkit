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
Performance Test Base Module.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import six

import os
import glob
import numpy as np
import matplotlib.pyplot as plt

import livvkit
from livvkit.util import functions
from livvkit.util import colormaps
from livvkit.util.LIVVDict import LIVVDict
from livvkit.util import elements

SEC_PER_DAY = 86400.0


def run_suite(case, config, summary):
    """ Run the full suite of performance tests """
    config["name"] = case
    timing_data = dict()
    model_dir = os.path.join(livvkit.model_dir, config['data_dir'], case)
    bench_dir = os.path.join(livvkit.bench_dir, config['data_dir'], case)
    plot_dir = os.path.join(livvkit.output_dir, "performance", "imgs")
    model_cases = functions.collect_cases(model_dir)
    bench_cases = functions.collect_cases(bench_dir)
    functions.mkdir_p(plot_dir)

    # Generate all of the timing data
    for subcase in sorted(model_cases):
        bench_subcases = bench_cases[subcase] if subcase in bench_cases else []
        timing_data[subcase] = dict()
        for mcase in model_cases[subcase]:
            config["case"] = "-".join([subcase, mcase])
            bpath = (os.path.join(bench_dir, subcase, mcase.replace("-", os.path.sep))
                     if mcase in bench_subcases else None)
            mpath = os.path.join(model_dir, subcase, mcase.replace("-", os.path.sep))
            timing_data[subcase][mcase] = _analyze_case(mpath, bpath, config)

    # Create scaling and timing breakdown plots
    weak_data = weak_scaling(timing_data, config['scaling_var'],
                             config['weak_scaling_points'])
    strong_data = strong_scaling(timing_data, config['scaling_var'],
                                 config['strong_scaling_points'])

    timing_plots = [
        generate_scaling_plot(weak_data,
                              "Weak scaling for " + case.capitalize(),
                              "runtime (s)", "",
                              os.path.join(plot_dir, case + "_weak_scaling.png")
                              ),
        weak_scaling_efficiency_plot(weak_data,
                                     "Weak scaling efficiency for " + case.capitalize(),
                                     "Parallel efficiency (% of linear)", "",
                                     os.path.join(plot_dir, case + "_weak_scaling_efficiency.png")
                                     ),
        generate_scaling_plot(strong_data,
                              "Strong scaling for " + case.capitalize(),
                              "Runtime (s)", "",
                              os.path.join(plot_dir, case + "_strong_scaling.png")
                              ),
        strong_scaling_efficiency_plot(strong_data,
                                       "Strong scaling efficiency for " + case.capitalize(),
                                       "Parallel efficiency (% of linear)", "",
                                       os.path.join(plot_dir,
                                                    case + "_strong_scaling_efficiency.png")
                                       ),
        ]

    timing_plots = timing_plots + \
        [generate_timing_breakdown_plot(timing_data[s],
                                        config['scaling_var'],
                                        "Timing breakdown for " + case.capitalize()+" "+s,
                                        "",
                                        os.path.join(plot_dir, case+"_"+s+"_timing_breakdown.png")
                                        )
         for s in sorted(six.iterkeys(timing_data), key=functions.sort_scale)]

    # Build an image gallery and write the results
    el = [
            elements.gallery("Performance Plots", timing_plots)
         ]
    result = elements.page(case, config["description"], element_list=el)
    summary[case] = _summarize_result(timing_data, config)
    _print_result(case, summary)
    functions.create_page_from_template("performance.html",
                                        os.path.join(livvkit.index_dir, "performance",
                                                     case + ".html"))
    functions.write_json(result, os.path.join(livvkit.output_dir, "performance"),
                         case + ".json")


def _analyze_case(model_dir, bench_dir, config):
    """ Generates statistics from the timing summaries """
    model_timings = set(glob.glob(os.path.join(model_dir, "*" + config["timing_ext"])))
    if bench_dir is not None:
        bench_timings = set(glob.glob(os.path.join(bench_dir, "*" + config["timing_ext"])))
    else:
        bench_timings = set()
    if not len(model_timings):
        return dict()
    model_stats = generate_timing_stats(model_timings, config['timing_vars'])
    bench_stats = generate_timing_stats(bench_timings, config['timing_vars'])
    return dict(model=model_stats, bench=bench_stats)


# noinspection PyUnusedLocal
def _print_result(case, summary):
    """ Show some statistics from the run """
    for case, case_data in summary.items():
        for dof, data in case_data.items():
            print("    " + case + " " + dof)
            print("    -------------------")
            for header, val in data.items():
                print("    " + header + " : " + str(val))
            print("")


def _summarize_result(result, config):
    """ Trim out some data to return for the index page """
    timing_var = config['scaling_var']
    summary = LIVVDict()
    for size, res in result.items():
        proc_counts = []
        bench_times = []
        model_times = []
        for proc, data in res.items():
            proc_counts.append(int(proc[1:]))
            try:
                bench_times.append(data['bench'][timing_var]['mean'])
            except KeyError:
                pass
            try:
                model_times.append(data['model'][timing_var]['mean'])
            except KeyError:
                pass
        if model_times != [] and bench_times != []:
            time_diff = np.mean(model_times)/np.mean(bench_times)
        else:
            time_diff = 'NA'
        summary[size]['Proc. Counts'] = ", ".join([str(x) for x in sorted(proc_counts)])
        summary[size]['Mean Time Diff (% of benchmark)'] = time_diff
    return summary


# noinspection PyUnusedLocal
def populate_metadata(case, config):
    """ Provide some top level information for the summary """
    return {"Type": "Summary",
            "Title": "Performance",
            "Headers": ["Proc. Counts", "Mean Time Diff (% of benchmark)"]}


def generate_timing_stats(file_list, var_list):
    """
    Parse all of the timing files, and generate some statistics
    about the run.

    Args:
        file_list: A list of timing files to parse
        var_list: A list of variables to look for in the timing file

    Returns:
        A dict containing values that have the form:
            [mean, min, max, mean, standard deviation]
    """
    timing_result = dict()
    timing_summary = dict()
    for file in file_list:
        timing_result[file] = functions.parse_gptl(file, var_list)
    for var in var_list:
        var_time = []
        for f, data in timing_result.items():
            try:
                var_time.append(data[var])
            except:
                continue
        if len(var_time):
            timing_summary[var] = {'mean': np.mean(var_time),
                                   'max': np.max(var_time),
                                   'min': np.min(var_time),
                                   'std': np.std(var_time)}
    return timing_summary


def weak_scaling(timing_stats, scaling_var, data_points):
    """
    Generate data for plotting weak scaling.  The data points keep
    a constant amount of work per processor for each data point.

    Args:
        timing_stats: the result of the generate_timing_stats function
        scaling_var: the variable to select from the timing_stats dictionary
                     (can be provided in configurations via the 'scaling_var' key)
        data_points: the list of size and processor counts to use as data
                     (can be provided in configurations via the 'weak_scaling_points' key)

    Returns:
         A dict of the form:
            {'bench' : {'mins' : [], 'means' : [], 'maxs' : []},
             'model' : {'mins' : [], 'means' : [], 'maxs' : []},
             'proc_counts' : []}
    """
    timing_data = dict()
    proc_counts = []
    bench_means = []
    bench_mins = []
    bench_maxs = []
    model_means = []
    model_mins = []
    model_maxs = []
    for point in data_points:
        size = point[0]
        proc = point[1]
        try:
            model_data = timing_stats[size][proc]['model'][scaling_var]
            bench_data = timing_stats[size][proc]['bench'][scaling_var]
        except KeyError:
            continue
        proc_counts.append(proc)
        model_means.append(model_data['mean'])
        model_mins.append(model_data['min'])
        model_maxs.append(model_data['max'])
        bench_means.append(bench_data['mean'])
        bench_mins.append(bench_data['min'])
        bench_maxs.append(bench_data['max'])
    timing_data['bench'] = dict(mins=bench_mins, means=bench_means, maxs=bench_maxs)
    timing_data['model'] = dict(mins=model_mins, means=model_means, maxs=model_maxs)
    timing_data['proc_counts'] = [int(pc[1:]) for pc in proc_counts]
    return timing_data


def strong_scaling(timing_stats, scaling_var, data_points):
    """
    Generate data for plotting strong scaling.  The data points keep
    the problem size the same and varies the number of processors
    used to complete the job.

    Args:
        timing_stats: the result of the generate_timing_stats function
        scaling_var: the variable to select from the timing_stats dictionary
                     (can be provided in configurations via the 'scaling_var' key)
        data_points: the list of size and processor counts to use as data
                     (can be provided in configurations via the 'strong_scaling_points' key)

    Returns:
        A dict of the form:
            {'bench' : {'mins' : [], 'means' : [], 'maxs' : []},
             'model' : {'mins' : [], 'means' : [], 'maxs' : []},
             'proc_counts' : []}
    """
    timing_data = dict()
    proc_counts = []
    bench_means = []
    bench_mins = []
    bench_maxs = []
    model_means = []
    model_mins = []
    model_maxs = []
    for point in data_points:
        size = point[0]
        proc = point[1]
        try:
            model_data = timing_stats[size][proc]['model'][scaling_var]
            bench_data = timing_stats[size][proc]['bench'][scaling_var]
        except KeyError:
            continue
        proc_counts.append(proc)
        model_means.append(model_data['mean'])
        model_mins.append(model_data['min'])
        model_maxs.append(model_data['max'])
        bench_means.append(bench_data['mean'])
        bench_mins.append(bench_data['min'])
        bench_maxs.append(bench_data['max'])
    timing_data['bench'] = dict(mins=bench_mins, means=bench_means, maxs=bench_maxs)
    timing_data['model'] = dict(mins=model_mins, means=model_means, maxs=model_maxs)
    timing_data['proc_counts'] = [int(pc[1:]) for pc in proc_counts]
    return timing_data


def generate_scaling_plot(timing_data, title, ylabel, description, plot_file):
    """
    Generate a scaling plot.

    Args:
        timing_data: data returned from a `*_scaling` method
        title: the title of the plot
        ylabel: the y-axis label of the plot
        description: a description of the plot
        plot_file: the file to write out to

    Returns:
        an image element containing the plot file and metadata
    """
    proc_counts = timing_data['proc_counts']
    if len(proc_counts) > 2:
        plt.figure(figsize=(10, 8), dpi=150)
        plt.title(title)
        plt.xlabel("Number of processors")
        plt.ylabel(ylabel)

        for case, case_color in zip(['bench', 'model'], ['#91bfdb', '#fc8d59']):
            case_data = timing_data[case]
            means = case_data['means']
            mins = case_data['mins']
            maxs = case_data['maxs']
            plt.fill_between(proc_counts, mins, maxs, facecolor=case_color, alpha=0.5)
            plt.plot(proc_counts, means, 'o-', color=case_color, label=case)

        plt.legend(loc='best')
    else:
        plt.figure(figsize=(5, 3))
        plt.axis('off')
        plt.text(0.4, 0.8, "ERROR:")
        plt.text(0.0, 0.6, "Not enough data points to draw scaling plot")
        plt.text(0.0, 0.44, "To generate this data rerun BATS with the")
        plt.text(0.0, 0.36, "performance option enabled.")

    if livvkit.publish:
        plt.savefig(os.path.splitext(plot_file)[0]+'.eps', dpi=600)
    plt.savefig(plot_file)
    plt.close()
    return elements.image(title, description, os.path.basename(plot_file))


def scaling_sypd_plot(timing_data, title, ylabel, description, plot_file):
    for case in ['bench', 'model']:
        case_data = timing_data[case]
        means = np.array(case_data['means'])
        mins = np.array(case_data['mins'])
        maxs = np.array(case_data['maxs'])

        case_data['means'] = 10.0/means * SEC_PER_DAY
        case_data['mins'] = 10.0/mins * SEC_PER_DAY
        case_data['maxs'] = 10.0/maxs * SEC_PER_DAY

        timing_data[case] = case_data

    return generate_scaling_plot(timing_data, title, ylabel, description, plot_file)


def weak_scaling_efficiency_plot(timing_data, title, ylabel, description, plot_file):
    for case in ['bench', 'model']:
        case_data = timing_data[case]
        means = np.array(case_data['means'])
        mins = np.array(case_data['mins'])
        maxs = np.array(case_data['maxs'])

        case_data['means'] = (means[0] / means) * 100
        case_data['mins'] = (mins[0] / mins) * 100
        case_data['maxs'] = (maxs[0] / maxs) * 100

        timing_data[case] = case_data

    return generate_scaling_plot(timing_data, title, ylabel, description, plot_file)


def strong_scaling_efficiency_plot(timing_data, title, ylabel, description, plot_file):
    for case in ['bench', 'model']:
        case_data = timing_data[case]
        means = np.array(case_data['means'])
        mins = np.array(case_data['mins'])
        maxs = np.array(case_data['maxs'])

        case_data['means'] = (means[0] / (np.arange(1, len(means)+1) * means)) * 100
        case_data['mins'] = (mins[0] / (np.arange(1, len(mins)+1) * mins)) * 100
        case_data['maxs'] = (maxs[0] / (np.arange(1, len(maxs)+1) * maxs)) * 100

        timing_data[case] = case_data

    return generate_scaling_plot(timing_data, title, ylabel, description, plot_file)


def generate_timing_breakdown_plot(timing_stats, scaling_var, title, description, plot_file):
    """
    Description

    Args:
        timing_stats: a dictionary of the form
            {proc_count : {model||bench : { var : { stat : val }}}}
        scaling_var: the variable that accounts for the total runtime
        title: the title of the plot
        description: the description of the plot
        plot_file: the file to write the plot out to
    Returns:
        an image element containing the plot file and metadata
    """
    # noinspection PyProtectedMember
    cmap_data = colormaps._viridis_data
    n_subplots = len(six.viewkeys(timing_stats))
    fig, ax = plt.subplots(1, n_subplots+1, figsize=(3*(n_subplots+2), 5))
    for plot_num, p_count in enumerate(
            sorted(six.iterkeys(timing_stats), key=functions.sort_processor_counts)):

        case_data = timing_stats[p_count]
        all_timers = set(six.iterkeys(case_data['model'])) | set(six.iterkeys(case_data['bench']))
        all_timers = sorted(list(all_timers), reverse=True)
        cmap_stride = int(len(cmap_data)/(len(all_timers)+1))
        colors = {all_timers[i]: cmap_data[i*cmap_stride] for i in range(len(all_timers))}

        sub_ax = plt.subplot(1, n_subplots+1, plot_num+1)
        sub_ax.set_title(p_count)
        sub_ax.set_ylabel('Runtime (s)')
        for case, var_data in case_data.items():
            if case == 'bench':
                bar_num = 2
            else:
                bar_num = 1

            offset = 0
            if var_data != {}:
                for var in sorted(six.iterkeys(var_data), reverse=True):
                    if var != scaling_var:
                        plt.bar(bar_num, var_data[var]['mean'], 0.8, bottom=offset,
                                color=colors[var], label=(var if bar_num == 1 else '_none'))
                        offset += var_data[var]['mean']

                plt.bar(bar_num, var_data[scaling_var]['mean']-offset, 0.8, bottom=offset,
                        color=colors[scaling_var], label=(scaling_var if bar_num == 1 else '_none'))

                sub_ax.set_xticks([1.4, 2.4])
                sub_ax.set_xticklabels(('test', 'bench'))

    plt.legend(loc=6, bbox_to_anchor=(1.05, 0.5))
    plt.tight_layout()

    sub_ax = plt.subplot(1, n_subplots+1, n_subplots+1)
    hid_bar = plt.bar(1, 100)
    for group in hid_bar:
            group.set_visible(False)
    sub_ax.set_visible(False)

    if livvkit.publish:
        plt.savefig(os.path.splitext(plot_file)[0]+'.eps', dpi=600)
    plt.savefig(plot_file)
    plt.close()
    return elements.image(title, description, os.path.basename(plot_file))

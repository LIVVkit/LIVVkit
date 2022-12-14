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
Provides CISM_glissade specific verification tools
"""

import os
import numpy as np
import yaml

from configparser import ConfigParser

import livvkit
from livvkit import elements
from livvkit.util import functions
from livvkit.util import colormaps
from livvkit.util.LIVVDict import LIVVDict

import matplotlib.pyplot as plt

def parse_log(file_path):
    """
    Parse a CISM output log and extract some information.

    Args:
        file_path: absolute path to the log file

    Return:
        A dictionary created by the elements object corresponding to
        the results of the bit for bit testing
    """
    if not os.path.isfile(file_path):
        return elements.Error("Output Log", "Could not open file: " + file_path.split(os.sep)[-1])
    if "albany" in file_path:
        times = {
            "Solution time": 0,
            "total iterations": 0
        }
        headers = {"Solution time": "Solution time [s]",
                   "total iterations": "Total iterations [n]"}
        _idx = 2
    else:
        times = {
            "1 total time": 0,
            "halo updates": 0,
            "initialize": 0,
        }
        headers = {"1 total time": "Total time [s]",
                   "halo updates": "Halo updates [s]",
                   "initialize": "Init time [s]"}
        _idx = 3
    with open(file_path) as f:
        # print(file_path)
        for line in f:
            split = line.split()
            for time_cat in times:
                if time_cat in line:
                    try:
                        times[time_cat] += float(split[_idx])
                    except ValueError:
                        pass
    # data = {
    #     "Total Time [s]": [times["1 total time"]],
    #     "Halo updates [s]": [times["halo updates"]],
    #     "Init time [s]": [times["initialize"]],
    # }
    data = {headers[timer]: [times[timer]] for timer in times}
    test_name = file_path.split(os.path.sep)[
        file_path.split(os.path.sep).index("MPAS") + 1
    ]
    return elements.Table("Output Log: {}/.../{}".format(
        test_name, file_path.split(os.sep)[-1]), data
    )


def parse_config(file_path):
    """
    Convert the CISM configuration file to a python dictionary

    Args:
        file_path: absolute path to the configuration file

    Returns:
        A dictionary representation of the given file
    """
    if not os.path.isfile(file_path):
        return {}
    with open(file_path) as _fin:
        cfg = yaml.safe_load(_fin)
    return elements.Table("Configuration", cfg)
    # parser = ConfigParser()
    # parser.read(file_path)
    # # Strip out inline comments
    # for s in parser._sections:
    #     for v in parser._sections[s]:
    #         parser._sections[s][v] = parser._sections[s][v].split("#")[0].strip()
    # return parser._sections



def plot_bit_for_bit(case, var_name, model_dataset, bench_dataset, diff_data):
    """ Create a bit for bit plot """
    # plt.scatter(x_cell[:], y_cell[:], 80, var_slice, marker="h", edgecolors="none")
    plot_title = ""
    plot_name = case + "_" + var_name + ".png"
    plot_path = os.path.join(os.path.join(livvkit.output_dir, "verification", "imgs"))
    functions.mkdir_p(plot_path)
    x_data_m = model_dataset["xCell"][:]
    y_data_m = model_dataset["yCell"][:]

    x_data_b = bench_dataset["xCell"][:]
    y_data_b = bench_dataset["yCell"][:]

    try:
        model_data = model_dataset.variables[var_name][:]
    except KeyError:
        model_data = np.zeros(x_data_m.shape)
    try:
        bench_data = bench_dataset.variables[var_name][:]
    except KeyError:
        bench_data = np.zeros(x_data_b.shape)

    m_ndim = np.ndim(model_data)
    b_ndim = np.ndim(bench_data)
    if m_ndim != b_ndim:
        return "Dataset dimensions didn't match!"
    if m_ndim == 2:
        model_data = model_data[-1]
        bench_data = bench_data[-1]
        diff_data = diff_data[-1]
        plot_title = "Showing "+var_name+"[-1, :]"
    elif m_ndim == 3:
        model_data = model_data[-1, 0]
        bench_data = bench_data[-1, 0]
        diff_data = diff_data[-1, 0]
        plot_title = "Showing "+var_name+"[-1, 0, :]"
    elif m_ndim == 4:
        model_data = model_data[-1][0][0]
        bench_data = bench_data[-1][0][0]
        diff_data = diff_data[-1][0][0]
        plot_title = "Showing "+var_name+"[-1, 0, 0, :]"
    plt.figure(figsize=(12, 3), dpi=120)
    plt.clf()

    # Calculate min and max to scale the colorbars
    _max = np.amax([np.amax(model_data), np.amax(bench_data)])
    _min = np.amin([np.amin(model_data), np.amin(bench_data)])

    data_plot_settings = {
        "marker": "h", "edgecolors": "black", "linewidths": 0.05, "cmap": colormaps.viridis
    }
    # Plot the model output
    plt.subplot(1, 3, 1)
    plt.xlabel("Model Data")
    plt.ylabel(var_name)
    # plt.xticks([])
    # plt.yticks([])
    # plt.imshow(model_data, vmin=_min, vmax=_max, interpolation='nearest', cmap=colormaps.viridis)
    plt.scatter(
        x_data_m, y_data_m, 10, model_data, **data_plot_settings
    )
    plt.colorbar()

    # Plot the benchmark data
    plt.subplot(1, 3, 2)
    plt.xlabel("Benchmark Data")
    # plt.xticks([])
    # plt.yticks([])
    # plt.imshow(bench_data, vmin=_min, vmax=_max, interpolation='nearest', cmap=colormaps.viridis)
    plt.scatter(
        x_data_b, y_data_b, 10, bench_data, **data_plot_settings
    )
    plt.colorbar()

    # Plot the difference
    _abs_max_diff = np.max(np.abs(diff_data)) * 0.90
    if _abs_max_diff == 0:
        _abs_max_diff = 0.01

    plt.subplot(1, 3, 3)
    plt.xlabel("Difference")
    # plt.xticks([])
    # plt.yticks([])
    # plt.imshow(diff_data, interpolation='nearest', cmap=colormaps.viridis)
    plt.scatter(
        x_data_b,
        y_data_b,
        10,
        diff_data,
        marker="h",
        edgecolors="black",
        cmap="RdBu_r",
        vmin=-_abs_max_diff,
        vmax=_abs_max_diff,
        linewidths=0.05
    )
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

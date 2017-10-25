# Copyright (c) 2015-2017, UT-BATTELLE, LLC
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
Analyze the ice sheet coverage.  For more information check documentation for
the run() function.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import subprocess

import livvkit
from livvkit.util import functions
from livvkit.util import elements


def run(name, config):
    """
    Runs the analysis of the coverage of the ice sheet over the land mass.
    Produces both an overall coverage percentage metric and a coverage plot.

    Args:
        name: The name of the test
        config: A dictionary representation of the configuration file
    Returns:
        An elements.page with the list of elements to display
    """
    bench_data = os.path.join(livvkit.__path__[0], config['data_dir'], config['bench_data'])
    model_data = os.path.join(livvkit.__path__[0], config['data_dir'], config['model_data'])

    if not (os.path.exists(model_data) and os.path.exists(bench_data)):
        # Add more handling here -- what do we want to return for failed tests
        print("ERROR: Could not find necessary data to run the coverage validation!")
        print(model_data)
        print(bench_data)
        print("")
        return elements.error("coverage",
                              "Could not find necessary data to run the coverage validation!")

    # Generate the script
    plot_name = "coverage.png"
    output_dir = os.path.join(livvkit.index_dir, 'validation', 'imgs')
    output_path = os.path.join(output_dir, plot_name)
    functions.mkdir_p(output_dir)

    plot_coverage(config['plot_script'], model_data, bench_data, output_path)

    plot_list = [elements.image(plot_name, " ", plot_name)]
    the_page = elements.page('coverage',
                             config['description'],
                             elements.gallery("Plots", plot_list))

    return the_page


def plot_coverage(plot_file, model_data, bench_data, output_file):
    """
    Calls the ncl script to generate the plots for percent ice sheet
    coverage.

    Args:
        plot_file: Location of the ncl script to generate the coverage plot
        model_data: The dataset with the model output
        bench_data: The dataset with the benchmark output
        output_file: The full path of where to write the plot to

    Returns:
        N/A
    """
    ncl_command = ('ncl \'bench = addfile("' + bench_data +
                   '", "r")\' \'model = addfile("' + model_data +
                   '", "r")\' \'plotFile = "' + output_file + '"\' ' + plot_file)

    # Be cautious about running subprocesses
    subprocess.Popen(ncl_command, shell=True, cwd=livvkit.__path__[0],
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # TODO: Put some error checking here

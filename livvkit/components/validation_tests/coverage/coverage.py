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
Analyze the ice sheet coverage.  For more information check documentation for 
the run() function.

@author: arbennett
"""
import os
import numpy as np
import subprocess
from netCDF4 import Dataset

import util.variables
import util.datastructures

def run(name, *args, **kwargs):
    """
    Runs the analysis of the coverage of the ice sheet over the land mass.
    Produces both an overall coverage percentage metric and a coverage plot.

    Required args:
        plot_file:  full path to the ncl script used to plot the data
        model_data: full path to the output from the model data
        bench_data: full path to the output from the benchmark data
    """
    description = kwargs.get('description')
    plot_file = kwargs.get('plot_file')
    bench_data = kwargs.get('bench_data')
    model_data = kwargs.get('model_data')

    if not (os.path.exists(model_data) and os.path.exists(bench_data)):
        # Add more handling here -- what do we want to return for failed tests
        print("ERROR: Could not find necessary data to run the coverage validation!")
        print(model_data)
        print(bench_data)
        print("")
        return

    # Generate the script
    output_dir = os.path.join(util.variables.index_dir, 
                              'Validation', name, 'imgs')
    output_path = os.path.join(output_dir, "coverage.png")
    util.datastructures.mkdir_p(output_dir)
    plot_coverage(plot_file, model_data, bench_data, output_path)


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
        TBD
    """
    ncl_command = ('ncl \'bench = addfile("'+ bench_data +
                   '", "r")\' \'model = addfile("'+ model_data +
                   '", "r")\' \'plotFile = "'+ output_file +'"\' ' + plot_file)

    # Be cautious about running subprocesses
    call = subprocess.Popen(ncl_command, shell=True, 
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdOut, stdErr = call.stdout.read(), call.stderr.read()



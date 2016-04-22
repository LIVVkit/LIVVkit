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
        plot_script:  full path to the ncl script used to plot the data
        model_data: full path to the output from the model data
        bench_data: full path to the output from the benchmark data
    """
    description = kwargs.get('description')
   
    pd = plotData()

    # Get the data out of the config file
    pd.plot_script  = kwargs.get('plot_script')
    pd.gl_data      = kwargs.get('gl_data')
    pd.vel_data     = kwargs.get('vel_data')
    pd.model_dir    = kwargs.get('model_dir')
    pd.model_prefix = kwargs.get('model_prefix')
    pd.model_suffix = kwargs.get('model_suffix')
    pd.model_start  = kwargs.get('model_start')
    pd.model_end    = kwargs.get('model_end')
    

    if not (os.path.exists(pd.gl_data) and os.path.exists(pd.model_dir)):
        # Add more handling here -- what do we want to return for failed tests
        print("ERROR: Could not find necessary data to run the lvargo13 validation!")
        print(pd.gl_data)
        print(pd.model_dir)
        print("")
        return

    # Generate the script
    pd.output_file_base = os.path.join(util.variables.index_dir, 
                           'validation', self.name, 'imgs', 'lvargo13')
    util.datastructures.mkdir_p(pd.output_file_base)
    plot_lvargo13(pd)


def plot_lvargo13(pd):
    """ 
    Calls the ncl script to generate the plots for percent ice sheet 
    coverage.

    Args:
         pd: A plotData class instance that holds all the needed plot data.
    """
    ncl_command = 'ncl \'gl_data = addfile("'+ pd.gl_data +'", "r")\' '  \
                  + '\'vel_data = addfile("'+ pd.vel_data +'", "r")\' '  \
                  + '\'model_prefix = "' \
                  + os.path.join(pd.model_dir, pd.model_prefix) +'"\' '  \
                  + '\'model_suffix = "'+ pd.model_suffix +'"\' '  \
                  + '\'model_start = '+ pd.model_start +'\' '  \
                  + '\'model_end = '+ pd.model_end +'\' '  \
                  + '\'plot_file_base = "'+ pd.output_file_base +'"\' '  \
                  + pd.plot_script

    # Be cautious about running subprocesses
    call = subprocess.Popen(ncl_command, shell=True, 
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdOut, stdErr = call.stdout.read(), call.stderr.read()


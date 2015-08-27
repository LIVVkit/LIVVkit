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

Created on Aug 7, 2015

@author: arbennett
"""

import os
import numpy as np
import subprocess
from netCDF4 import Dataset

from validation.base import AbstractTest
import util.variables

class Test(AbstractTest):

    def run(self, *args, **kwargs):
        """
        Runs the analysis of the coverage of the ice sheet over the land mass.
        Produces both an overall coverage percentage metric and a coverage plot.
    
        Required args:
            plot_script:  full path to the ncl script used to plot the data
            model_data: full path to the output from the model data
            bench_data: full path to the output from the benchmark data
        """
        self.description = kwargs.get('description')
        plot_script = kwargs.get('plot_script')
        
        gl_data = kwargs.get('gl_data')
        vel_data = kwargs.get('vel_data')
        model_dir = kwargs.get('model_dir')
        model_prefix = kwargs.get('model_prefix')
        model_suffix = kwargs.get('model_suffix')
        model_start = kwargs.get('model_start')
        model_end = kwargs.get('model_end')
        

        if not (os.path.exists(gl_data) and os.path.exists(model_dir)):
            # Add more handling here -- what do we want to return for failed tests
            print("ERROR: Could not find necessary data to run the lvargo13 validation!")
            print(gl_data)
            print(model_dir)
            print("")
            return
    
        # Generate the script
        output_file_base = util.variables.index_dir + os.sep + 'validation' + os.sep + self.name + os.sep + 'imgs' + os.sep + 'lvargo13'
        self.plot_lvargo13(plot_script, gl_data, vel_data, model_dir, model_prefix, model_suffix, model_start, model_end, output_file_base)
    
    
    def plot_lvargo13(self, plot_script, gl_data, vel_data, model_dir, model_prefix, model_suffix, model_start, model_end, output_file_base):
        """ 
        Calls the ncl script to generate the plots for percent ice sheet 
        coverage.
    
        Args:
            plot_script: Location of the ncl script to generate the coverage plot
            model_data: The dataset with the model output
            bench_data: The dataset with the benchmark output
            output_file_base: The full path of where to write the plot to
    
        Returns:
            TBD
        """
        ncl_command = 'ncl \'gl_data = addfile("'+ gl_data +'", "r")\' '  \
                           + '\'vel_data = addfile("'+ vel_data +'", "r")\' '  \
                           + '\'model_prefix = "'+ os.path.join(model_dir, model_prefix) +'"\' '     \
                           + '\'model_suffix = "'+ model_suffix +'"\' '     \
                           + '\'model_start = '+ model_start +'\' '       \
                           + '\'model_end = '+ model_end +'\' '           \
                           + '\'plot_file_base = "'+ output_file_base +'"\' '       \
                           + plot_script
    
        # Be cautious about running subprocesses
        call = subprocess.Popen(ncl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdOut, stdErr = call.stdout.read(), call.stderr.read()
    
        #FIXME: Need better error check here!
        #if not os.path.exists(output_file_base):
        #    print("****************************************************************************")
        #    print("*** Error saving "+output_file_base)
        #    print("*** Details of the error follow: ")
        #    print("")
        #    print(stdOut)
        #    print(stdErr)
        #    print("****************************************************************************")    
    
    

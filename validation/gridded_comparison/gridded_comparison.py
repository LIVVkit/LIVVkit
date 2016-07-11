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
A gridded comparison.  For more information check documentation for 
the run() function.

Created on Feb. 5, 2015

@author: arbennett
@author: jhkennedy 
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
        A gridded comparison of somethhing...
        Produces something...
    
        Required args:
        """
        self.description = kwargs.get('description')
        #plot_file = kwargs.get('plot_file')
        #bench_data = kwargs.get('bench_data')
        #model_data = kwargs.get('model_data')
    
        #if not (os.path.exists(model_data) and os.path.exists(bench_data)):
        #    # Add more handling here -- what do we want to return for failed tests
        #    print("ERROR: Could not find necessary data to run the coverage validation!")
        #    print(model_data)
        #    print(bench_data)
        #    print("")
        #    return
    
        # Generate the script
        #output_path = util.variables.index_dir + os.sep + 'validation' + os.sep + self.name + os.sep + 'imgs' + os.sep + 'coverage.png'
        #self.plot_coverage(plot_file, model_data, bench_data, output_path)
    
    
    def plot_coverage(self, plot_file, model_data, bench_data, output_file):
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
        ncl_command = 'ncl \'bench = addfile("'+ bench_data +'", "r")\' \'model = addfile("'+ model_data +'", "r")\' \'plotFile = "'+ output_file +'"\' ' + plot_file
    
        # Be cautious about running subprocesses
        call = subprocess.Popen(ncl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdOut, stdErr = call.stdout.read(), call.stderr.read()
    
        if not os.path.exists(output_file):
            print("****************************************************************************")
            print("*** Error saving "+output_file)
            print("*** Details of the error follow: ")
            print("")
            print(stdOut)
            print(stdErr)
            print("****************************************************************************")    
    
    

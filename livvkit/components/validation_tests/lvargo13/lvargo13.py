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
"""
import os
import numpy as np
import subprocess
from netCDF4 import Dataset

from livvkit.util import functions
from livvkit.util import variables
from livvkit.util.datastructures import ElementHelper 

def run(name, config):
    """
    Runs the analysis of the coverage of the ice sheet over the land mass.
    Produces both an overall coverage percentage metric and a coverage plot.
    
    Args:
        name: The name of the test
        config: A dictionary representation of the configuration file
    Returns:
        A list of elements to 
    """
    description = config['description']
    greenland_data = os.path.join(variables.cwd, config['data_dir'], config['gl_data']) 
    velocity_data = os.path.join(variables.cwd, config['data_dir'], config['vel_data'])
    print(greenland_data)
   
    if not (os.path.exists(greenland_data) and os.path.exists(velocity_data)):
        # Add more handling here -- what do we want to return for failed tests
        return ElementHelper.error("lvargo13", "Could not find necessary data for validation!")


    # Generate the script
    output_file_base = os.path.join(variables.index_dir, 
                           'validation', name, 'imgs', 'lvargo13')
    functions.mkdir_p(output_file_base)
   
    ncl_command = 'ncl \'gl_data = addfile("'+ config['gl_data'] +'", "r")\' '  \
                  + '\'vel_data = addfile("'+ config['vel_data'] +'", "r")\' '  \
                  + '\'model_prefix = "' \
                  + os.path.join(config['model_dir'], config['model_prefix']) +'"\' '  \
                  + '\'model_suffix = "'+ config['model_suffix'] +'"\' '  \
                  + '\'model_start = '+ config['model_start'] +'\' '  \
                  + '\'model_end = '+ config['model_end'] +'\' '  \
                  + '\'plot_file_base = "'+ output_file_base +'"\' ' \
                  + os.path.join(variables.cwd, config['plot_script'])

    # Be cautious about running subprocesses
    call = subprocess.Popen(ncl_command, shell=True, 
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdOut, stdErr = call.stdout.read(), call.stderr.read()



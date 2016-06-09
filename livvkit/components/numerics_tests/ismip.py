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
Utilities to provide numerical verification for the ISMIP test cases
"""

import os
import json
import glob
import numpy
import scipy

import matplotlib.pyplot as plt

from livvkit.util import variables
from livvkit.util.datastructures import ElementHelper

with open(__file__.replace('.py','.json'), 'r') as f:
    setup = json.load(f)

case_color = {'bench': '#d7191c',
              'test':  '#fc8d59' }

line_style = {'bench': 'o-',
              'test':  '-'  }

def get_case_length(case):
        return str(int(case.split('-')[-1][1:])).zfill(3)

def hom(config, analysis_data):
    #FIXME:
    """ 
    Verify ISMIP-HOM model data against ISMIP's datasets 
    
    Args:
        model_path: Absolute path to the model data set
        bench_path: Absolute path to the benchmark data set
        config: A dictionary containing configuration options

    Returns:
        A result of the differences between the model and benchmark
    """
   
    exp = config['name'].split('-')[-1]
    if exp in ['a', 'c']:
        coord = 'x_hat'
    else:
        coord = 'y_hat'

    lengths = list(set(
        [ get_case_length(case) for case in analysis_data.keys() ]
        ))

    plot_list = []
    for p, pattern in enumerate(sorted(setup[exp]['pattern'])):
        fig_label = pattern.split('_')[1]
        description = ''

        for l in sorted(lengths):
            plt.figure(figsize=(10,8), dpi=150)
            plt.rc('text', usetex=True)
            plt.xlabel(setup[exp]['xlabel'][p])
            plt.ylabel(setup[exp]['ylabel'][p])
            
            if exp in ['a','c']:
                plt.title(str(int(l))+' km')
                plot_file = os.path.join( config["plot_dir"], config['name']+'_'+fig_label+'_'+l+'.png' )
                title = fig_label[0:-1]+'. '+fig_label[-1]+': '+str(int(l))+' km'
                recreate_file = os.path.join(
                        variables.cwd, setup[exp]["data_dir"], pattern
                        ).replace('???', l)
            else:
                plt.title('No-Slip Bed')
                plot_file = os.path.join( config["plot_dir"], config['name']+'_'+fig_label+'_000.png' )
                title = fig_label[0:-2]+'. '+fig_label[-2:]+': No-Slip Bed'
                recreate_file = os.path.join(
                        variables.cwd, setup[exp]["data_dir"], pattern
                        ).replace('???', '000')


            axis, fs_amin, fs_amax, fs_mean, ho_amin, ho_amax, ho_mean = \
                numpy.genfromtxt(recreate_file, delimiter=',', missing_values='nan', unpack=True)
            
            plt.fill_between(axis, ho_amin, ho_amax, facecolor='green', alpha=0.5)
            plt.fill_between(axis, fs_amin, fs_amax, facecolor='blue', alpha=0.5)
            
            plt.plot(axis, fs_mean, 'b-', linewidth=2, label='Full stokes')
            plt.plot(axis, ho_mean, 'g-', linewidth=2, label='Higher order')

            
            analysis = {}
            for a in analysis_data.keys():
                if int(l) == int(a.split('-')[-1][1:]):
                    analysis[a] = analysis_data[a]

            for a in analysis.keys():
                for model in sorted(analysis[a].keys()):
                    plt.plot(analysis[a][model][coord], analysis[a][model][config['plot_vars'][p]], 
                                line_style[model], color=case_color[model], linewidth=2, label=a+'-'+model)

            plt.legend(loc='best')
            
            plt.savefig(plot_file)
            plt.close()

            plot_list.append( ElementHelper.image_element(title, description, os.path.basename(plot_file)) )

    
    return plot_list



def populate_metadata():
    """ Provide some top level information for the summary """
    metadata = {}
    metadata["Type"] = "Summary"
    metadata["Title"] = "Numerics"
    metadata["Headers"] = ["Test1", "Test2"]
    return metadata


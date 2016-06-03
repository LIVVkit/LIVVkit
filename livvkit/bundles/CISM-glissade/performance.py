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
CISM-glissade module for performance analysis

@authors: arbennett
"""

import os
import matplotlib
import numpy as np
import pprint

from livvkit.util.datastructures import LIVVDict
from livvkit.util.datastructures import ElementHelper

def weak_scaling(timing_stats, scaling_var):
    """ 
    Generate data for plotting weak scaling.  The data points keep 
    a constant amount of work per processor for each data point.

    Args:
        timing_stats: the result of livvkit.components.performance's 
                      generate_timing_stats function
        scaling_var: the variable to select from the timing_stats dictionary
                     (can be provided in configurations via the 'scaling_var' key)

    Returns:
        TODO : Currently returns a dict with model, 
                 bench, and proc data containing lists
    """
    timing_data = LIVVDict()
    #data_points = [['s0','p1'],['s1','p4'],['s2','p16'],['s3','p64'],['s4','p256']]
    data_points = [['s0','p1'],['s1','p4'],['s2','p16']]
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
        proc_counts.append(proc)
        try:
            model_data = timing_stats[size][proc]['model'][scaling_var]
            bench_data = timing_stats[size][proc]['bench'][scaling_var]
            model_means.append(model_data['mean'])
            model_mins.append(model_data['min'])
            model_maxs.append(model_data['max'])
            bench_means.append(bench_data['mean'])
            bench_mins.append(bench_data['min'])
            bench_maxs.append(bench_data['max'])
        except KeyError:
            pass
    timing_data['bench'] = dict(mins=bench_mins, means=bench_means, maxs=bench_maxs)
    timing_data['model'] = dict(mins=model_mins, means=model_means, maxs=model_maxs)
    timing_data['proc_counts'] = [int(pc[1:]) for pc in proc_counts]
    return timing_data 


def strong_scaling(timing_stats, scaling_var):
    """
    Generate data for plotting strong scaling.  The data points keep
    the problem size the same and varies the number of processors
    used to complete the job.

    Args:
        timing_stats: the result of livvkit.components.performance's
                      generate_timing_stats function
        scaling_var: the variable to select from the timing_stats dictionary
                     (can be provided in configurations via the 'scaling_var' key)

    Returns:
        TODO: A LIVVDict() of the form...
    """
    timing_data = LIVVDict()
    data_points = [['s0', 'p1'],['s0','p2'],['s0','p4'],['s0','p8']]
#    timing_data['proc_counts'] = [1,2,4,8]
#    for case in ['bench', 'model']:
#        means = []
#        mins = []
#        maxs = []
#        for point in data_points:
#            size = point[0]
#            proc = point[1]
#            try:
#                data = timing_stats[size][proc][case][scaling_var]
#                means.append(data['mean'])
#                mins.append(data['min'])
#                maxs.append(data['max'])
#                timing_data[case] = dict(mins=mins, means=means, maxs=maxs)
#            except:
#                pass
#    return timing_data
#
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
        proc_counts.append(proc)
        try:
            model_data = timing_stats[size][proc]['model'][scaling_var]
            bench_data = timing_stats[size][proc]['bench'][scaling_var]
            model_means.append(model_data['mean'])
            model_mins.append(model_data['min'])
            model_maxs.append(model_data['max'])
            bench_means.append(bench_data['mean'])
            bench_mins.append(bench_data['min'])
            bench_maxs.append(bench_data['max'])
        except KeyError:
            pass
    timing_data['bench'] = dict(mins=bench_mins, means=bench_means, maxs=bench_maxs)
    timing_data['model'] = dict(mins=model_mins, means=model_means, maxs=model_maxs)
    timing_data['proc_counts'] = [int(pc[1:]) for pc in proc_counts]
    return timing_data 

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
        # TODO : Currently returns a dict with model, 
                 bench, and proc data containing lists
    """
    timing_data = LIVVDict()
    data_points = [['s0','p1'],['s1','p4'],['s2','p16'],['s3','p64'],['s4','p256']]
    proc_counts = [1, 4, 16, 64, 256]
    for case in ['bench', 'model']:
        means = []
        mins = []
        maxs = []
        for point in data_points:
            size = point[0]
            proc = point[1]
            if timing_stats[size][proc][case][scaling_var] is not None:
                data = timing_stats[size][proc][case][scaling_var]
                means.append(data['mean'])
                mins.append(data['min'])
                maxs.append(data['max'])
                timing_data[case] = dict(mins=mins, means=means, maxs=maxs)
    timing_data['proc_counts'] = proc_counts
    return timing_data 


def strong_scaling(timing_stats):
    """ Description """
    return ElementHelper.image_element("Strong Scaling", "", None)


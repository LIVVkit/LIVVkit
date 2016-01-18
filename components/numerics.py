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
Numerics Test Base Module.  

@author: arbennett
"""

import os
import util.variables
from util.datastructures import LIVVDict

def run_suite(test, case, config):
    """ Run the full suite of numerics tests """
    summary = LIVVDict()
    summary[case] = LIVVDict()
    model_dir = os.path.join(util.variables.model_dir, config['data_dir'], case)
    bench_dir = os.path.join(util.variables.bench_dir, config['data_dir'], case)
    model_cases = []
    bench_cases = []

    for data_dir, cases in zip([model_dir, bench_dir], [model_cases, bench_cases]):
        for root, dirs, files in os.walk(data_dir):
            if not dirs:
                cases.append(root.strip(data_dir).split(os.sep))
   
    model_cases = sorted(model_cases)
    for mcase in model_cases:
        bench_path = (os.path.join(bench_dir, os.sep.join(mcase))
                        if mcase in bench_cases else None)
        model_path = os.path.join(model_dir, os.sep.join(mcase))
        summary[case].nested_assign(mcase, analyze_case(model_path, bench_path, config))
    print_summary(test,case,summary) #TODO
    write_summary(test,case,summary) #TODO


def analyze_case(model_dir, bench_dir, config):
    """ Run all of the numerics checks on a particular case """
    summary = LIVVDict()
    model_timings = set([])
    bench_timings = set([])
    

def ismip(exp_type, resolution):
    """ 
    Verify ISMIP-HOM model data against ISMIP's datasets 
    
    Args:
        exp_type: Which ISMIP experiment to analyze
        resolution: The size of the dataset

    Returns:
        TODO
    """
    ismip_path = os.path.join(util.variables.cwd, "datasets",
            "ismip-hom", exp_type+"."+resolution, ".lmla.txt")
    x, y, vx_u, vx_std, vx_min, vx_max, vy_u, vy_std, vy_min, vy_max = (
        np.loadfromtxt(ismip_path, unpack=True, delimiter=',',
        skiprows=1, usecols=(0,1,2,3,4,5,6,7,8,9)))
    
    n_pts = int(np.sqrt(len(x)))
    vnorm_mean =  np.reshape(np.sqrt(np.add(np.power(vx_mean,2), np.power(vy_mean,2))),\
                             (n_pts,n_pts))
    vnorm_stdev = np.reshape(np.sqrt(np.add(np.power(vx_stdev,2), np.power(vy_stdev,2))),\
                             (n_pts,n_pts))
    vnorm_plus =  np.reshape(np.add(vnorm_mean, vnorm_stdev), (n_pts,n_pts))
    vnorm_minus = np.reshape(np.subtract(vnorm_mean, vnorm_stdev), (n_pts,n_pts))
    vnorm_max = np.reshape(np.sqrt(np.add(np.power(vx_max,2), np.power(vy_max,2))),\
                           (n_pts,n_pts))
    vnorm_min = np.reshape(np.sqrt(np.add(np.power(vx_min,2), np.power(vy_min,2))),\
                           (n_pts,n_pts))
 
    # Grab the model data
    data_files = sorted(set(fn for fn in fnmatch.filter(os.listdir(self.model_dir), \
                            'ismip-hom-' + exp_type + '.'+resolution+'.????.out.nc')))
    for fname in data_files:
        dataset = Dataset(os.path.join(self.model_dir,fname),'r')
        uvel  = dataset.variables['uvel'][0,0,:,:]
        vvel  = dataset.variables['vvel'][0,0,:,:]
        shape = np.shape(uvel)
        vnorm = np.sqrt(np.add(np.power(uvel,2), np.power(vvel,2)))
        floor = np.subtract(vnorm_min[1:-1,1:-1],   vnorm)
        ciel  = np.subtract(vnorm_max[1:-1,1:-1],   vnorm)
        under = np.subtract(vnorm_minus[1:-1,1:-1], vnorm)
        over  = np.subtract(vnorm_plus[1:-1,1:-1],  vnorm)
        bad_data = np.zeros(shape)
        for i in range(shape[0]):
            for j in range(shape[0]):
                if floor[i,j]>0:
                    bad_data[i,j] = -2 # CISM < MIN_ISMIP
                elif ciel[i,j]<0:
                    bad_data[i,j] = 2  # CISM > MAX_ISMIP
                elif under[i,j]>0:
                    bad_data[i,j] = -1 # CISM < MU - SIGMA 
                elif over[i,j]<0:
                    bad_data[i,j] = 1  # CISM > MU + SIGMA
        mean_diff = 100.0*np.divide(np.subtract(vnorm_mean[1:-1,1:-1], vnorm),\
                                                vnorm_mean[1:-1,1:-1])
    
def print_summary(test,case,summary):
    pass

def write_summary(test,case,summary):
    pass


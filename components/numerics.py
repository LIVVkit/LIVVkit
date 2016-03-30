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
import glob
import json
import pprint
import numpy as np
import util.variables
import util.datastructures
from netCDF4 import Dataset

from util.datastructures import LIVVDict

def run_suite(case, config, summary):
    """ Run the full suite of numerics tests """
    result = LIVVDict()
    result[case] = LIVVDict()
    model_dir = os.path.join(util.variables.model_dir, config['data_dir'], case)
    bench_dir = os.path.join(util.variables.cwd, config['bench_dir'], case)
    model_cases = []
    bench_cases = []

    for data_dir, cases in zip([model_dir, bench_dir], [model_cases, bench_cases]):
        for root, dirs, files in os.walk(data_dir):
            if not dirs:
                cases.append(root.strip(data_dir).split(os.sep))
    
    model_cases = sorted(model_cases)
    for mcase in model_cases:
        # Strip last part since benchmarks don't have processor counts
        bench_path = (os.path.join(bench_dir, os.sep.join(mcase[0:-1]))
                if mcase[0:-1] in bench_cases else None)
        model_path = os.path.join(model_dir, os.sep.join(mcase))
        result[case].nested_assign(mcase, analyze_case(mcase, model_path, bench_path, config))
    print_result(case,result) #TODO
    write_result(case,result) #TODO
    summarize_result(case, result, summary)

def analyze_case(case, model_dir, bench_dir, config):
    """ Run all of the numerics checks on a particular case """
    result = LIVVDict()
    str_to_case = {
                "ismip-hom" : ismip
            }
    model_files = list(set([os.path.basename(f) for f in 
                    glob.glob(os.path.join(model_dir, "*" + config["output_ext"]))]))
    if bench_dir is not None:
        bench_files = list(set([os.path.basename(f) for f in glob.glob(
            os.path.join(util.variables.cwd , bench_dir, "*" + config["bench_ext"]))]))
    if len(model_files) > 0 and len(bench_files) > 0:
        result[model_files[0]] = ismip(os.path.join(model_dir,model_files[0]), 
                                        os.path.join(bench_dir,bench_files[0]),
                                        config)
    return result


def ismip(model_path, bench_path, config):
    """ 
    Verify ISMIP-HOM model data against ISMIP's datasets 
    
    Args:
        model_path: Absolute path to the model data set
        bench_path: Absolute path to the benchmark data set
        config: A dictionary containing configuration options

    Returns:
        A result of the differences between the model and benchmark
    """
    result = LIVVDict()
    # Python2 equivalent call: np.loadtxt -> np.loadfromtxt
    x, y, vx_u, vx_std, vx_min, vx_max, vy_u, vy_std, vy_min, vy_max = (
        np.loadtxt(bench_path, unpack=True, delimiter=',',
        skiprows=1, usecols=(0,1,2,3,4,5,6,7,8,9)))
    
    n_pts = int(np.sqrt(len(x)))
    vnorm_mean =  np.reshape(np.sqrt(np.add(np.power(vx_u,2), np.power(vy_u,2))),\
                             (n_pts,n_pts))
    vnorm_stdev = np.reshape(np.sqrt(np.add(np.power(vx_std,2), np.power(vy_std,2))),\
                             (n_pts,n_pts))
    vnorm_plus =  np.reshape(np.add(vnorm_mean, vnorm_stdev), (n_pts,n_pts))
    vnorm_minus = np.reshape(np.subtract(vnorm_mean, vnorm_stdev), (n_pts,n_pts))
    vnorm_max = np.reshape(np.sqrt(np.add(np.power(vx_max,2), np.power(vy_max,2))),\
                           (n_pts,n_pts))
    vnorm_min = np.reshape(np.sqrt(np.add(np.power(vx_min,2), np.power(vy_min,2))),\
                           (n_pts,n_pts))
 
    # Grab the model data
    dataset = Dataset(model_path,'r')
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
    result["Mean % Difference"] = np.nanmean(mean_diff)
    return result
    
def print_result(case,result):
    pass


def write_result(case,result):
    """ Take the result and write out a JSON file """
    outpath = os.path.join(util.variables.output_dir, "Numerics", case)
    util.datastructures.mkdir_p(outpath)
    with open(os.path.join(outpath, case+".json"), 'w') as f:
        json.dump(result, f, indent=4)

def summarize_result(case, result, summary):
    """ Trim out some data to return for the index page """
    # Get the number of bit for bit failures
    # Get the number of config matches
    # Get the number of files parsed

def populate_metadata():
    """ Provide some top level information """
    metadata = {}
    metadata["Format"] = "Summary"
    metadata["Type"] = "Numerics"
    metadata["Headers"] = ["Max Error", "RMSE"]
    return metadata

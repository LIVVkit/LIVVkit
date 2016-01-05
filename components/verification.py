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
Verification Test Base Module

@author: arbennett
"""

import os
import json
import numpy as np
from netCDF4 import Dataset
from configparser import ConfigParser

import util.netcdf
import util.variables
from util.datastructures import LIVVDict


def run_suite(summary, config):
    """ Run the full suite of verification tests """
    pass


def bit_for_bit(model_path, bench_path, var_list):
    """
    Checks whether the given files have bit for bit solution matches
    on the given variable list.

    Args:
        model_path: absolute path to the model dataset
        bench_path: absolute path to the benchmark dataset
        var_list: the list of variables to compare
    
    Returns:
        TODO 
    """
    max_err   = np.zeros(len(var_list))
    rms_err   = np.zeros(len(var_list))
    diff_data = np.zeros(len(var_list))

    if not (os.path.isfile(bench_path) and os.path.isfile(model_path)):
        return

    try:
        model_data = Dataset(model_path, 'r')
        bench_data = Dataset(bench_data, 'r')
    except:
        print("Error opening datasets!")
        raise

    if not (util.netcdf.has_time(model_data) and util.netcdf.has_time(bench_data)):
        return

    for i, var in enumerate(var_list):
        if not (var in model_data.variables and var in bench_data.variables):
            pass
        diff_data[i] = model_data.variables[var] - bench_data.variables[var]
        if diff_data.any():
            max_err[i] = np.amax(np.absolute(diff_data))
            rms_err[i] = np.sqrt(np.sum(np.square(diff_data).flatten()) / diff_data.size)
        
    model_data.close()
    bench_data.close()

    # TODO: Figure out what data to return and which data to dispatch to somewhere else
    return


def diff_configurations(model_config, bench_config):
    """
    Description

    Args:
        model_config: a dictionary with the model configuration data
        bench_config: a dictionary with the benchmark configuration data

    Returns:
        a nested dictionary with the format 
            {section : {variable : (equal, model value, benchmark value) } }
    """
    diff_dict = LIVVDict()
    model_sections= set(model_data.keys())
    bench_sections = set(bench_data.keys())
    all_sections = set(model_sections + bench_sections)
    for s in all_sections:
        model_vars = set(model_data[s].keys()) if s in model_sections else set()
        bench_vars = set(bench_data[s].keys()) if s in bench_sections else set()
        all_vars = set(model_vars + bench_vars)
        for v in all_vars:
            model_val = model_data[s][v] if s in model_sections and v in model_vars else 'NA'
            bench_val = bench_data[s][v] if s in bench_sections and v in bench_vars else 'NA'
            same = True if model_val == bench_val and model_val != 'NA' else False
            diff_dict[s][v] = (same, model_val, bench_val)
    return diff_dict


def parse_cism_config(file_path):
    """
    Convert the CISM configuration file to a python dictionary

    Args:
        file_path: absolute path to the configuration file

    Returns:
        A dictionary representation of the given file
    """
    if not os.path.isfile(file_path):
        return None
    parser = ConfigParser()
    return parser.read(file_path)


def parse_cism_log(file_path):
    """
    Parse a CISM output log and extract some information.

    Args:
        file_path: absolute path to the log file

    Return:
        TODO
    """
    if not os.path.isfile(file_path):
        return
    with open(file_path, 'r') as f:
        dycore_types = {"0" : "Glide", "1" : "Glam", "2" : "Glissade", "3" : "Albany_felix", "4" : "BISICLES"}
        curr_step = 0
        proc_count = 0
        iter_count = 0
        avg_iters_to_converge = 0
        converged_iters = []
        iters_to_converge = []
        for line in f:
            if ('CISM dycore type' in line):
                if line.split()[-1] == '=':
                    self.std_out_data['Dycore Type'] = dycore_types[next(logfile).strip()]
                else:
                    self.std_out_data['Dycore Type'] = dycore_types[line.split()[-1]]
            elif ('total procs' in line):
                number_procs += int(line.split()[-1])
            elif ('Nonlinear Solver Step' in line):
                current_step = int(line.split()[4])
            elif ('Compute ice velocities, time = ' in line):
                current_step = float(line.split()[-1])
            elif ('"SOLVE_STATUS_CONVERGED"' in line):
                split = line.split()
                iters_to_converge.append(int(split[split.index('"SOLVE_STATUS_CONVERGED"') + 2]))
            elif ("Compute dH/dt" in line):
                iters_to_converge.append(int(iter_number))
            elif ('Converged!' in line):
                converged_iters.append(current_step)
            elif ('Failed!' in line):
                converged_iters.append(-1*current_step)
            split = line.split()
            if len(split) > 0 and split[0].isdigit():
                iter_number = split[0]

            



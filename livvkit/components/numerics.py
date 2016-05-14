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
from netCDF4 import Dataset

from livvkit.util import functions
from livvkit.util import variables
from livvkit.util.datastructures import LIVVDict
from livvkit.util.datastructures import ElementHelper
import livvkit.components.numerics_tests.ismip as ismip

def _run_suite(case, config, summary):
    """ Run the full suite of numerics tests """
    config["name"] = case
    result = LIVVDict()
    result[case] = LIVVDict()
    model_dir = os.path.join(variables.model_dir, config['data_dir'], case)
    bench_dir = os.path.join(variables.cwd, config['bench_dir'], case)
    model_cases = functions.collect_cases(model_dir) 
    bench_cases = functions.collect_cases(bench_dir)
    
    for mcase in sorted(model_cases):
        # Strip last part since benchmarks don't have processor counts
        bench_path = (os.path.join(bench_dir, os.sep.join(mcase[0:-1]))
                if mcase[0:-1] in bench_cases else None)
        model_path = os.path.join(model_dir, os.sep.join(mcase))
        result[case].nested_assign(mcase, _analyze_case(mcase, model_path, bench_path, config))
    print_result(case,result) #TODO
    functions.create_page_from_template("numerics.html",
            os.path.join(variables.index_dir, "numerics", case+".html"))
    functions.write_json(result, os.path.join(variables.output_dir,"numerics"), case+".json")
    summarize_result(result, summary)


def _analyze_case(case, model_dir, bench_dir, config):
    """ Run all of the numerics checks on a particular case """
    result = LIVVDict()
    str_to_case = {
                "ismip-hom" : ismip
            }
    model_files = list(set([os.path.basename(f) for f in 
                    glob.glob(os.path.join(model_dir, "*" + config["output_ext"]))]))
    if bench_dir is not None:
        bench_files = list(set([os.path.basename(f) for f in glob.glob(
            os.path.join(variables.cwd , bench_dir, "*" + config["bench_ext"]))]))
    if len(model_files) > 0 and len(bench_files) > 0:
        result[model_files[0]] = ismip(os.path.join(model_dir,model_files[0]), 
                                        os.path.join(bench_dir,bench_files[0]),
                                        config)
    return result


def print_result(case,result):
    pass


def summarize_result(result, summary):
    """ Trim out some data to return for the index page """
    # Get the number of bit for bit failures
    # Get the number of config matches
    # Get the number of files parsed


def populate_metadata():
    """ Provide some top level information """
    return {"Type" : "Summary",
            "Title" : "Numerics",
            "Headers" : ["Max Error", "RMSE"]}


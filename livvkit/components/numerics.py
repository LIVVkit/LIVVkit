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
"""
import os
import glob
import numpy as np
from netCDF4 import Dataset

import livvkit
from livvkit.util import functions
from livvkit.util.datastructures import LIVVDict
from livvkit.util.datastructures import ElementHelper

import livvkit.components.numerics_tests.ismip as ismip

def _run_suite(case, config, summary):
    """ Run the full suite of numerics tests """
    config["name"] = case
    analysis_data = {} 
    bundle = livvkit.numerics_model_module
    model_dir = os.path.join(livvkit.model_dir, config['data_dir'], case)
    bench_dir = os.path.join(livvkit.bench_dir, config['data_dir'], case)
    plot_dir = os.path.join(livvkit.output_dir, "numerics", "imgs")
    config["plot_dir"] = plot_dir
    functions.mkdir_p(plot_dir)
    model_cases = functions.collect_cases(model_dir) 
    bench_cases = functions.collect_cases(bench_dir)
    
    for mscale in sorted(model_cases):
        bscale = bench_cases[mscale] if mscale in bench_cases else []
        for mproc in model_cases[mscale]:
            config["case"] = '-'.join([mscale,mproc])
            bpath = (os.path.join(bench_dir, mscale, mproc.replace("-", os.sep)) 
                            if mproc in bscale else "")
            mpath = os.path.join(model_dir, mscale, mproc.replace("-", os.sep))
            analysis_data[config["case"]] = _analyze_case(bundle, mpath, bpath, config)

    try:
        analysis_plots = ElementHelper.gallery("Numerics Plots", ismip.hom(config, analysis_data))
    except KeyError:
        analysis_plots = ElementHelper.error("Numerics Plots", "Missing data")
    
    el = [ 
            analysis_plots
         ]
    result = ElementHelper.page(case, config["description"], element_list=el) 

    summary[case] = _summarize_result(analysis_data, config)
    _print_result(case,result) #TODO

    functions.create_page_from_template("numerics.html",
            os.path.join(livvkit.index_dir, "numerics", case+".html"))
    functions.write_json(result, os.path.join(livvkit.output_dir,"numerics"), case+".json")


def _analyze_case(bundle, model_dir, bench_dir, config):
    """ Run all of the numerics tests on a particular case """
    model_files = list(set(glob.glob(os.path.join(model_dir, "*" +
                            config["output_ext"]))))
    bench_files = list(set(glob.glob(os.path.join(bench_dir, "*" + 
                            config["output_ext"]))))
   
    if model_files == [] or bench_files == []:
        return {'test' : {}, 'bench' : {}} 
    
    which_experiment = config['name'].split('-')[-1]
    plot_data = bundle.get_plot_data(ismip.setup[which_experiment], model_files[0], bench_files[0], config)

    return plot_data


def _print_result(case,result):
    pass


def _summarize_result(result, config):
    """ Trim out some data to return for the index page """
    summary = LIVVDict()
    for case in result.keys():
        summary[case] = "test"
        

    return summary


def _populate_metadata():
    """ Provide some top level information """
    return {"Type" : "Summary",
            "Title" : "Numerics",
            "Headers" : ["Max Error", "RMSE"]}


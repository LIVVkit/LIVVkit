# coding=utf-8
# Copyright (c) 2015-2018, UT-BATTELLE, LLC
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
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import importlib

import livvkit
from livvkit.util import functions
from livvkit.util import elements


def run_suite(case, config, summary):
    """ Run the full suite of numerics tests """
    m = importlib.import_module(config['module'])
    m.set_up()
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
            full_name = '-'.join([mscale, mproc])
            bpath = (os.path.join(bench_dir, mscale, mproc.replace("-", os.path.sep))
                     if mproc in bscale else "")
            mpath = os.path.join(model_dir, mscale, mproc.replace("-", os.path.sep))
            model_data = functions.find_file(mpath, "*" + config["output_ext"])
            bench_data = functions.find_file(bpath, "*" + config["output_ext"])
            analysis_data[full_name] = bundle.get_plot_data(model_data,
                                                            bench_data,
                                                            m.setup[case],
                                                            config)
    try:
        el = m.run(config, analysis_data)
    except KeyError:
        el = elements.error("Numerics Plots", "Missing data")
    result = elements.page(case, config['description'], element_list=el)
    summary[case] = _summarize_result(m, analysis_data, config)
    _print_summary(m, case, summary[case])
    functions.create_page_from_template("numerics.html",
                                        os.path.join(livvkit.index_dir, "numerics", case + ".html"))
    functions.write_json(result, os.path.join(livvkit.output_dir, "numerics"), case + ".json")


def _print_summary(module, case, summary):
    try:
        module.print_summary(case, summary)
    except (NotImplementedError, AttributeError):
        print("    Ran " + case + "!")
        print("")


def _summarize_result(module, data, config):
    try:
        summary = module.summarize_result(data, config)
    except (NotImplementedError, AttributeError):
        status = "Could not retrieve summary, open page for statistics"
        summary = {"": {"Test mean % error": status,
                        "Bench mean % error": "",
                        "Coefficient of variation": ""}}
    return summary


# noinspection PyUnusedLocal
def populate_metadata(case, config):
    metadata = {"Type": "Summary",
                "Title": "Numerics",
                "Headers": ["Bench mean % error", "Test mean % error", "Coefficient of variation"]}
    return metadata

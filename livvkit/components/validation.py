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
Validation Test Base Module
"""
import os
import importlib

import livvkit
from livvkit.util import functions
from livvkit.util.datastructures import LIVVDict

def _run_suite(case, config, summary):
    """ Run the full suite of validation tests """
    m = importlib.import_module(config['module'])
    result = m.run(case, config)
    summary[case] = _summarize_result(m, result)
    _print_summary(m, case, summary[case])
    functions.create_page_from_template("validation.html",
            os.path.join(livvkit.index_dir, "validation", case + ".html"))
    functions.write_json(result, os.path.join(livvkit.output_dir, "validation"), case + ".json")


def _print_summary(module, case, summary):
    try:
        module.print_summary()
    except:
        print("    Ran " + case + "!")
        print("")


def _summarize_result(module, result):
    try:
        summary = module.summarize_result(result, summary)
    except:
        status = "Success"
        for e in result.get("Data").get("Elements"):
            if e.get("Type") == "Error":
                status = "Failure"
        summary = {"" : {"Outcome" : status}} 
    return summary 
        

def _populate_metadata():
    try:
        metadata= module.populate_metadata()
    except:
        metadata = {"Type" : "Summary",
                    "Title" : "Validation",
                    "Headers" : ["Outcome"]}
    return metadata


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
Validation Test Base Module
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import six

import os
import importlib

import livvkit
from livvkit.util import functions

ERR_MISSING_MOD_MSG = """
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                       UH OH!")
----------------------------------------------------------
Could not find the module for {}:
    {}

The module must be specified as an import statement of a
module that can be found on your python, or a valid path
to a python module file (specified either relative to your
current working directory or absolutely).
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

ERR_MISSING_DEP_MSG = """
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                       UH OH!")
----------------------------------------------------------
{} depends on {}. 

Please install it before using this extension; `conda` or
`pip` is recommended. 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

ERR_MISSING_DEP_CONDA_MSG = """
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                       UH OH!")
----------------------------------------------------------
{} depends on {}. 

If you're using `conda` you can update your environment
with the required packages by issuing this command:
    conda env update --name {} -f {}

Otherwise, install the packages listed in the above *.yml
file. 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""


def _case_dep_err(mod_path):
    yml_path = mod_path.replace('.py', '.yml')
    conda_env = os.environ.get('CONDA_DEFAULT_ENV')
    if conda_env and os.path.isfile(yml_path):
        return ERR_MISSING_DEP_CONDA_MSG.format('{}', '{}', conda_env, os.path.relpath(yml_path, os.getcwd()))
    else:
        return ERR_MISSING_DEP_MSG


def _load_case_module(case, config):
    try:
        m = importlib.import_module(config['module'])
    except ImportError:
        mod_path = os.path.abspath(config['module'])
        try:
            if six.PY2:
                import imp
                m = imp.load_source(case, mod_path)
            elif six.PY3:
                # noinspection PyUnresolvedReferences
                spec = importlib.util.spec_from_file_location(case, mod_path,
                                                              submodule_search_locations=os.path.dirname(mod_path))
                # noinspection PyUnresolvedReferences
                m = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(m)
            else:
                raise
        except IOError:
            # imp.load_source (py2) and spec.loader.exec_module (py3) raises an IOError if module isn't found
            print(ERR_MISSING_MOD_MSG.format(case, os.path.relpath(mod_path, os.getcwd())))
            raise
        except ImportError as iie:
            # If module's internal import statements fail
            dep = str(iie).split()[-1] if six.PY2 else iie.name 
            print(_case_dep_err(mod_path).format(case, dep))
            raise
        
    return m


def run_suite(case, config, summary):
    """ Run the full suite of validation tests """
    m = _load_case_module(case, config)

    result = m.run(case, config)
    summary[case] = _summarize_result(m, result)
    _print_summary(m, case, summary)
   
    if result['Type'] == 'Book':
        for name, page in six.iteritems(result['Data']):
            functions.create_page_from_template("validation.html",
                                                os.path.join(livvkit.index_dir, "validation", name + ".html"))
            functions.write_json(page, os.path.join(livvkit.output_dir, "validation"), name + ".json")
    else:
        functions.create_page_from_template("validation.html",
                                            os.path.join(livvkit.index_dir, "validation", case + ".html"))
        functions.write_json(result, os.path.join(livvkit.output_dir, "validation"), case + ".json")


def _print_summary(module, case, summary):
    try:
        try:
            module.print_summary(summary[case])
        except TypeError:
            module.print_summary(case, summary[case])
    except (NotImplementedError, AttributeError):
        print("    Ran " + case + "!")
        print("")


def _summarize_result(module, result):
    try:
        summary = module.summarize_result(result)
    except (NotImplementedError, AttributeError):
        status = "Success"
        if result["Type"] == "Error":
            status = "Failure"
        summary = {"": {"Outcome": status}}
    return summary


def populate_metadata(case, config):
    m = _load_case_module(case, config)
    try:
        try:
            metadata = m.populate_metadata()
        except TypeError:
            metadata = m.populate_metadata(case, config)
    except (NotImplementedError, AttributeError):
        metadata = {"Type": "ValSummary",
                    "Title": "Validation",
                    "TableTitle": "Validation",
                    "Headers": ["Outcome"]}

    return metadata

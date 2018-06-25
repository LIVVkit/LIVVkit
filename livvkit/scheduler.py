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
Provides functions for scheduling the runs of tests.
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import six

import multiprocessing


def run(run_type, module, config):
    """
    Collects the analyses cases to be run and launches processes for each of
    them.

    Args:
        run_type: A string representation of the run type (eg. verification)
        module: The module corresponding to the run.  Must have a run_suite function
        config: The configuration for the module
    """
    print(" -----------------------------------------------------------------")
    print("   Beginning " + run_type.lower() + " test suite ")
    print(" -----------------------------------------------------------------")
    print("")
    summary = run_quiet(module, config)
    print(" -----------------------------------------------------------------")
    print("   " + run_type.capitalize() + " test suite complete ")
    print(" -----------------------------------------------------------------")
    print("")
    return summary


def run_quiet(module, config, group=True):
    tests = [t for t in six.iterkeys(config) if isinstance(config[t], dict)]
    summary = launch_processes(tests, module, group=group, **config)
    return summary


def launch_processes(tests, run_module, group=True, **config):
    """ Helper method to launch processes and sync output """
    manager = multiprocessing.Manager()
    test_summaries = manager.dict()
    process_handles = [multiprocessing.Process(target=run_module.run_suite,
                       args=(test, config[test], test_summaries)) for test in tests]
    for p in process_handles:
        p.start()
    for p in process_handles:
        p.join()

    if group:
        summary = run_module.populate_metadata(tests[0], config[tests[0]])
        summary["Data"] = dict(test_summaries)
        return summary
    else:
        test_summaries = dict(test_summaries)
        summary = []
        for ii, test in enumerate(tests):
            summary.append(run_module.populate_metadata(test, config[test]))
            if summary[ii]:
                summary[ii]['Data'] = {test: test_summaries[test]}
        return summary

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

import os
import sys
import multiprocessing as mp

import pandas as pd

import livvkit
from livvkit import elements


def pool_worker(run_type, run_suite, test, config):
    sys.stdout = open(
        os.path.join(livvkit.index_dir, 'logs', '{}-{}.stdout'.format(run_type, test)),
        'a',
    )
    sys.stderr = open(
        os.path.join(livvkit.index_dir, 'logs', '{}-{}.stderr'.format(run_type, test)),
        'a',
    )

    summary = run_suite(test, config)

    sys.stdout.flush()
    sys.stderr.flush()

    return summary


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
    summary = run_quiet(run_type, module, config)
    print(" -----------------------------------------------------------------")
    print("   " + run_type.capitalize() + " test suite complete ")
    print(" -----------------------------------------------------------------")
    print("")
    return summary


def run_quiet(run_type, module, config, group=True):
    tests = [t for t in config if isinstance(config[t], dict)]
    if livvkit.pool_size == 0:
        test_summaries = {}
        for test in tests:
            test_summaries[test] = module.run_suite(test, config[test])
    else:
        test_summaries = launch_processes(run_type, tests, module, config)

        for t in tests:
            with open(os.path.join(livvkit.index_dir, 'logs', '{}-{}.stdout'.format(run_type, t))) as log:
                stdout = log.read()
            print(stdout)

    if group:
        meta = module.populate_metadata(tests[0], config[tests[0]])
        df = pd.concat(
            {k: pd.DataFrame.from_dict(v, orient='index') for k, v, in test_summaries.items()},
            names=['case', 'scale']
        ).reset_index()
        summary = elements.Table(meta['Title'], df.set_index('case'))
    else:
        summary = []
        for ii, t in enumerate(tests):
            meta = module.populate_metadata(t, config[t])
            df = pd.DataFrame.from_dict(test_summaries[t], orient='index')
            summary.append(elements.Table(meta['title'], df))

    return summary


def launch_processes(run_type, tests, run_module, config):
    """ Helper method to launch processes and sync output """
    test_summaries = {}
    with mp.Pool(livvkit.pool_size) as pool:
        results = [
            pool.apply_async(pool_worker, (run_type, run_module.run_suite, t, config[t])) for t in tests
        ]

        for t, r in zip(tests, results):
            test_summaries[t] = r.get()

    return test_summaries

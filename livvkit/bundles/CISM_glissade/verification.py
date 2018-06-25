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
Provides CISM_glissade specific verification tools
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import six

import os
import numpy as np

from six.moves.configparser import ConfigParser

from livvkit.util import elements


def parse_log(file_path):
    """
    Parse a CISM output log and extract some information.

    Args:
        file_path: absolute path to the log file

    Return:
        A dictionary created by the elements object corresponding to
        the results of the bit for bit testing
    """
    if not os.path.isfile(file_path):
        return elements.error("Output Log", "Could not open file: " + file_path.split(os.sep)[-1])

    headers = ["Converged Iterations",
               "Avg. Iterations to Converge",
               "Processor Count",
               "Dycore Type"]

    with open(file_path, 'r') as f:
        dycore_types = {"0": "Glide",
                        "1": "Glam",
                        "2": "Glissade",
                        "3": "Albany_felix",
                        "4": "BISICLES"}
        curr_step = 0
        proc_count = 0
        iter_number = 0
        converged_iters = []
        iters_to_converge = []
        for line in f:
            split = line.split()
            if ('CISM dycore type' in line):
                if line.split()[-1] == '=':
                    dycore_type = dycore_types[next(f).strip()]
                else:
                    dycore_type = dycore_types[line.split()[-1]]
            elif ('total procs' in line):
                proc_count += int(line.split()[-1])
            elif ('Nonlinear Solver Step' in line):
                curr_step = int(line.split()[4])
            elif ('Compute ice velocities, time = ' in line):
                converged_iters.append(curr_step)
                curr_step = float(line.split()[-1])
            elif ('"SOLVE_STATUS_CONVERGED"' in line):
                split = line.split()
                iters_to_converge.append(int(split[split.index('"SOLVE_STATUS_CONVERGED"') + 2]))
            elif ("Compute dH/dt" in line):
                iters_to_converge.append(int(iter_number))
            elif len(split) > 0 and split[0].isdigit():
                iter_number = split[0]
        if iters_to_converge == []:
            iters_to_converge.append(int(iter_number))
    data = {
        "Dycore Type": dycore_type,
        "Processor Count": proc_count,
        "Converged Iterations": len(converged_iters),
        "Avg. Iterations to Converge": np.mean(iters_to_converge)
    }
    return elements.table("Output Log", headers, data)


def parse_config(file_path):
    """
    Convert the CISM configuration file to a python dictionary

    Args:
        file_path: absolute path to the configuration file

    Returns:
        A dictionary representation of the given file
    """
    if not os.path.isfile(file_path):
        return {}
    parser = ConfigParser()
    parser.read(file_path)
    # Strip out inline comments
    for s in parser._sections:
        for v in six.iterkeys(parser._sections[s]):
            parser._sections[s][v] = parser._sections[s][v].split("#")[0].strip()
    return parser._sections

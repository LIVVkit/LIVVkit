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
The LIVV Performance Parser.

@author: arbennett
"""

import re
import os
import glob
    
def get_processor_count(self, lines):
    """ Gets the number of mpi tasks from the gptl file """
    data = ''.join([line for line in lines if re.match("\** GLOBAL STATISTICS \**", line) is not None])
    procs = [int(s) for s in data.split() if s.isdigit()]
    if len(procs) > 0:
        return procs[0]
    else:
        return 0


def get_column_names(self, lines):
    """ Get the names of each of the column headers """
    for idx, line in enumerate(lines):
        if line.startswith("name"):
            header_idx = idx
            headers = line.replace('(', '').replace(')', '').split()
            headers = headers[1:]
            break

    for idx, head in enumerate(headers):
        if head == 'proc':
            head = '_'.join([headers[idx-1], head])
        elif head == 'thrd':
            head = '_'.join([headers[idx-2], head])
        headers[idx] = head

    return headers, header_idx


def parse_gptl(self, file_path):
    """ Parses a gptl file """
    timing_data = []
    with open(file_path, 'r') as gptl:
        lines = gptl.readlines()
        
        # Make sure this is a gptl file
        if not bool(sum([re.match("\$Id: gptl.c*", line) is not None for line in lines])):
            return timing_data
        
        n_procs = self.get_processor_count(lines)
        headers, idx = self.get_column_names(lines)

        for line in lines[idx+1:]:
            line = line.replace('(', '').replace(')', '').split()
            if len(line) != 0:
                timing_data.append((line[0], []))
                for idx, value in enumerate(line[1:]):
                    timing_data[-1][-1].append((headers[idx], value))
    
    return timing_data


def parse_simple(self, file_path):
    """ Parse a timing file that only lists run time """
    pass




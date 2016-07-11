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
Master module for shelf test cases  Inherits methods from the Abstract_test
class from the base module.  Shelf specific verification is performed by calling
the run() method, which gathers & passes the necessary information to the run_case()
method.  Both methods are found in the base class.

@author: arbennett
"""
import os
import fnmatch

from verification.base import AbstractTest
import util.variables

def get_name(): return "Shelf"

class Test(AbstractTest):

    def __init__(self):
        """ Constructor """
        super(self.__class__, self).__init__()
        self.name = "shelf"
        self.model_dir = util.variables.input_dir + os.sep + 'shelf'
        self.bench_dir = util.variables.benchmark_dir + os.sep + 'shelf'
        self.description = "Simulates two shelf conditions, confined and " + \
                            "circular.  The confined shelf is an idealized 500m " + \
                            "ice shelf in a confined, rectangular embayment.  The " + \
                            "circular shelf is a 1000 m thick circular shelf grounded " + \
                            "at the center."

    def collect_cases(self):
        """ Searches through the data directory and gathers the test cases to run """
        self.tests_run = sorted(set('.'.join(fn.split('-')[-1].split('.')[0:2]) for fn in fnmatch.filter(os.listdir(self.model_dir), 'shelf-*')))


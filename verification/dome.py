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
Master module for dome test cases.  Inherits methods from the Abstract_test
class from the base module.  Dome specific verification is performed by calling
the run() method, which gathers & passes the necessary information to the run_dome()
method.

Created on Dec 8, 2014

@author: arbennett
"""
import os
import fnmatch
import multiprocessing

from verification.base import AbstractTest
from util.parser import Parser
import util.variables

def get_name(): return "Dome"


class Test(AbstractTest):
    """
    Main class for handling dome verification tests
    
    The dome test cases inherit functionality from AbstractTest for checking 
    bit-for-bittedness from a model run. This class handles evolving and \
    diagnostic variations of the dome case.
    """
    
    def __init__(self):
        """ Constructor """
        super(self.__class__, self).__init__()
        self.name = "dome"
        self.model_dir = util.variables.input_dir + os.sep + "dome"
        self.bench_dir = util.variables.benchmark_dir + os.sep + "dome"
        self.description = "3-D paraboloid dome of ice with a circular, 60 km" + \
                      " diameter base sitting on a flat bed.  For this" + \
                      " set of experiments a quasi no-slip basal condition in" + \
                      " imposed by setting. A zero-flux boundary condition is" + \
                      " applied to the dome margins. "

    def collect_cases(self):
        """ Returns a list of the dome cases found in the data """
        test_types = set()
        model_configFiles = fnmatch.filter(os.listdir(self.model_dir), 'dome*.config')
        for mcf in model_configFiles:
            test_types.add( mcf.split('.')[1] )
        self.tests_run = sorted( set(test_types) )



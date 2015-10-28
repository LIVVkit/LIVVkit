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
Master module for ISMIP numerics. 

@author: arbennett
"""
import os
import fnmatch
import numpy as np

from numerics.base import AbstractTest
import util.variables

def get_name(): return "Ismip-hom"

class Test(AbstractTest):

    def __init__(self):
        """ Constructor """
        super(self.__class__, self).__init__()
        self.name = "ismip-hom"
        self.model_dir = util.variables.input_dir + os.sep + 'ismip-hom'
        self.bench_dir = util.variables.benchmark_dir + os.sep + 'ismip-hom'
        self.description = "The Ice Sheet Model Intercomparison Project for Higher-Order Models (ISMIP-HOM) " + \
                           "prescribes a set of experiments meant to test the implementation of higher-order" + \
                           " physics.  For more information, see <a href=http://homepages.ulb.ac.be/~fpattyn/ismip/>" +\
                           "http://homepages.ulb.ac.be/~fpattyn/ismip/</a> \n" + \
                           " Simulates steady ice flow over a surface with periodic boundary conditions"

    def collect_cases(self):
        """ Searches through the data directory and gathers the test cases to run """
        self.tests_run = sorted(set('.'.join(fn.split('-')[-1].split('.')[0:2]) for fn in fnmatch.filter(os.listdir(self.model_dir), 'ismip-hom-?.*.nc')))


    def run_case(self, test_case, output):
        """
        Run a case
        """
        run_functs = {'a' : self.run_experiment_a,
                      'c' : self.run_experiment_c,
                      'f' : self.run_experiment_f}
        case, res = test_case.split('.')
        run_functs[case](res)
        

    def run_experiment_a(self, resolution):
        """
        Details here
        """
        fpath = ""
        data_files = sorted(set(fn for fn in fnmatch.filter(os.listdir(self.data_dir), 'ismip-hom-a.*.txt')))
        #x,y,vx_mean,vx_stdev,vy_mean,vy_stdev = np.loadtxt(fpath, unpack=True, delimiter=',', skiprows=1, usecols=(0,1,2,3,6,7)) 


    def run_experiment_c(self, resolution):
        """
        Details here
        """
        pass
        data_files = sorted(set(fn for fn in fnmatch.filter(os.listdir(self.data_dir), 'ismip-hom-c.*.txt')))


    def run_experiment_f(self, resolution):
        """
        Details here
        """
        pass
        data_files = sorted(set(fn for fn in fnmatch.filter(os.listdir(self.data_dir), 'ismip-hom-f.*.txt')))


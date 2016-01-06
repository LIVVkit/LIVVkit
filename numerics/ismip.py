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
from netCDF4 import Dataset

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot

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
        self.tests_run = sorted(set('.'.join(fn.split('-')[-1].split('.')[0:2]) for fn in\
                         fnmatch.filter(os.listdir(self.model_dir), 'ismip-hom-?.*.nc')))


    def run_case(self, test_case, output):
        """
        Run a case
        """
        run_functs = {'a' : self.run_experiment_a,
                      'c' : self.run_experiment_c,
                      'f' : self.run_experiment_f}
        case, res = test_case.split('.')
        self.summary[test_case] = dict()
        self.summary[test_case] = run_functs[case](res)

    def run_experiment_a(self, resolution):
        """
        Details here
        """
        # Grab the ISMIP benchmark data & calculate velocity norm mean and standard deviation
        exp_type = 'a'
        return self.do_plots(exp_type, resolution)
        

    def run_experiment_c(self, resolution):
        """
        Details here
        """
        exp_type = 'c'
        return self.do_plots(exp_type, resolution)


    def run_experiment_f(self, resolution):
        """
        Details here
        """
        exp_type = 'f'
        return self.do_plots(exp_type, resolution)

    def do_plots(self, exp_type, resolution):
        """ Description """
        plots = self.manager.list() 
        fpath = os.path.join(util.variables.cwd,"numerics","data",\
                "ismip-hom-" + exp_type + "." + resolution + ".lmla.txt")

        x, y, vx_mean, vx_stdev, vx_min, vx_max, vy_mean, vy_stdev, vy_min, vy_max =\
            np.loadtxt(fpath, unpack=True, delimiter=',',skiprows=1, usecols=(0,1,2,3,4,5,6,7,8,9)) 

        n_pts = int(np.sqrt(len(x)))
        vnorm_mean =  np.reshape(np.sqrt(np.add(np.power(vx_mean,2), np.power(vy_mean,2))),\
                                 (n_pts,n_pts))
        vnorm_stdev = np.reshape(np.sqrt(np.add(np.power(vx_stdev,2), np.power(vy_stdev,2))),\
                                 (n_pts,n_pts))
        vnorm_plus =  np.reshape(np.add(vnorm_mean, vnorm_stdev), (n_pts,n_pts))
        vnorm_minus = np.reshape(np.subtract(vnorm_mean, vnorm_stdev), (n_pts,n_pts))
        vnorm_max = np.reshape(np.sqrt(np.add(np.power(vx_max,2), np.power(vy_max,2))),\
                               (n_pts,n_pts))
        vnorm_min = np.reshape(np.sqrt(np.add(np.power(vx_min,2), np.power(vy_min,2))),\
                               (n_pts,n_pts))

        # Grab the model data
        data_files = sorted(set(fn for fn in fnmatch.filter(os.listdir(self.model_dir), \
                                'ismip-hom-' + exp_type + '.'+resolution+'.????.out.nc')))
        for fname in data_files:
            dataset = Dataset(os.path.join(self.model_dir,fname),'r')
            uvel  = dataset.variables['uvel'][0,0,:,:]
            vvel  = dataset.variables['vvel'][0,0,:,:]
            shape = np.shape(uvel)
            vnorm = np.sqrt(np.add(np.power(uvel,2), np.power(vvel,2)))
            floor = np.subtract(vnorm_min[1:-1,1:-1],   vnorm)
            ciel  = np.subtract(vnorm_max[1:-1,1:-1],   vnorm)
            under = np.subtract(vnorm_minus[1:-1,1:-1], vnorm)
            over  = np.subtract(vnorm_plus[1:-1,1:-1],  vnorm)
            bad_data = np.zeros(shape)
            for i in range(shape[0]):
                for j in range(shape[0]):
                    if floor[i,j]>0:
                        bad_data[i,j] = -2 # CISM < MIN_ISMIP
                    elif ciel[i,j]<0:
                        bad_data[i,j] = 2  # CISM > MAX_ISMIP
                    elif under[i,j]>0:
                        bad_data[i,j] = -1 # CISM < MU - SIGMA 
                    elif over[i,j]<0:
                        bad_data[i,j] = 1  # CISM > MU + SIGMA
            mean_diff = 100.0*np.divide(np.subtract(vnorm_mean[1:-1,1:-1], vnorm),\
                                                    vnorm_mean[1:-1,1:-1])
            
            plt_name = os.path.join(util.variables.index_dir, 'numerics', self.name.capitalize(),\
                        'imgs', exp_type + resolution + '_percent_diff.png')
            pyplot.figure()
            pyplot.imshow(mean_diff)
            pyplot.title('% Difference from mean')
            pyplot.colorbar()
            pyplot.savefig(plt_name)
            plots.append(plt_name.split(os.sep)[-1])

            plt_name = os.path.join(util.variables.index_dir, 'numerics', self.name.capitalize(),\
                        'imgs', exp_type + resolution + '_outliers.png')
            pyplot.figure()
            pyplot.imshow(bad_data,interpolation='nearest')
            pyplot.colorbar()
            pyplot.title('Data outside of standard deviation')
            pyplot.savefig(plt_name)
            plots.append(plt_name.split(os.sep)[-1])
        return plots

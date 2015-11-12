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
import matplotlib.pyplot as plt

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
        # Grab the ISMIP benchmark data & calculate velocity norm mean and standard deviation
        # TODO: There is a rather large issue with the way that the assimilated data is laid out
        #       This data comes in (x,y,var1,var2,...,varn) form, meaning when we get the data in
        #       from the file we end up with a 1xN (or Nx1, whichever) for each column.  The CISM
        #       output data is in grid format, so each variable has an NxM array.
        #
        #       It will probably be easier to remap the assimilated data - this could be done one
        #       of two ways.  The first way would involve more work on the assimilation scripts.
        #       Instead of outputting plain text, it would be nice if the data were output in 
        #       netcdf files that have the same structure as the CISM output.  This would make,
        #       it easier to compare as well as well as making the files more easily human 
        #       readable.  it would also reduce the amount of processing that we would need to 
        #       do inside of LIVV.  Okay, this will be a WIP.
        fpath = os.path.join(util.variables.cwd,"numerics","data","ismip-hom-a."+resolution+".lmla.txt")
        x,y,vx_mean,vx_stdev,vy_mean,vy_stdev = np.loadtxt(fpath, unpack=True, delimiter=',', skiprows=1, usecols=(0,1,2,3,6,7)) 
        grid_shape = int(np.sqrt(len(x)))
        vnorm_mean =  np.reshape(np.sqrt(np.add(np.power(vx_mean,2), np.power(vy_mean,2))), (grid_shape,grid_shape))
        vnorm_stdev = np.reshape(np.sqrt(np.add(np.power(vx_stdev,2), np.power(vy_stdev,2))), (grid_shape,grid_shape))
        vnorm_plus =  np.reshape(np.add(vnorm_mean, vnorm_stdev), (grid_shape,grid_shape))
        vnorm_minus = np.reshape(np.subtract(vnorm_mean, vnorm_stdev), (grid_shape,grid_shape))

        # Grab the model data
        data_files = sorted(set(fn for fn in fnmatch.filter(os.listdir(self.model_dir), 'ismip-hom-a.'+resolution+'.????.out.nc')))
        for fname in data_files:
            dataset = Dataset(os.path.join(self.model_dir,fname),'r')
            uvel = dataset.variables['uvel'][0,1,:,:]
            vvel = dataset.variables['vvel'][0,1,:,:]
            shape = np.shape(uvel)
            vnorm = np.sqrt(np.add(np.power(uvel,2), np.power(vvel,2)))
            under = np.subtract(vnorm,vnorm_minus[1:-1,1:-1])
            over = np.subtract(vnorm_plus[1:-1,1:-1],vnorm)
            bad_data = np.zeros(shape)
            for i in range(shape[0]):
                for j in range(shape[0]):
                    if under[i,j]<0 or over[i,j]>0:
                        bad_data[i,j]=1
            mean_diff = np.subtract(vnorm, vnorm_mean[1:-1,1:-1])
            plt.subplot(1,2,1)
            plt.imshow(mean_diff)
            plt.title('Mean diff')
            plt.colorbar()
            plt.subplot(1,2,2)
            plt.imshow(bad_data)
            plt.colorbar()
            plt.title('Bad data')
            plt.savefig('/home/bzq/ismip_'+fname+'.png')

    def run_experiment_c(self, resolution):
        """
        Details here
        """
        return
        # Grab the ISMIP benchmark data & calculate velocity norm mean and standard deviation
        fpath = os.path.join(util.variables.cwd,"numerics","data","ismip-hom-c."+resolution+".lmla.txt")
        x,y,vx_mean,vx_stdev,vy_mean,vy_stdev = np.loadtxt(fpath, unpack=True, delimiter=',', skiprows=1, usecols=(0,1,2,3,6,7)) 
        vnorm_mean = np.sqrt(vx_mean + vy_mean)
        vnorm_stdev = np.sqrt(vx_stdev + vy_stdev)
        
        # Grab the model data
        data_files = sorted(set(fn for fn in fnmatch.filter(os.listdir(self.model_dir), 'ismip-hom-c.'+resolution+'.????.out.nc')))



    def run_experiment_f(self, resolution):
        """
        Details here
        """
        return
        # Grab the ISMIP benchmark data & calculate velocity norm mean and standard deviation
        fpath = os.path.join(util.variables.cwd,"numerics","data","ismip-hom-f."+resolution+".lmla.txt")
        x,y,vx_mean,vx_stdev,vy_mean,vy_stdev = np.loadtxt(fpath, unpack=True, delimiter=',', skiprows=1, usecols=(0,1,2,3,6,7)) 
        vnorm_mean = np.sqrt(vx_mean + vy_mean)
        vnorm_stdev = np.sqrt(vx_stdev + vy_stdev)
        
        # Grab the model data
        data_files = sorted(set(fn for fn in fnmatch.filter(os.listdir(self.model_dir), 'ismip-hom-f.'+resolution+'.????.out.nc')))



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
CISM-glissade module for numerics analysis
"""

import os
import numpy
import scipy

from netCDF4 import Dataset
from scipy import interpolate 

from livvkit.util import variables

print(variables.cwd)

class DataGrid:
    def __init__(self, data):
        self.y = data.variables['y1']
        self.ny = self.y[:].shape[0]
        self.dy = self.y[1] - self.y[0]
        self.Ly = self.y[-1] - self.y[0] + self.dy
        #NOTE: Cell centered grids, hence the dy. 

        self.x = data.variables['x1']
        self.nx = self.x[:].shape[0]
        self.dx = self.x[1] - self.x[0]
        self.Lx = self.x[-1] - self.x[0] + self.dx
        #NOTE: Cell centered grids, hence the dx. 

        self.y_hat = (self.y[:] + self.y[0])/self.Ly
        self.x_hat = (self.x[:] + self.x[0])/self.Lx
   
   
    def make_grids(self):
        self.y_hat_grid, self.x_hat_grid = \
                scipy.meshgrid(self.y_hat[:], self.x_hat[:], indexing='ij')


def get_plot_data(setup, test_file, bench_file, config):
    test_plot_data = {}
    bench_plot_data = {}

    exp = config['name'].split('-')[-1]

    test_data = Dataset(os.path.join(variables.cwd,test_file), 'r')
    bench_data = Dataset(os.path.join(variables.cwd,bench_file), 'r')

    test = DataGrid(test_data)
    bench = DataGrid(bench_data)

    y_coord = numpy.linspace(setup['y'][0], setup['y'][1], test.ny)
    x_coord = numpy.linspace(setup['x'][0], setup['x'][1], test.nx)

    test_plot_data['y_hat'] = y_coord
    test_plot_data['x_hat'] = x_coord
    bench_plot_data['y_hat'] = y_coord
    bench_plot_data['x_hat'] = x_coord
    
    for var in config['interp_vars']:
        if var == 'usurf':
            # regular 2d linear interp. but faster. 
            test2plot = interpolate.RectBivariateSpline( test.y_hat, test.x_hat, 
                            test_data.variables[var][-1,:,:], kx=1, ky=1, s=0 ) 
            
            # regular 2d linear interp. but faster. 
            bench2plot = interpolate.RectBivariateSpline( bench.y_hat, bench.x_hat, 
                            bench_data.variables[var][-1,:,:], kx=1, ky=1, s=0 ) 
        
        else:
            # regular 2d linear interp. but faster. 
            test2plot = interpolate.RectBivariateSpline( test.y_hat, test.x_hat, 
                            test_data.variables[var][-1,0,:,:], kx=1, ky=1, s=0 ) 
            
            # regular 2d linear interp. but faster. 
            bench2plot = interpolate.RectBivariateSpline( bench.y_hat, bench.x_hat, 
                            bench_data.variables[var][-1,0,:,:], kx=1, ky=1, s=0 ) 
            
            
        test_plot_data[var] = test2plot(y_coord, x_coord, grid=False)
        bench_plot_data[var] = bench2plot(y_coord, x_coord, grid=False)
        

    if exp in ['a','c']:
        test_plot_data['velnorm_extend'] = \
            numpy.linalg.norm(
                numpy.array([test_plot_data['uvel_extend'],
                             test_plot_data['vvel_extend'] ]),
                axis=0)

        bench_plot_data['velnorm_extend'] = \
            numpy.linalg.norm(
                numpy.array([bench_plot_data['uvel_extend'],
                             bench_plot_data['vvel_extend'] ]),
            axis=0)

    else: # f
        test_plot_data['velnorm_extend'] = \
            numpy.linalg.norm(
                numpy.array([test_plot_data['uvel_extend'],
                             test_plot_data['vvel_extend'],
                             test_plot_data['wvel_ho'] ]),
                axis=0)

        bench_plot_data['velnorm_extend'] = \
            numpy.linalg.norm(
                numpy.array([bench_plot_data['uvel_extend'],
                             bench_plot_data['vvel_extend'],
                             bench_plot_data['wvel_ho'] ]),
            axis=0)

        test_plot_data['usurfnorm'] = test_plot_data['usurf'] - test_plot_data['usurf'][0]
        bench_plot_data['usurfnorm'] = bench_plot_data['usurf'] - bench_plot_data['usurf'][0]

    return {'test': test_plot_data, 'bench': bench_plot_data}
        


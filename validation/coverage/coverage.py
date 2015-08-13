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
Analyze the ice sheet coverage.  For more information check documentation for 
the run() function.

Created on Aug 7, 2015

@author: arbennett
"""

import os
import numpy
import jinja2
import pyproj
import scipy
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset

import util.variables
# import validation.validation_utils.coverage_plot

def run(model_dir, bench_dir, model_data, bench_data, run_args=None):
    """
    Runs the analysis of the coverage of the ice sheet over the land mass.
    Produces both an overall coverage percentage metric and a coverage plot.

    Args:
        model_dir: location of model output
        bench_dir: location of benchmark output
        model_data: the output file from the model run to be analyzed
        bench_data: the output file from the benchmark run to be analyzed
    """
    if not (os.path.exists(model_dir) and os.path.exists(bench_dir)):
        # Add more handling here -- what do we want to return for failed tests
        return
    proj_file = pyproj.Proj('+proj=stere +ellps=WGS84 +datum=WGS84 +lat_ts=71.0 +lat_0=90 +lon_0=321.0 +k_0=1.0')
    proj_lat_lon = pyproj.Proj('+proj=latlong +ellps=WGS84 +datum=WGS84')
    model_dataset = Dataset(model_dir + os.sep + model_data)
    bench_dataset = Dataset(bench_dir + os.sep + bench_data)

    for set in [model_dataset, bench_dataset]:
        # THIS PART NEEDS HELP.  LOOK THROUGH GREENLAND INTERACTS COMMITS FOR HELP
        fig, ax = plt.figure()
        x = set.variables['x1'][:]
        y = set.variables['y1'][:]
        nx = x.shape[0]
        ny = y.shape[0]
        y_grid, x_grid = scipy.meshgrid(y[:], x[:], indexing='ij')
        # This may need to be tweaked
        thk = set.variables['thk'][0]
        
        # Transform coords to lat/lon
        lon, lat = pyproj.transform(proj_file, proj_lat_lon, x_grid.flatten(), y_grid.flatten())
        lat = lat.reshape(ny,nx)
        lon = lon.reshape(ny,nx)

        # Put the thickness in a basemap
        map_thk = Basemap(projection='stere', lat_0=65, lon_0=-25, \
                    llcrnrlat=55, urcrnrlat=85, \
                    llcrnrlon=-50, urcrnrlon=0, \
                    rsphere=6371200, resolution='l', \
                    area_thresh=10000, ax=ax)
        map_thk.drawcoastlines(linewidth=0.25)
        map_thk.fillcontinents(color='grey')
        map_thk.drawmeridians(np.arange(0,360,30))
        map_thk.drawparallels(np.arange(-90,90,30))
        x, y = map_thk(lon,lat)
        cs = map_thk.contour(x, y, thk, 5)

        plt.plot()
        plt.save(util.variables.output_dir + os.sep + 'coverage.png')


 I

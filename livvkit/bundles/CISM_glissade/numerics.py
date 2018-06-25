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
CISM_glissade module for numerics analysis
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import math

import numpy as np

from netCDF4 import Dataset
from scipy import interpolate


class DataGrid:
    """
    Class to handle the CISM_glissade grids, which are cell-centered grids.
    """
    def __init__(self, data):
        self.y = data.variables['y1']
        self.ny = self.y[:].shape[0]
        self.dy = self.y[1] - self.y[0]

        # NOTE: cell centered grids, hence the dy.
        self.Ly = self.y[-1] - self.y[0] + self.dy

        self.x = data.variables['x1']
        self.nx = self.x[:].shape[0]
        self.dx = self.x[1] - self.x[0]

        # NOTE: cell centered grids, hence the dx.
        self.Lx = self.x[-1] - self.x[0] + self.dx

        self.y_hat = (self.y[:] + self.y[0])/self.Ly
        self.x_hat = (self.x[:] + self.x[0])/self.Lx


class RotatedGrid:
    """
    For the ISMIP-HOM f tests, CISM computes the flow of a glacier down an
    inclined plane:

    ::

        z
        ^
        |
        * .
        .    .
        .        .
        *           .
        | .             .
        |    .     ICE      .
        |        .              .
        |            .             .
        |  BED           .            .
        |                    .           *
        |                       .        .
        |                          .     .
        |                             .  .
        |                                *
        |                                |
        |                                |
        |                                |
        0------------------------------------->x


    The origin is at point 0 in the above figure, and the topmost point of the
    glacier is at x=0, z=7 (in km). The slope is 3 degrees. The ice is 1000 m
    tall and flows down the inclined plane.

    ISMIP-HOM, however, defines the coordinate system with the origin located at
    the topmost point of the glacier (0,7) with the x' axis pointing down slope
    and z' pointing perpendicular to the slope. So the coordinate system is
    shifted, and rotated by a=3 degrees from the CISM glissade grid.

    An additional complication is that the surface is computed in CISM on the
    standard grid, but velocities are computed on a staggered, grid.

    This class converts the CISM_glissade coordinate system to the ISMIP-HOM
    coordinate system.
    """
    def __init__(self, alpha, data):
        self.alpha = alpha
        self.y0 = data.variables['y0'][:]
        self.x0 = data.variables['x0'][:]

        self.usurf_ustag = data.variables['usurf'][-1,:,:]
        self.usurf_stag = (  self.usurf_ustag[1: , 1: ] + self.usurf_ustag[1: , :-1]
                           + self.usurf_ustag[:-1, :-1] + self.usurf_ustag[:-1, 1: ]) / 4.0

        self.usurf = -(self.x0)*math.sin(alpha) + (self.usurf_stag-7000.0)*math.cos(alpha)

        self.uvel_stag = data.variables['uvel'][-1,0,:,:]
        self.vvel_stag = data.variables['uvel'][-1,0,:,:]

        try:
            self.wvel_ustag = data.variables['wvel_ho'][-1,0,:,:]
        except:
            self.wvel_ustag = data.variables['wvel'][-1,0,:,:]
        self.wvel_stag = (  self.wvel_ustag[1: , 1: ] + self.wvel_ustag[1: , :-1]
                          + self.wvel_ustag[:-1, :-1] + self.wvel_ustag[:-1, 1: ]) / 4.0

        self.uvel =  self.uvel_stag*math.cos(alpha) + self.wvel_stag*math.sin(alpha)
        self.vvel = -self.uvel_stag*math.sin(alpha) + self.wvel_stag*math.cos(alpha)

        self.x = (self.x0*math.cos(alpha)
                  + (self.usurf_stag[20,:]-7000.0)*math.sin(alpha)
                  )/1000.0 - 50.0
        self.y = self.y0/1000.0 - 50.0


def get_plot_data(test_file, bench_file, setup, config):
    test_plot_data = {}
    bench_plot_data = {}
    exp = config['name'].split('-')[-1]
    test_data = Dataset(test_file, 'r')
    bench_data = Dataset(bench_file, 'r')

    test = DataGrid(test_data)
    bench = DataGrid(bench_data)

    x_coord = setup['interp_points']
    y_coord = np.linspace(setup['y'][0], setup['y'][1], len(x_coord))

    test_plot_data['y_hat'] = y_coord
    test_plot_data['x_hat'] = x_coord
    bench_plot_data['y_hat'] = y_coord
    bench_plot_data['x_hat'] = x_coord

    if exp in ['a', 'c']:
        for var in config['interp_vars']:
            if var == 'usurf':
                # regular 2d linear interp. but faster.
                test2plot = interpolate.RectBivariateSpline(test.y_hat, test.x_hat,
                                                            test_data.variables[var][-1,:,:],
                                                            kx=1, ky=1, s=0)
                bench2plot = interpolate.RectBivariateSpline(bench.y_hat, bench.x_hat,
                                                             bench_data.variables[var][-1,:,:],
                                                             kx=1, ky=1, s=0)
            else:
                # regular 2d linear interp. but faster.
                test2plot = interpolate.RectBivariateSpline(test.y_hat, test.x_hat,
                                                            test_data.variables[var][-1,0,:,:],
                                                            kx=1, ky=1, s=0)
                bench2plot = interpolate.RectBivariateSpline(bench.y_hat, bench.x_hat,
                                                             bench_data.variables[var][-1,0,:,:],
                                                             kx=1, ky=1, s=0)

            test_plot_data[var] = test2plot(y_coord, x_coord, grid=False)
            bench_plot_data[var] = bench2plot(y_coord, x_coord, grid=False)

        test_plot_data['velnorm_extend'] = \
            np.linalg.norm(
                np.array([test_plot_data['uvel_extend'],
                          test_plot_data['vvel_extend'] ]),
                axis=0)
        bench_plot_data['velnorm_extend'] = \
            np.linalg.norm(
                np.array([bench_plot_data['uvel_extend'],
                          bench_plot_data['vvel_extend'] ]),
                axis=0)
    else:  # f
        alpha = math.radians(-3.0)

        test_rotated = RotatedGrid(alpha, test_data)
        bench_rotated = RotatedGrid(alpha, bench_data)

        for var in config['interp_vars']:
            # regular 2d linear interp. but faster.
            test2plot = interpolate.RectBivariateSpline(test_rotated.x, test_rotated.y,
                                                        getattr(test_rotated, var),
                                                        kx=1, ky=1, s=0)
            bench2plot = interpolate.RectBivariateSpline(bench_rotated.x, bench_rotated.y,
                                                         getattr(bench_rotated, var),
                                                         kx=1, ky=1, s=0)

            test_plot_data[var] = test2plot(y_coord, x_coord, grid=False)
            bench_plot_data[var] = bench2plot(y_coord, x_coord, grid=False)

        test_plot_data['velnorm'] = \
            np.linalg.norm(
                np.array([test_plot_data['uvel'],
                          test_plot_data['vvel'] ]),
                axis=0)
        bench_plot_data['velnorm'] = \
            np.linalg.norm(
                np.array([bench_plot_data['uvel'],
                          bench_plot_data['vvel'] ]),
                axis=0)

    return {'test': test_plot_data, 'bench': bench_plot_data}

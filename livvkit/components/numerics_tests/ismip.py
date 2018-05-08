# coding=utf-8
# Copyright (c) 2015-2017, UT-BATTELLE, LLC
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
Utilities to provide numerical verification for the ISMIP test cases
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import six


import os

import numpy as np
import matplotlib.pyplot as plt

import livvkit
from livvkit.util.LIVVDict import LIVVDict
from livvkit.util import elements
from livvkit.util import functions


case_color = {'bench': '#d7191c',
              'test':  '#fc8d59'}

line_style = {'bench': 'o-',
              'test': '-'}

setup = None


def set_up():
    global setup
    setup = functions.read_json(os.path.join(os.path.dirname(__file__), 'ismip.json'))

    for exp, size in [('ismip-hom-a', '005'), ('ismip-hom-c', '005'), ('ismip-hom-f', '000')]:
        recreate_file = os.path.join(livvkit.__path__[0], setup[exp]["data_dir"],
                                     setup[exp]['pattern'][0].replace('???', size))
        setup[exp]['interp_points'] = \
            np.genfromtxt(recreate_file, delimiter=',', missing_values='nan',
                          usecols=(0,), unpack=True)
        if exp == 'ismip-hom-f':
            setup[exp]['interp_points'] = setup[exp]['interp_points']*100 - 50


def get_case_length(case):
    return str(int(case.split('-')[-1][1:])).zfill(3)


def run(config, analysis_data):
    case = config['name']
    if case in ['ismip-hom-a', 'ismip-hom-c', 'ismip-hom-f']:
        coord = 'x_hat'
    else:
        coord = 'y_hat'

    lengths = list(set(
        [get_case_length(d) for d in six.iterkeys(analysis_data)]
        ))

    plot_list = []
    for p, pattern in enumerate(sorted(setup[case]['pattern'])):
        fig_label = pattern.split('_')[1]
        description = ''

        for l in sorted(lengths):
            plt.figure(figsize=(10, 8), dpi=150)
            plt.xlabel(setup[case]['xlabel'][p])
            plt.ylabel(setup[case]['ylabel'][p])

            if case in ['ismip-hom-a', 'ismip-hom-c']:
                plt.title(str(int(l))+' km')
                title = fig_label[0:-1]+'. '+fig_label[-1]+': '+str(int(l))+' km'
            else:
                plt.title('No-Slip Bed')
                title = fig_label[0:-2]+'. '+fig_label[-2:]+': No-Slip Bed'

            plot_file = os.path.join(config["plot_dir"], config['name']+'_'+fig_label+'_'+l+'.png')
            recreate_file = os.path.join(
                    livvkit.__path__[0], setup[case]["data_dir"], pattern
                    ).replace('???', l)
            axis, fs_amin, fs_amax, fs_mean, fs_std, ho_amin, ho_amax, ho_mean, ho_std = \
                np.genfromtxt(recreate_file, delimiter=',', missing_values='nan', unpack=True)

            if case in ['ismip-hom-f']:
                axis = axis*100.0 - 50.0

            plt.fill_between(axis, ho_amin, ho_amax, facecolor='green', alpha=0.5)
            plt.fill_between(axis, fs_amin, fs_amax, facecolor='blue', alpha=0.5)
            plt.plot(axis, fs_mean, 'b-', linewidth=2, label='Full stokes')
            plt.plot(axis, ho_mean, 'g-', linewidth=2, label='Higher order')

            analysis = {}
            for a in six.iterkeys(analysis_data):
                if int(l) == int(a.split('-')[-1][1:]):
                    analysis[a] = analysis_data[a]

            for a in six.iterkeys(analysis):
                for model in sorted(six.iterkeys(analysis[a])):
                    plt.plot(analysis[a][model][coord],
                             analysis[a][model][config['plot_vars'][p]],
                             line_style[model],
                             color=case_color[model],
                             linewidth=2,
                             label=a+'-'+model)

            plt.legend(loc='best')
            if livvkit.publish:
                plt.savefig(os.path.splitext(plot_file)[0]+'.eps', dpi=600)
            plt.savefig(plot_file)
            plt.close()
            plot_list.append(elements.image(title, description, os.path.basename(plot_file)))

    return elements.gallery("Numerics Plots", plot_list)


def summarize_result(data, config):
    case = config['name']
    summary = LIVVDict()
    lengths = list(set([get_case_length(d) for d in six.iterkeys(data)]))

    for p, pattern in enumerate(sorted(setup[case]['pattern'])):
        for l in sorted(lengths):

            recreate_file = os.path.join(
                    livvkit.__path__[0], setup[case]["data_dir"], pattern
                    ).replace('???', l)

            axis, fs_amin, fs_amax, fs_mean, fs_std, ho_amin, ho_amax, ho_mean, ho_std = \
                np.genfromtxt(recreate_file, delimiter=',', missing_values='nan', unpack=True)

            analysis = {}
            for a in six.iterkeys(data):
                if int(l) == int(a.split('-')[-1][1:]):
                    analysis[a] = data[a]

            for a in six.iterkeys(analysis):
                for model in sorted(six.iterkeys(analysis[a])):
                    if setup[case]['ylabel'][p].split(" ")[0].lower() == 'surface':
                        percent_errors = np.divide(analysis[a][model][config['plot_vars'][p]]
                                                   - ho_mean, ho_mean+1000)
                        coefficient = np.divide(ho_std, ho_mean+1000)
                    else:
                        percent_errors = np.divide(analysis[a][model][config['plot_vars'][p]]
                                                   - ho_mean, ho_mean)
                        coefficient = np.divide(ho_std, ho_mean)

                    label = a+' '+setup[case]['ylabel'][p].split(" ")[0]
                    if model.lower() == 'bench':
                        summary[label]['Bench mean % error'] = \
                            '{:3.2%}'.format(np.nanmean(percent_errors))
                    else:
                        summary[label]['Test mean % error'] = \
                            '{:3.2%}'.format(np.nanmean(percent_errors))

                    summary[label]['Coefficient of variation'] = \
                        '{:3.2%}'.format(np.nanmean(coefficient))

    return summary


def print_summary(case, summary):
    """ Show some statistics from the run """
    for subcase in six.iterkeys(summary):
        message = case + " " + subcase
        print("    " + message)
        print("    " + "-"*len(message))
        for key, val in summary[subcase].items():
            print(" "*4 + key.ljust(25) + ":" + val.rjust(7))
        print("")

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

from __future__ import absolute_import, print_function, unicode_literals

import os
import re

from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), 'r') as f:
    long_desc = f.read()
with open(os.path.join(here, 'livvkit', '__init__.py')) as f:
    init_file = f.read()

setup(
      name='livvkit',
      version=re.search(r'{}\s*=\s*[(]([^)]*)[)]'.format('__version_info__'),
                        init_file
                        ).group(1).replace(', ', '.'),

      description='The land ice verification and validation toolkit',
      long_description=long_desc,
      long_description_content_type='text/markdown',

      url='https://github.com/LIVVkit/LIVVkit',

      author='Joseph H. Kennedy et al.',
      author_email='kennedyjh@ornl.gov',

      license='BSD',
      include_package_data=True,

      classifiers=['Development Status :: 5 - Production/Stable',

                   'Intended Audience :: Science/Research',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Software Development :: Testing',

                   'License :: OSI Approved :: BSD License',

                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   ],

      install_requires=['six',
                        'numpy',
                        'scipy',
                        'netCDF4',
                        'matplotlib',
                        'json_tricks==3.11.0'
                        ],

      packages=['livvkit',
                'livvkit.bundles',
                'livvkit.bundles.CISM_glissade',
                'livvkit.components',
                'livvkit.components.numerics_tests',
                'livvkit.data',
                'livvkit.util',
                ],

      entry_points={'console_scripts': ['livv = livvkit.__main__:main']},
      )

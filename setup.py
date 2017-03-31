# Copyright (c) 2015,2016, UT-BATTELLE, LLC
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

from setuptools import setup
from os import path

long_file = path.join(path.abspath(path.dirname(__file__)), 'README.md')
with open(long_file, 'r') as f:
    long_desc = f.read()

# NOTE: Numpy really wants to build from source unless it's already installed,
# which is slow and prone to failure This significanlty make the build more
# robused and much faster.
try:
    import numpy
    print('Found numpy.')
except ImportError:
    import pip
    pip.main(['install', 'numpy'])
    import numpy
    print('Installed numpy via pip.')

setup(
      name='livvkit',
      version='2.0.1',

      description='The land ice verification and validation toolkit.',
      long_description=long_desc,

      url='http://github.com/LIVVkit/LIVVkit',

      author='Joseph H. Kennedy et al.',
      author_email='kennedyjh@ornl.gov',

      license='BSD',
      include_package_data=True,

      classifiers=[
                   'Development Status :: 5 - Production/Stable',

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

      setup_requires=['numpy'],
      install_requires=[
                       'numpy',
                       'scipy',
                       'netCDF4',
                       'matplotlib'
                       ],

      scripts=['livv'],
      packages=[
               'livvkit',
               'livvkit.bundles',
               'livvkit.bundles.CISM-glissade',
               'livvkit.bundles.CISM-albany',
               'livvkit.components',
               'livvkit.components.numerics_tests',
               'livvkit.components.validation_tests',
               'livvkit.components.validation_tests.template',
               'livvkit.data',
               'livvkit.util',
               ]
      )

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

try:
    import numpy
except ImportError:
    from setuptools.command import easy_install
    easy_install.main(["--user", 'numpy'])
    print("")
    print("--------------------------------------------------------------------")
    print("|                       *** ATTENTION! ***                         |")
    print("|                                                                  |")
    print("|    Numpy has been installed, but the build process must be       |")
    print("|    restarted in order to complete successfully.  Please run      |")
    print("|    the setup command again to proceed.                           |")
    print("|                                                                  |")
    print("--------------------------------------------------------------------")
    print("")

setup(name='livvkit',
      version='2.0.1',
      description='V&V library and toolkit for ice sheet models.',
      url='http://github.com/LIVVkit/LIVVkit',
      author='Oak Ridge National Laboratory',
      author_email='kennedyjh@ornl.gov',
      license='BSD',
      include_package_data=True,
      scripts=['livv'],
      install_requires=[
                        'scipy',
                        'netCDF4',
                        'matplotlib'
                       ],
      packages=[
                'livvkit',
                'livvkit.bundles',
                'livvkit.bundles.CISM-glissade',
                'livvkit.bundles.CISM-albany',
                'livvkit.components',
                'livvkit.components.numerics_tests',
                'livvkit.components.validation_tests',
                'livvkit.util',
                'livvkit.data'
               ]
    )


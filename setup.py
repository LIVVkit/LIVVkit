import os
import sys
import fnmatch
from setuptools import setup
from setuptools.command.build_ext import build_ext as _build_ext

def find_eggs(path):
    matches = []
    for base, dirs, files in os.walk(path):
        matches.extend(os.path.join(base, f) for f in fnmatch.filter(files, '*.egg'))
        matches.extend(os.path.join(base, d) for d in fnmatch.filter(dirs, '*.egg'))
    return matches

try:
    import numpy
except ImportError:
    from setuptools.command import easy_install
    easy_install.main(["--user", 'numpy'])
    [sys.path.append(ef) for ef in find_eggs(os.environ['HOME']+'/'+'.local') if ef not in sys.path]


setup(name='livvkit',
      version='1.0',
      description='V&V library and toolkit for ice sheet models.',
      url='http://github.com/LIVVkit/LIVVkit',
      author='Oak Ridge National Laboratory',
      author_email='evanskj@ornl.gov',
      license='BSD',
      include_package_data=True,
      scripts=['livv'],
      install_requires=[
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


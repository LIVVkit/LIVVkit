from setuptools import setup

setup(name='livvkit',
      version='1.0',
      description='V&V library and toolkit for ice sheet models.',
      url='http://github.com/LIVVkit/LIVVkit',
      author='Oak Ridge National Laboratory',
      author_email='evanskj@ornl.gov',
      license='BSD',
      include_package_data=True,
      scripts=['livvkit/livv'],
      install_requires=[
                        'numpy',
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


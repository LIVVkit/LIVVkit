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

